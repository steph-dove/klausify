"""Scaffold Claude Code hook configurations."""

import json
from pathlib import Path

from rich.console import Console

console = Console()


def _detect_lint_command(repo: Path) -> str | None:
    """Detect the project's lint command."""
    if (repo / "pyproject.toml").exists():
        return "ruff check --fix ."
    if (repo / "package.json").exists():
        pkg = json.loads((repo / "package.json").read_text())
        scripts = pkg.get("scripts", {})
        if "lint" in scripts:
            return "npm run lint"
        if "lint:fix" in scripts:
            return "npm run lint:fix"
    if (repo / "Makefile").exists():
        content = (repo / "Makefile").read_text()
        if "lint" in content:
            return "make lint"
    return None


def _detect_format_command(repo: Path) -> str | None:
    """Detect the project's format command."""
    if (repo / "pyproject.toml").exists():
        return "ruff format ."
    if (repo / "package.json").exists():
        pkg = json.loads((repo / "package.json").read_text())
        scripts = pkg.get("scripts", {})
        if "format" in scripts:
            return "npm run format"
        if "prettier" in " ".join(scripts.values()):
            return "npx prettier --write ."
    if (repo / "Makefile").exists():
        content = (repo / "Makefile").read_text()
        if "format" in content:
            return "make format"
    return None


def scaffold_hooks(*, repo: Path, force: bool = False) -> Path:
    """Add hook configurations to .claude/settings.json."""
    repo = repo.resolve()
    settings_file = repo / ".claude" / "settings.json"

    # Load existing settings or start fresh
    if settings_file.exists():
        settings = json.loads(settings_file.read_text())
    else:
        settings = {}

    if "hooks" in settings and not force:
        console.print(
            "[yellow]⚠ Hooks already configured in settings.json. "
            "Use --force to overwrite.[/yellow]"
        )
        raise SystemExit(1)

    lint_cmd = _detect_lint_command(repo)
    format_cmd = _detect_format_command(repo)

    hooks: dict = {}

    # PreCommit hook: run lint + format before committing
    pre_commit_commands: list[str] = []
    if format_cmd:
        pre_commit_commands.append(format_cmd)
    if lint_cmd:
        pre_commit_commands.append(lint_cmd)

    if pre_commit_commands:
        hooks["PreCommit"] = [
            {
                "command": " && ".join(pre_commit_commands),
                "description": "Auto-format and lint before committing",
            }
        ]

    if hooks:
        settings["hooks"] = hooks
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        settings_file.write_text(json.dumps(settings, indent=2) + "\n")
        console.print(f"[green]✔ Added hooks to {settings_file.relative_to(repo)}[/green]")
    else:
        console.print("[dim]No hooks to add (couldn't detect lint/format commands).[/dim]")

    return settings_file
