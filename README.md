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
├── CLAUDE.md                    # Repo conventions (via conventions-cli)
├── settings.json                # Tool permissions + deny rules + PreCommit hooks
└── commands/
    ├── review.md                # PR review with repo-specific checks
    ├── test.md                  # Write tests for current changes
    ├── fix.md                   # Fix lint/format/type errors
    ├── pr.md                    # Generate a PR description
    ├── commit.md                # Generate a commit message
    └── debug.md                 # Debug an error with repo context

.github/
└── PULL_REQUEST_TEMPLATE.md     # Only if repo doesn't have one

AGENTS.md                        # Only if repo doesn't have one

.gitignore                       # Appends klausify output exclusions
```

### What each piece does

**CLAUDE.md** — Auto-detected conventions, architecture, commands, and pitfalls for your repo. This is what Claude Code reads to understand your project.

**settings.json** — Auto-detects your stack (Python, Node, Go, Rust, Make) and sets tool permissions. Detects sensitive files (`.env`, `*.pem`, `credentials*`) and adds deny rules so Claude can't read them.

**Slash commands** — Available as `/review`, `/test`, `/fix`, `/pr`, `/commit`, `/debug` in Claude Code:

| Command | What it does | Output |
|---------|-------------|--------|
| `/review` | Senior-level PR review against your base branch, enriched with repo conventions | `REVIEW_OUTPUT.md` |
| `/test` | Writes tests for current changes matching your repo's test patterns | — |
| `/fix` | Fixes all lint, format, and type errors | — |
| `/pr` | Generates a ready-to-paste PR description | `pr-description.md` |
| `/commit` | Generates a commit message from staged changes | — |
| `/debug` | Debugs an error using repo context and test commands | — |

**PreCommit hooks** — Auto-detects your lint/format commands and runs them before each commit.

**PR template** — A basic PR template, only created if your repo doesn't already have one (checks root, `.github/`, and `docs/`).

**AGENTS.md** — Lightweight instructions for AI agents, only created if one doesn't exist.

**.gitignore** — Appends `pr-description.md` and `REVIEW_OUTPUT.md` so generated outputs don't get committed.

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

The template will be used as the `/review` slash command instead of the default.

## Individual Commands

You can run each step individually:

```bash
klausify checklist              # Regenerate review command from CLAUDE.md
klausify commands               # Regenerate slash commands
klausify settings               # Regenerate settings.json
klausify hooks                  # Regenerate hook configs
klausify github                 # Regenerate PR template
```

All subcommands support `--repo`, `--force`, and `--base-branch` where applicable.

## How It Works

1. Runs `conventions discover --claude --init` to analyze your codebase and generate `CLAUDE.md`
2. Parses `CLAUDE.md` to extract conventions, commands, and pitfalls
3. Injects those into the review command template so `/review` checks repo-specific rules
4. Detects your stack from marker files (`pyproject.toml`, `package.json`, `go.mod`, etc.)
5. Sets permissions, deny rules, and hooks based on what it finds
6. Skips anything that already exists (PR template, AGENTS.md) unless `--force` is used

## Requirements

- Python 3.10+
- [conventions-cli](https://pypi.org/project/conventions-cli/) >= 1.3.0
- [Claude Code CLI](https://www.npmjs.com/package/@anthropic-ai/claude-code) (optional, for `--init` enrichment)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor guidelines.

## License

MIT — see [LICENSE](LICENSE) for details.

## Ownership and Governance

klausify is an open-source project owned and maintained by Dovatech LLC.

Dovatech LLC is a privately held company founded and wholly owned by Stephanie Dover, who is also the original author and lead maintainer of this project.
