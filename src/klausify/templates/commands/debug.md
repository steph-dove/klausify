Debug the error or issue described below. Follow these steps:

1. Read CLAUDE.md to understand the project structure, test commands, and known pitfalls.
2. Run `git diff` and `git log --oneline -10` to see recent changes and commits — regressions often hide here.
3. Analyze the error message or described behavior.
4. Search the codebase for the relevant code using Grep and Glob.
5. Read the full files involved to understand context.
6. Identify the root cause.
7. Implement the fix.
8. Run the project's test command to verify the fix doesn't break anything.

Rules:
- Fix the root cause, not the symptom.
- Don't change unrelated code.
- If the fix touches a hot path, consider performance implications.
- If you're unsure about the root cause, explain your hypothesis before changing code.
- After fixing, run tests to verify.

$ARGUMENTS
