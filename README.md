# klausify

Claude Code boilerplate generator. One command to make any repo Claude Code-ready.

## Install

```bash
pip install klausify
```

Requires [conventions-cli](https://pypi.org/project/conventions-cli/) (installed automatically).

## Quick Start

```bash
cd your-repo
klausify init
```

That's it. You'll be prompted for your base branch (auto-detects `dev`, `main`, etc.), then klausify generates everything.

## What Gets Generated

```
.claude/
├── CLAUDE.md                                  # Repo conventions, path-scoped (via conventions-cli)
├── settings.json                              # Tool permissions + deny rules + PreCommit hooks
└── skills/
    ├── <repo>-review/SKILL.md                 # PR review with parallel sub-agents and repo-specific checks
    ├── <repo>-plan/SKILL.md                   # Multi-phase plan + implement (discovery, parallel architects, review)
    ├── <repo>-debug/SKILL.md                  # Debug an error with root-cause analysis and a failing test
    ├── <repo>-implement/SKILL.md              # Implement a pasted ticket/design with plan-mode investigation
    ├── <repo>-refactor/SKILL.md               # Refactor code while preserving behavior, test-backed
    ├── <repo>-test/SKILL.md                   # Write tests for current changes
    ├── <repo>-fix/SKILL.md                    # Fix lint/format/type errors
    ├── <repo>-pr/SKILL.md                     # Generate a PR description
    ├── <repo>-commit/SKILL.md                 # Generate a commit message
    ├── <repo>-explain/SKILL.md                # Explain code or current diff
    └── <repo>-new-worktree/SKILL.md           # Create a git worktree for a task

.github/
└── PULL_REQUEST_TEMPLATE.md                   # Only if repo doesn't have one

.gitignore                                     # Appends klausify output exclusions
```

### What each piece does

**CLAUDE.md** — Auto-detected conventions, architecture, commands, and pitfalls for your repo. As of 0.2.0 the `## Conventions` and `## Architecture` sections are grouped by inferred path globs (e.g. `### \`src/api/**/*.py\``, `### \`src/db/**/*.py\``, `### Project-wide`) so rules apply where they belong instead of as a flat list. This is what Claude Code reads to understand your project.

**settings.json** — Auto-detects your stack (Python, Node, Go, Rust, Make) and sets tool permissions. Detects sensitive files (`.env`, `*.pem`, `credentials*`) and adds deny rules so Claude can't read them.

**Skills** — Each repo gets a set of namespaced skills (`<repo>-<skill>`) so Claude Code auto-triggers them by description and they don't collide across repos. The bundled set is listed below; the canonical list lives in `SKILL_NAMES` in `src/klausify/skills.py`.

| Skill | What it does | Output |
|-------|-------------|--------|
| `<repo>-review` | Senior-level PR review against your base branch. Small PRs get a single-pass review; larger PRs fan out to parallel sub-agents (correctness, architecture, security, scope, plus an Agentic & Evals lens when the diff touches AI/agent/eval code) with a validation phase that removes false positives | `REVIEW_OUTPUT.md` |
| `<repo>-plan` | Multi-phase task planning + implementation: discovery → parallel exploration → clarify → parallel architectures → approval → implement → parallel review → summary | — |
| `<repo>-test` | Writes tests for current changes matching your repo's test patterns. Covers happy path, edge cases, and error paths without over-mocking | — |
| `<repo>-fix` | Fixes all lint, format, and type errors | — |
| `<repo>-pr` | Generates a ready-to-paste PR description | `pr-description.md` |
| `<repo>-commit` | Generates a commit message from staged changes | — |
| `<repo>-debug` | Five-phase debug flow: reproduce, diagnose root cause, write a failing test, fix, verify against the full suite | — |
| `<repo>-implement` | Implements a pasted ticket or design doc. Uses plan mode to investigate and plan before editing, enforces scope rules, and writes failing tests first for bug fixes | — |
| `<repo>-refactor` | Refactors code while preserving behavior exactly. Requires a passing test baseline, runs tests between every incremental step | — |
| `<repo>-new-worktree` | Creates a git worktree with a branch named for your task | — |
| `<repo>-explain` | Explains code or concept; defaults to explaining the current diff | — |

**PreCommit hooks** — Auto-detects your lint/format commands and runs them before each commit.

**PR template** — A basic PR template, only created if your repo doesn't already have one (checks root, `.github/`, and `docs/`).

**.gitignore** — Appends `pr-description.md` and `REVIEW_OUTPUT.md` so generated outputs don't get committed.

### Migrating from 0.1.x

If you ran an earlier version of klausify, you have `.claude/commands/*.md` files. On the next `klausify init` (with 0.2.0+) those files — and only the ones klausify itself created — are removed and replaced with `.claude/skills/<repo>-<skill>/SKILL.md`. Any commands you wrote yourself are left alone.

## Options

```bash
klausify init [OPTIONS]

Options:
  -r, --repo PATH             Target repository (default: current directory)
  -f, --force                 Overwrite existing files
  -b, --base-branch TEXT      Base branch for diffs (default: auto-detect, prompts)
  --skip-enrich               Skip Claude CLI enrichment (faster, no API call)
  --review-template PATH      Use a custom review prompt instead of the default
```

### Custom review template

If your team has a specific review checklist (e.g. domain-specific checks, security requirements), pass it in:

```bash
klausify init --review-template path/to/your-review.md
```

The template will be used as the body of the `<repo>-review` skill instead of the default. Custom templates are responsible for supplying their own SKILL.md frontmatter.

## Individual Commands

You can run each step individually:

```bash
klausify checklist              # Regenerate the review skill from CLAUDE.md
klausify skills                 # Regenerate all skills
klausify settings               # Regenerate settings.json
klausify hooks                  # Regenerate hook configs
klausify github                 # Regenerate PR template
```

All subcommands support `--repo`, `--force`, and `--base-branch` where applicable.

## How It Works

1. Runs `conventions discover --claude --init` to analyze your codebase and generate `CLAUDE.md` with path-scoped conventions and architecture sections
2. Parses `CLAUDE.md` to extract conventions, commands, and pitfalls (including which file globs each rule applies to)
3. Injects those into the review skill template so `<repo>-review` checks repo-specific rules with the right path scope
4. Detects your stack from marker files (`pyproject.toml`, `package.json`, `go.mod`, etc.)
5. Sets permissions, deny rules, and hooks based on what it finds
6. Skips anything that already exists (PR template) unless `--force` is used

## Claude Code Integration

klausify can be used three ways with Claude Code:

### As a CLI (simplest)

```bash
pip install klausify
klausify init
```

### As a Claude Code Plugin

Install the plugin directly from GitHub:

```
/plugin install https://github.com/steph-dove/klausify
```

This gives you the `klausify-init` skill and the MCP server.

### As an MCP Server

Add klausify as an MCP server so Claude can invoke it directly:

```bash
pip install klausify[mcp]
claude mcp add --transport stdio klausify -- klausify-mcp
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "klausify": {
      "command": "klausify-mcp",
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

The MCP server exposes these tools: `klausify_init`, `klausify_checklist`, `klausify_skills`, `klausify_settings`, `klausify_status`.

## Requirements

- Python 3.10+
- [conventions-cli](https://pypi.org/project/conventions-cli/) >= 1.4.0
- [Claude Code CLI](https://www.npmjs.com/package/@anthropic-ai/claude-code) (optional, for `--init` enrichment)
- [mcp](https://pypi.org/project/mcp/) (optional, for MCP server: `pip install klausify[mcp]`)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor guidelines.

## License

MIT — see [LICENSE](LICENSE) for details.

## Ownership and Governance

klausify is an open-source project owned and maintained by Dovatech LLC.

Dovatech LLC is a privately held company founded and wholly owned by Stephanie Dover, who is also the original author and lead maintainer of this project.
