---
name: {{REPO}}-test
description: Use when the user wants tests written for current changes (uncommitted diff or recent feature). Matches the repo's existing test framework, fixtures, and assertion style. Covers happy path, edge cases, and error paths without over-mocking.
allowed-tools: Read Grep Glob Bash Edit Write
---

Write tests for the current changes. Follow these steps:

1. **Read CLAUDE.md** to understand the project's test framework, conventions, and test commands.
2. **Check `git diff`** to identify what changed. Understand the behavior being added or modified before writing tests.
3. **Find existing test files** for the modules you're testing. Read them fully — match their patterns:
   - File naming and location conventions.
   - Fixtures, factories, helpers, and setup/teardown patterns.
   - Assertion style and test structure.
   - How similar features are tested (use as a template).
4. **Write focused tests** that cover:
   - **Happy path** — the expected behavior works correctly.
   - **Edge cases** — empty inputs, boundary values, null/nil, large inputs.
   - **Error cases** — invalid input, missing data, permission failures. Test that errors are handled, not just that they don't crash.
   - **Behavior, not implementation** — test what the code does, not how it does it. Tests should survive a refactor that preserves behavior.
5. **Run the test suite** to verify everything passes, including your new tests.

## Rules

- **Match existing patterns.** If the codebase uses factories, use factories. If it uses fixtures, use fixtures. Don't introduce a new testing pattern.
- **Don't over-mock.** Prefer integration-style tests where practical. Mocks that stub out the thing you're trying to test hide real bugs. Only mock external services, slow I/O, or things that are genuinely impractical to use in tests.
- **Don't under-test.** If you changed a conditional, test both branches. If you added error handling, test the error path. "Happy path only" is not adequate coverage.
- **Each test should test one thing.** If a test name needs "and" in it, split it into two tests.
- **Tests must be deterministic.** No reliance on timing, ordering, or random data without seeds.
