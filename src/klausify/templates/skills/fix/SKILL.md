---
name: {{REPO}}-fix
description: Use when the user wants lint, format, and type errors fixed in the current changes. Reads CLAUDE.md for the repo's lint/format/type-check commands, runs each, and fixes only style/format/type issues — no behavior changes.
allowed-tools: Read Grep Glob Bash Edit
---

Fix all lint, format, and type errors in the current changes.

1. Read CLAUDE.md to find the project's lint, format, and type-check commands.
2. Run each command and collect errors.
3. Fix all reported issues.
4. Re-run the commands to verify everything is clean.

Do not change logic or behavior — only fix style, formatting, and type issues.
