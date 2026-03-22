"""Scaffold .claude/commands/ with custom slash commands."""

from importlib import resources
from pathlib import Path

from rich.console import Console

console = Console()

COMMAND_FILES = ["review.md", "test.md", "fix.md", "pr.md", "commit.md", "debug.md"]


def _review_filename(repo: Path) -> str:
    """Return the review command filename scoped to the repo name."""
    return f"pr-review-{repo.name}.md"


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

    created: list[Path] = []
    templates = resources.files("klausify").joinpath("templates/commands")

    for filename in COMMAND_FILES:
        # Rename review.md to pr-review-<repo>.md
        target_filename = _review_filename(repo) if filename == "review.md" else filename
        target = commands_dir / target_filename
        if target.exists() and not force:
            console.print(
                f"[yellow]⚠ {target.relative_to(repo)} already exists, skipping.[/yellow]"
            )
            continue

        # Use custom review template if provided
        if filename == "review.md" and review_template is not None:
            content = review_template.read_text()
        else:
            content = templates.joinpath(filename).read_text()

        # Substitute base branch
        content = content.replace("{{BASE_BRANCH}}", base_branch)

        target.write_text(content)
        created.append(target)
        console.print(f"[green]✔ Created {target.relative_to(repo)}[/green]")

    if not created:
        console.print("[dim]No command files created (all exist, use --force to overwrite).[/dim]")

    return created
