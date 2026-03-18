Write tests for the current changes. Follow these steps:

1. Read CLAUDE.md to understand the project's test framework and conventions.
2. Check `git diff` to identify what changed.
3. Find existing test files nearby to match patterns (file naming, fixtures, helpers).
4. Write focused tests that cover:
   - Happy path
   - Error / edge cases
   - Boundary conditions
5. Run the test suite to verify everything passes.

Do not over-mock. Prefer integration-style tests where practical.
