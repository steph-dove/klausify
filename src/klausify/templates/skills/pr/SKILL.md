---
name: {{REPO}}-pr
description: Use when the user wants a PR description generated for the current branch. Reads commit history, file changes, and CLAUDE.md, then writes a Summary / Changes / Test Plan / Notes block to pr-description.md.
allowed-tools: Read Grep Glob Bash(git *) Write
disable-model-invocation: true
---

Generate a PR description for the current branch. Follow these steps:

1. Run `git branch --show-current` to get the branch name. Extract any ticket reference (e.g. FEAT-1234).
2. Run `git log {{BASE_BRANCH}}..HEAD --oneline` to understand the commit history.
3. Run `git diff {{BASE_BRANCH}}...HEAD --stat` to see which files changed.
4. For key changed files, read them to understand the full context of the changes.
5. Read CLAUDE.md for project conventions and context.

Generate a PR description in this format:

```markdown
## Summary

<!-- 1-3 sentences explaining what this PR does and why -->

## Changes

<!-- Bullet list of key changes, grouped logically -->

## Test Plan

<!-- How the changes were tested -->
- [ ] Tests pass locally
- [ ] Manually verified

## Notes

<!-- Anything reviewers should pay attention to, migration steps, feature flags, etc. -->
```

Rules:
- Be specific — reference actual file names, functions, and components.
- Focus on the "why" not just the "what".
- If the branch name has a ticket reference, include it in the summary.
- Keep it concise. No filler.
- If there are database changes, call them out explicitly.
- If there are new dependencies, mention them.

Write the output to `pr-description.md` in the repo root.
