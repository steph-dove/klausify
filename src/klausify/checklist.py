"""Generate a repo-tailored review command from CLAUDE.md."""

import re
from importlib import resources
from pathlib import Path

from rich.console import Console

console = Console()


def _read_review_template() -> str:
    """Read the review command template."""
    return resources.files("klausify").joinpath("templates/commands/review.md").read_text()


def _parse_claude_md(claude_md: Path) -> dict[str, list[str]]:
    """Extract key sections from CLAUDE.md for review enrichment."""
    content = claude_md.read_text()
    sections: dict[str, list[str]] = {
        "conventions": [],
        "commands": [],
        "tech_stack": [],
        "pitfalls": [],
    }

    current_section = ""
    for line in content.splitlines():
        heading = line.strip().lower()
        if heading.startswith("## conventions"):
            current_section = "conventions"
        elif heading.startswith("## commands"):
            current_section = "commands"
        elif heading.startswith("## tech stack"):
            current_section = "tech_stack"
        elif heading.startswith("## known pitfalls"):
            current_section = "pitfalls"
        elif heading.startswith("## "):
            current_section = ""
        elif current_section and line.strip().startswith("- "):
            sections[current_section].append(line.strip())

    return sections


def _build_convention_checks(conventions: list[str]) -> str:
    """Turn convention bullet points into review check items."""
    if not conventions:
        return ""
    lines = ["### Repo Conventions"]
    for conv in conventions:
        label = re.sub(r"^\-\s*", "", conv)
        label = re.sub(r"\*\*(.+?)\*\*", r"\1", label)
        lines.append(f"- {label}")
    return "\n".join(lines)


def _build_command_checks(commands: list[str]) -> str:
    """Turn command items into verification checks."""
    if not commands:
        return ""
    lines = ["### Verification Commands", "Ensure these pass before approving:"]
    for cmd in commands:
        label = re.sub(r"^\-\s*", "", cmd)
        code_match = re.search(r"`(.+?)`", label)
        if code_match:
            lines.append(f"- `{code_match.group(1)}`")
    return "\n".join(lines)


def _build_pitfall_checks(pitfalls: list[str]) -> str:
    """Turn known pitfalls into review watch items."""
    if not pitfalls:
        return ""
    lines = ["### Known Pitfalls", "Flag if any of these are violated:"]
    for pitfall in pitfalls:
        label = re.sub(r"^\-\s*", "", pitfall)
        label = re.sub(r"\*\*(.+?)\*\*", r"\1", label)
        lines.append(f"- {label}")
    return "\n".join(lines)


def _review_filename(repo: Path) -> str:
    """Return the review command filename scoped to the repo name."""
    return f"pr-review-{repo.name}.md"


def generate_checklist(*, repo: Path, force: bool = False, base_branch: str = "main") -> Path:
    """Generate a review command enriched with CLAUDE.md findings."""
    repo = repo.resolve()
    claude_md = repo / ".claude" / "CLAUDE.md"

    if not claude_md.exists():
        console.print(
            "[red]✗ .claude/CLAUDE.md not found. Run `klausify init` first.[/red]"
        )
        raise SystemExit(1)

    output_file = repo / ".claude" / "commands" / _review_filename(repo)

    if output_file.exists() and not force:
        console.print(
            f"[yellow]⚠ {output_file.relative_to(repo)} already exists. "
            "Use --force to overwrite.[/yellow]"
        )
        raise SystemExit(1)

    # Read template and CLAUDE.md
    template = _read_review_template()
    sections = _parse_claude_md(claude_md)

    # Build enrichment sections
    enrichments: list[str] = []
    conv_checks = _build_convention_checks(sections["conventions"])
    if conv_checks:
        enrichments.append(conv_checks)
    cmd_checks = _build_command_checks(sections["commands"])
    if cmd_checks:
        enrichments.append(cmd_checks)
    pitfall_checks = _build_pitfall_checks(sections["pitfalls"])
    if pitfall_checks:
        enrichments.append(pitfall_checks)

    # Merge into template
    enrichment_block = "\n\n".join(enrichments) if enrichments else ""
    output = template.replace("{{REPO_SPECIFIC_CHECKS}}", enrichment_block)
    output = output.replace("{{BASE_BRANCH}}", base_branch)

    # Write
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(output)
    console.print(f"[green]✔ Created {output_file.relative_to(repo)}[/green]")
    return output_file
