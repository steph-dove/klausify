"""Wraps conventions-cli to generate and enrich CLAUDE.md."""

import subprocess
import sys
from pathlib import Path

from rich.console import Console

console = Console()


def run_init(*, repo: Path, force: bool = False, skip_enrich: bool = False) -> Path:
    """Run conventions-cli discover --claude [--init] to produce ./CLAUDE.md.

    As of conventions-cli 1.4.0 the canonical location for the generated file
    is the repo root (./CLAUDE.md), with path-scoped rules emitted as
    `.claude/rules/<name>.md` files alongside.
    """
    repo = repo.resolve()
    claude_md = repo / "CLAUDE.md"

    if claude_md.exists() and not force:
        console.print(
            f"[yellow]⚠ {claude_md} already exists. Use --force to overwrite.[/yellow]"
        )
        raise SystemExit(1)

    # Install/upgrade conventions-cli to latest
    console.print("[dim]Ensuring latest conventions-cli...[/dim]")
    upgrade_result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "conventions-cli"],
        capture_output=True,
    )
    if upgrade_result.returncode != 0:
        # Fall back to pipx/uvx if pip fails
        for runner in ["uvx", "pipx"]:
            fallback = subprocess.run(
                [runner, "install", "conventions-cli", "--force"],
                capture_output=True,
            )
            if fallback.returncode == 0:
                break
        else:
            console.print(
                "[red]✗ Could not install conventions-cli. "
                "Install it manually: pip install conventions-cli[/red]"
            )
            raise SystemExit(1)

    # Build command
    cmd: list[str] = ["conventions", "discover", "--repo", str(repo), "--claude"]
    if not skip_enrich:
        cmd.append("--init")

    console.print(f"[bold]Running:[/bold] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(repo))

    if result.returncode != 0:
        console.print("[red]✗ conventions-cli failed.[/red]")
        raise SystemExit(result.returncode)

    if claude_md.exists():
        console.print(f"[green]✔ Created {claude_md.relative_to(repo)}[/green]")
    else:
        # Older conventions-cli (<1.4.0) wrote to .claude/CLAUDE.md when --claude
        # was passed. Fall back to that location if the root file is missing.
        legacy_path = repo / ".claude" / "CLAUDE.md"
        if legacy_path.exists():
            console.print(
                f"[yellow]⚠ CLAUDE.md found at legacy path {legacy_path.relative_to(repo)}; "
                "upgrade conventions-cli >= 1.4.0 for repo-root output.[/yellow]"
            )
            return legacy_path
        console.print(
            "[yellow]⚠ CLAUDE.md was not created — check conventions-cli output.[/yellow]"
        )
        raise SystemExit(1)

    return claude_md
