---
name: klausify-init
description: Generate all Claude Code boilerplate for this repository — CLAUDE.md, settings, slash commands, hooks, and PR template
argument-hint: "[--force] [--skip-enrich] [--base-branch dev]"
allowed-tools: "Bash(pipx *), Bash(klausify *), Read"
---

# Klausify Init

Set up Claude Code boilerplate for this project by running klausify.

Run:
```
pipx run klausify init $ARGUMENTS
```

If klausify prompts for a base branch, detect it from the repo:
- Check if `dev`, `develop`, `main`, or `master` exists
- Use whichever is found as the default

After klausify completes, read `.claude/CLAUDE.md` to confirm it was generated correctly.
