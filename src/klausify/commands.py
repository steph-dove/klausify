"""Scaffold .claude/commands/ with custom slash commands."""

from importlib import resources
from pathlib import Path

from rich.console import Console

from klausify import __version__

console = Console()

COMMAND_FILES = [
    "review.md",
    "test.md",
    "fix.md",
    "pr.md",
    "commit.md",
    "debug.md",
    "new-worktree.md",
    "explain.md",
    "implement.md",
    "refactor.md",
]

VERSION_FILE = ".klausify-version"


def _review_filename(repo: Path) -> str:
    """Return the review command filename scoped to the repo name."""
    return f"pr-review-{repo.name}.md"


def _read_version(commands_dir: Path) -> str | None:
    """Read the klausify version that last generated commands."""
    version_path = commands_dir / VERSION_FILE
    if version_path.exists():
        return version_path.read_text().strip()
    return None


def _write_version(commands_dir: Path) -> None:
    """Write the current klausify version to the marker file."""
    (commands_dir / VERSION_FILE).write_text(__version__ + "\n")


def scaffold_commands(
    *,
    repo: Path,
    force: bool = False,
    review_template: Path | None = None,
    base_branch: str = "main",
) -> list[Path]:
    """Create .claude/commands/ with review, test, fix, and pr slash commands."""
    repo = repo.resolve()
    commands_dir = repo / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)

    existing_version = _read_version(commands_dir)
    if existing_version == __version__ and not force:
        console.print(
            f"[dim]Commands already up to date (v{__version__}), skipping.[/dim]"
        )
        return []

    created: list[Path] = []
    templates = resources.files("klausify").joinpath("templates/commands")

    for filename in COMMAND_FILES:
        # Rename review.md to pr-review-<repo>.md
        target_filename = _review_filename(repo) if filename == "review.md" else filename
        target = commands_dir / target_filename

        # Use custom review template if provided
        if filename == "review.md" and review_template is not None:
            content = review_template.read_text()
        else:
            content = templates.joinpath(filename).read_text()

        # Substitute base branch
        content = content.replace("{{BASE_BRANCH}}", base_branch)

        # Skip if content hasn't changed
        if target.exists() and target.read_text() == content and not force:
            console.print(
                f"[dim]  {target.relative_to(repo)} unchanged, skipping.[/dim]"
            )
            continue

        target.write_text(content)
        created.append(target)
        console.print(f"[green]✔ Created {target.relative_to(repo)}[/green]")

    _write_version(commands_dir)

    if not created:
        console.print("[dim]No command files created.[/dim]")

    return created
