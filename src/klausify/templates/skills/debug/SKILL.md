---
name: {{REPO}}-debug
description: Use when the user reports an error, bug, or unexpected behavior in this repo and wants help diagnosing it. Five phases — reproduce, diagnose root cause (read-only), write a failing test, fix, verify against the full suite.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

Debug the error or issue the user described. Do NOT jump to a fix. Follow these phases in order.

---

## Phase 1: Reproduce and Understand

1. **Read CLAUDE.md** for project structure, test commands, and known pitfalls.
2. **Understand the failure.** What exactly is going wrong? Read the error message, stack trace, or described behavior carefully. Identify:
   - What is the expected behavior?
   - What is the actual behavior?
   - When did it start? Run `git log --oneline -10` to check for recent changes that could be the cause.
3. **Reproduce it.** If there's a test command or way to trigger the bug, run it now. If you can't reproduce it, say so before proceeding — a fix you can't verify is a guess.

---

## Phase 2: Diagnose

Do NOT write any fix yet. Investigate read-only until you understand the root cause.

1. **Find the code path.** Starting from the error location or the described behavior, trace the execution:
   - Grep for the error message, function name, or component.
   - Read the file where the failure occurs — the full file, not just the function.
   - Trace backwards: what calls this code? What data does it receive?
2. **Find the actual data source.** If the bug involves wrong values, read the query or data access that produces them. Do not assume — read the actual code.
3. **Identify the root cause.** Ask yourself:
   - Is this a logic error, a data error, or a state error?
   - Is this a regression from a recent change? Check `git diff` and `git log`.
   - Could this be caused by something upstream of where the error appears?

**State your diagnosis before proceeding.** Explain:
- Where the bug is (file and function).
- Why it happens (the root cause, not the symptom).
- What the fix should be.

If you are not confident in the diagnosis, say so and explain what's uncertain. Do not guess and code.

---

## Phase 3: Write a Failing Test

Before writing the fix, write a test that captures the bug:

1. Find existing tests for the module — match their patterns, fixtures, and style.
2. Write a test that reproduces the buggy behavior. It should fail right now for the same reason the bug occurs.
3. Run it to confirm it fails for the right reason. If it passes, your test doesn't capture the bug — fix the test first.

If the bug is not practically testable (e.g., a pure environment/config issue), skip this step and note why.

---

## Phase 4: Fix

Now implement the fix.

1. **Fix the root cause, not the symptom.** If the real problem is upstream, fix it upstream — don't add a bandaid where the error surfaces.
2. **Make the minimal change.** Don't refactor, rename, or "clean up" surrounding code. The fix should be as small and targeted as possible.
3. **Check for other callers.** If you changed a function's behavior, grep for other callers and verify they still work correctly.
4. **Re-read the file** after editing to verify the fix looks correct in context.

---

## Phase 5: Verify

1. **Run your failing test** — it should pass now. If it doesn't, your fix is wrong. Go back to Phase 2.
2. **Run the full test suite.** If other tests break, your fix caused a regression. Do not patch the other tests to make them pass — re-examine your fix.
3. **Run linters/formatters** if available.
4. **Check your diff.** Run `git diff` and verify every changed line is necessary for the fix. Remove anything unrelated.

---

## Rules

- Do NOT apply a fix before you can explain the root cause.
- Do NOT change unrelated code.
- Do NOT use defensive hacks like `|| 0`, `try/catch` wrappers, or null coalescing to mask the real problem.
- If the fix touches a hot path, consider performance implications.
- If you find the bug is a duplicate of a known pitfall from CLAUDE.md, mention it.
