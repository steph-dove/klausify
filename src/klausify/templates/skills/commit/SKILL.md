---
name: {{REPO}}-commit
description: Use when the user wants a commit message written for currently staged changes. Reads `git diff --cached`, recent log style, and CLAUDE.md, then outputs a conventional-commit-style message — type(scope) summary + why-focused body.
allowed-tools: Read, Bash
---

Write a commit message for the currently staged changes. Follow these steps:

1. Run `git diff --cached --stat` to see what's staged.
2. Run `git diff --cached` to read the actual changes.
3. Read CLAUDE.md to understand the project's commit conventions.
4. Run `git log --oneline -10` to see recent commit message style.

Write a commit message following this format:

```
<type>(<scope>): <short summary>

<body - explain what changed and why, not how>
```

Types: feat, fix, refactor, test, docs, chore, style, perf
Scope: the area of code affected (e.g. auth, api, ui)

Rules:
- Summary line under 72 characters.
- Body wraps at 80 characters.
- Match the style of recent commits in the repo.
- Focus on "why" in the body, not "what" (the diff shows "what").
- If the branch name has a ticket reference, include it in the body.

Output ONLY the commit message, nothing else. Do not wrap it in code blocks.
