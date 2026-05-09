---
name: {{REPO}}-refactor
description: Use when the user wants to restructure code while preserving behavior exactly. Establishes a passing test baseline first, then makes incremental moves that each leave the suite green. Refuses to change behavior and structure in the same step.
allowed-tools: Read Grep Glob Bash Edit Write
---

Refactor the code the user described. The goal is to change structure while preserving behavior exactly. Do NOT change what the code does — only how it's organized.

---

## Phase 1: Establish the Safety Net

Before changing any code, confirm you have tests that cover the current behavior.

1. **Read CLAUDE.md** for project structure, test commands, and conventions.
2. **Run the existing test suite.** Record the results — every test must pass before you start. If tests are failing already, stop and report that. Do not refactor code that doesn't have a passing baseline.
3. **Assess coverage of the code you plan to change.** Read the existing tests for the modules involved. If a function you're restructuring has no tests:
   - Write tests for its current behavior first.
   - Run them to confirm they pass.
   - These are your regression guardrails — they prove the refactor didn't break anything.

---

## Phase 2: Understand the Current Code

Read the code you're refactoring in full. Understand:

1. **What it does** — the inputs, outputs, side effects, and edge cases.
2. **Who calls it** — grep for callers. Every caller is a contract you must preserve.
3. **What depends on its interface** — function signatures, return types, exceptions thrown, event emissions. These are the things you cannot change without updating all consumers.

---

## Phase 3: Plan the Refactor

Design the target structure before editing.

1. **Describe the structural change** — what moves where, what gets renamed, what gets split or merged.
2. **List what must NOT change** — public interfaces, return values, side effects, error behavior. Be explicit.
3. **Plan incremental steps.** Break the refactor into the smallest possible moves that each leave the code in a working state. Never change behavior and structure in the same step. For example:
   - Step 1: Extract a function (tests still pass).
   - Step 2: Move the function to a new module (tests still pass).
   - Step 3: Update callers to use the new location (tests still pass).

---

## Phase 4: Refactor

Execute your plan. After EACH incremental step:

1. **Run the test suite.** If anything fails, your last change broke something. Fix it before moving on — do not accumulate breakage across steps.
2. **Re-read the code** to verify it looks correct.

Rules:
- **Never change behavior and structure in the same step.** If you need to fix a bug you found, do it in a separate commit.
- **Preserve all public interfaces** unless the explicit goal is to change them. If you change a function signature, update every caller in the same step.
- **Don't "improve" things outside the refactor scope.** No drive-by style fixes, no adding types to unrelated code, no renaming things you aren't restructuring.
- **Match existing conventions.** If moving code to a new file, follow the naming and structure patterns already in the codebase.

---

## Phase 5: Verify

1. **Run the full test suite one final time.** Every test that passed before must pass now. No exceptions.
2. **Check your diff.** Run `git diff` and verify:
   - No behavioral changes snuck in.
   - No unrelated files were modified.
   - No debug code or commented-out code remains.
3. **Verify callers.** Re-grep for callers of anything you moved or renamed. Confirm every reference was updated.
