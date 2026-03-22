"""Tests for klausify CLI and modules."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from klausify.agents import scaffold_agents
from klausify.checklist import _parse_claude_md, generate_checklist
from klausify.cli import app
from klausify.commands import scaffold_commands
from klausify.github import scaffold_github
from klausify.gitignore import update_gitignore
from klausify.hooks import _detect_format_command, _detect_lint_command, scaffold_hooks
from klausify.settings import _detect_sensitive_paths, _detect_stack, generate_settings

runner = CliRunner()

SAMPLE_CLAUDE_MD = """\
# CLAUDE.md - test-project

## Project Overview

A test project.

## Tech Stack

- python
- pytest
- ruff

## Commands

- **Install**: `pip install -e .`
- **Test**: `pytest`
- **Lint**: `ruff check .`

## Conventions

- **snake_case** for all function and variable names
- **Type hints** required on all public functions
- **Docstrings** on all modules and public functions

## Known Pitfalls

- **PYTHONPATH** must include src/ for imports to resolve
- **ruff** ignores E501 in this project
"""


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Create a minimal repo structure."""
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"\n')
    return tmp_path


@pytest.fixture()
def repo_with_claude_md(repo: Path) -> Path:
    """Create a repo with .claude/CLAUDE.md."""
    claude_dir = repo / ".claude"
    claude_dir.mkdir()
    (claude_dir / "CLAUDE.md").write_text(SAMPLE_CLAUDE_MD)
    return repo


class TestVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "klausify" in result.stdout


class TestSettings:
    def test_detect_python_stack(self, repo: Path):
        stack = _detect_stack(repo)
        assert stack["python"] is True
        assert stack["node"] is False

    def test_generate_settings(self, repo: Path):
        path = generate_settings(repo=repo)
        settings = json.loads(path.read_text())
        assert "permissions" in settings
        assert "Bash(pytest *)" in settings["permissions"]["allow"]

    def test_generate_settings_no_overwrite(self, repo: Path):
        generate_settings(repo=repo)
        with pytest.raises(SystemExit):
            generate_settings(repo=repo)

    def test_generate_settings_force(self, repo: Path):
        generate_settings(repo=repo)
        path = generate_settings(repo=repo, force=True)
        assert path.exists()

    def test_detect_sensitive_paths(self, repo: Path):
        (repo / ".env").write_text("SECRET=abc\n")
        deny = _detect_sensitive_paths(repo)
        assert "Read(.env)" in deny
        assert "Edit(.env)" in deny

    def test_settings_includes_deny_rules(self, repo: Path):
        (repo / ".env").write_text("SECRET=abc\n")
        path = generate_settings(repo=repo)
        settings = json.loads(path.read_text())
        assert len(settings["permissions"]["deny"]) > 0


class TestCommands:
    def test_scaffold_commands(self, repo: Path):
        created = scaffold_commands(repo=repo)
        assert len(created) == 6
        for f in created:
            assert f.exists()
            assert f.suffix == ".md"
        names = [f.name for f in created]
        assert "commit.md" in names
        assert "debug.md" in names
        assert f"pr-review-{repo.name}.md" in names
        assert "review.md" not in names

    def test_scaffold_commands_idempotent(self, repo: Path):
        scaffold_commands(repo=repo)
        created = scaffold_commands(repo=repo)
        assert len(created) == 0

    def test_scaffold_commands_force(self, repo: Path):
        scaffold_commands(repo=repo)
        created = scaffold_commands(repo=repo, force=True)
        assert len(created) == 6

    def test_scaffold_commands_base_branch(self, repo: Path):
        scaffold_commands(repo=repo, base_branch="dev")
        pr_content = (repo / ".claude" / "commands" / "pr.md").read_text()
        assert "dev..HEAD" in pr_content
        assert "{{BASE_BRANCH}}" not in pr_content


class TestChecklist:
    def test_parse_claude_md(self, repo_with_claude_md: Path):
        claude_md = repo_with_claude_md / ".claude" / "CLAUDE.md"
        sections = _parse_claude_md(claude_md)
        assert len(sections["conventions"]) == 3
        assert len(sections["commands"]) == 3
        assert len(sections["pitfalls"]) == 2

    def test_generate_checklist(self, repo_with_claude_md: Path):
        path = generate_checklist(repo=repo_with_claude_md)
        expected = f"pr-review-{repo_with_claude_md.name}.md"
        assert path == repo_with_claude_md / ".claude" / "commands" / expected
        content = path.read_text()
        assert "snake_case" in content
        assert "`pytest`" in content
        assert "PYTHONPATH" in content
        assert "Severity: Blocker" in content
        assert "Overall verdict" in content

    def test_generate_checklist_base_branch(self, repo_with_claude_md: Path):
        path = generate_checklist(repo=repo_with_claude_md, base_branch="develop")
        content = path.read_text()
        assert "develop..HEAD" in content
        assert "{{BASE_BRANCH}}" not in content

    def test_generate_checklist_no_claude_md(self, repo: Path):
        with pytest.raises(SystemExit):
            generate_checklist(repo=repo)


class TestHooks:
    def test_detect_lint_python(self, repo: Path):
        cmd = _detect_lint_command(repo)
        assert cmd == "ruff check --fix ."

    def test_detect_format_python(self, repo: Path):
        cmd = _detect_format_command(repo)
        assert cmd == "ruff format ."

    def test_scaffold_hooks(self, repo: Path):
        path = scaffold_hooks(repo=repo)
        settings = json.loads(path.read_text())
        assert "hooks" in settings
        assert "PreCommit" in settings["hooks"]


class TestGitHub:
    def test_scaffold_github(self, repo: Path):
        result = scaffold_github(repo=repo)
        assert result is not None
        assert result.name == "PULL_REQUEST_TEMPLATE.md"

    def test_scaffold_github_skips_existing_pr_template(self, repo: Path):
        pr_template = repo / ".github" / "PULL_REQUEST_TEMPLATE.md"
        pr_template.parent.mkdir(parents=True, exist_ok=True)
        pr_template.write_text("# Existing template\n")
        result = scaffold_github(repo=repo)
        assert result is None
        assert pr_template.read_text() == "# Existing template\n"

    def test_scaffold_github_skips_docs_template(self, repo: Path):
        docs_template = repo / "docs" / "pull_request_template.md"
        docs_template.parent.mkdir(parents=True, exist_ok=True)
        docs_template.write_text("# Docs template\n")
        result = scaffold_github(repo=repo)
        assert result is None


class TestAgents:
    def test_scaffold_agents(self, repo: Path):
        result = scaffold_agents(repo=repo)
        assert result is not None
        assert result.name == "AGENTS.md"
        assert "CLAUDE.md" in result.read_text()

    def test_scaffold_agents_skips_existing(self, repo: Path):
        (repo / "AGENTS.md").write_text("# Custom agents\n")
        result = scaffold_agents(repo=repo)
        assert result is None
        assert (repo / "AGENTS.md").read_text() == "# Custom agents\n"


class TestGitignore:
    def test_update_gitignore_new(self, repo: Path):
        update_gitignore(repo=repo)
        content = (repo / ".gitignore").read_text()
        assert "pr-description.md" in content
        assert "REVIEW_OUTPUT.md" in content

    def test_update_gitignore_existing(self, repo: Path):
        (repo / ".gitignore").write_text("node_modules/\n")
        update_gitignore(repo=repo)
        content = (repo / ".gitignore").read_text()
        assert "node_modules/" in content
        assert "pr-description.md" in content

    def test_update_gitignore_idempotent(self, repo: Path):
        update_gitignore(repo=repo)
        update_gitignore(repo=repo)
        content = (repo / ".gitignore").read_text()
        assert content.count("pr-description.md") == 1
