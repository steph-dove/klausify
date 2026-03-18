"""Detect or generate AGENTS.md."""

from pathlib import Path

from rich.console import Console

console = Console()

AGENTS_TEMPLATE = """\
# AGENTS.md

## Instructions for AI agents

- Read CLAUDE.md before starting any task.
- Follow the conventions documented there.
- Run the project's test suite after making changes.
- Do not modify files outside the scope of your task.
- Ask for clarification rather than guessing.
"""


def scaffold_agents(*, repo: Path, force: bool = False) -> Path | None:
    """Create AGENTS.md if the repo doesn't already have one."""
    repo = repo.resolve()
    agents_file = repo / "AGENTS.md"

    if agents_file.exists() and not force:
        console.print("[dim]AGENTS.md already exists, skipping.[/dim]")
        return None

    agents_file.write_text(AGENTS_TEMPLATE)
    console.print(f"[green]✔ Created {agents_file.relative_to(repo)}[/green]")
    return agents_file
