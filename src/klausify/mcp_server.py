"""MCP server for klausify — exposes klausify subcommands as tools."""

import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("klausify")


def _run_klausify(*args: str, cwd: str = ".") -> str:
    """Run a klausify CLI command and return output."""
    result = subprocess.run(
        ["klausify", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    output = result.stdout
    if result.stderr:
        output += "\n" + result.stderr
    if result.returncode != 0:
        output += f"\n[exit code: {result.returncode}]"
    return output.strip()


@mcp.tool()
def klausify_init(
    repo: str = ".",
    base_branch: str = "main",
    force: bool = False,
    skip_enrich: bool = False,
) -> str:
    """Generate all Claude Code boilerplate for a repository.

    Creates CLAUDE.md, settings.json, namespaced skills, hooks, PR template,
    AGENTS.md, and .gitignore entries.
    """
    args = ["init", "--repo", repo, "--base-branch", base_branch]
    if force:
        args.append("--force")
    if skip_enrich:
        args.append("--skip-enrich")
    return _run_klausify(*args, cwd=repo)


@mcp.tool()
def klausify_checklist(
    repo: str = ".",
    base_branch: str = "main",
    force: bool = False,
) -> str:
    """Regenerate the review skill from CLAUDE.md with repo-specific checks."""
    args = ["checklist", "--repo", repo, "--base-branch", base_branch]
    if force:
        args.append("--force")
    return _run_klausify(*args, cwd=repo)


@mcp.tool()
def klausify_settings(repo: str = ".", force: bool = False) -> str:
    """Generate .claude/settings.json with auto-detected stack permissions."""
    args = ["settings", "--repo", repo]
    if force:
        args.append("--force")
    return _run_klausify(*args, cwd=repo)


@mcp.tool()
def klausify_skills(
    repo: str = ".",
    base_branch: str = "main",
    force: bool = False,
) -> str:
    """Scaffold .claude/skills/<repo>-<skill>/SKILL.md for review, plan, debug, and 8 others."""
    args = ["skills", "--repo", repo, "--base-branch", base_branch]
    if force:
        args.append("--force")
    return _run_klausify(*args, cwd=repo)


SKILL_NAMES = [
    "review", "plan", "debug", "implement", "refactor",
    "test", "fix", "pr", "commit", "explain", "new-worktree",
]


@mcp.tool()
def klausify_status(repo: str = ".") -> str:
    """Check which klausify boilerplate files exist in a repository."""
    repo_path = Path(repo).resolve()
    files = {
        ".claude/CLAUDE.md": repo_path / ".claude" / "CLAUDE.md",
        ".claude/settings.json": repo_path / ".claude" / "settings.json",
        "AGENTS.md": repo_path / "AGENTS.md",
    }
    for skill in SKILL_NAMES:
        skill_dir = f"{repo_path.name}-{skill}"
        rel_path = f".claude/skills/{skill_dir}/SKILL.md"
        files[rel_path] = repo_path / ".claude" / "skills" / skill_dir / "SKILL.md"

    status = {}
    for name, path in files.items():
        status[name] = "exists" if path.exists() else "missing"

    return json.dumps(status, indent=2)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
