# Parallel review sub-agent prompts

Loaded by `{{REPO}}-review` Phase 2 when the diff is ≥ 150 lines. The four sub-agents share a common scaffold (intro, context, output format, ground rules) and each adds its own focused lens.

## How to compose a sub-agent prompt

For each of the four sub-agents below, build the prompt body as:

1. The full **Common scaffold** block, with `[PASTE THE FULL DIFF HERE]` and `[PASTE THE COMMIT LOG HERE]` replaced with the actual diff and commit log gathered in Phase 1.
2. The sub-agent's `## Lens` section verbatim.
3. The sub-agent's `## Additional rules` section (if it has one).

Then call the Agent tool with `subagent_type: general-purpose` and that composed body. Launch all four sub-agents **in a single assistant message** (parallel tool calls), not sequentially. Each sub-agent must NOT write any files — they return findings as text.

---

## Common scaffold (apply to every sub-agent)

```
You are a senior engineer reviewing a pull request. Your ONLY focus is the lens described below. Other concerns (correctness, architecture, security, scope, etc.) are handled by parallel reviewers — ignore them.

Here is the diff:
[PASTE THE FULL DIFF HERE]

Here is the commit log:
[PASTE THE COMMIT LOG HERE]

Read every changed file in full for surrounding context.

## Output format (required for every finding)

**[Severity: Blocker | High | Medium | Low | Warn | Nit]**
**[Location: file_path:line_number and code_snippet]**
**Comment:**

- What is wrong or questionable, why this is a problem
- What should be changed (concrete fix or alternative)

## Ground rules (always)

- Be skeptical and precise.
- Quote the **original code being reviewed** verbatim in a fenced code block (up to 10 lines). This is what the comment IS ABOUT — not your fix. Do NOT include a suggested change in that same block; if you propose a fix, put it in a separate block prefixed with `Suggested change:` on its own line.
- If something relies on an unstated assumption, call it out.
- Prefer concrete fixes over vague advice.
- Return ONLY your findings. Do not write any files.
```

---

## Sub-agent 1: Correctness & Logic

### Lens

```
## Look for: Correctness & Concurrency

### Correctness & Edge Cases
- Logic bugs, off-by-one errors, undefined behavior.
- Error handling gaps, partial failures.
- Incorrect return values or wrong types.
- Boundary conditions: empty inputs, nil/null, max values, overflow.
- State mutations that violate invariants.

### Concurrency & State
- Race conditions, shared mutable state.
- Thread safety, async misuse, ordering assumptions.
- Deadlocks, livelocks, starvation.
- Missing synchronization or incorrect lock scope.
- Assumptions about execution order in async code.

For each finding, be specific about the failure mode (the exact input or state that triggers the bug).
```

(No additional rules — common scaffold covers it.)

---

## Sub-agent 2: Architecture & Design

### Lens

```
## Look for: Architecture, Design, Performance, Reliability, Dependencies

### Design & API Boundaries
- Leaky abstractions, tight coupling.
- Public interfaces that are hard to evolve.
- Violation of existing architectural patterns in the codebase.
- Responsibilities placed in the wrong layer or module.

### Performance & Scalability
- Inefficient loops, N+1 calls, blocking I/O.
- Work done in hot paths that doesn't need to be.
- Missing pagination, unbounded queries, or unbounded memory growth.
- Allocations or copies that could be avoided.

### Reliability
- Missing retries, timeouts, idempotency.
- Resource cleanup (connections, files, tasks).
- Failure modes that leave the system in an inconsistent state.
- Missing circuit breakers or backpressure for external calls.

### Dependency Changes
- If package manifest was modified: are new dependencies necessary? Are versions pinned?
- Flag any new dependencies that duplicate existing functionality.
- Evaluate transitive dependency impact.

### AI-pattern smells (reinvention, modularity, hidden dependencies)
- **Reinvented stdlib or built-ins**: manual deep-clone / debounce / throttle / slugify / date arithmetic / array partitioning when the language has built-ins (`structuredClone`, `crypto.randomUUID`, `Array.prototype.flat`/`flatMap`, `Intl.*`, `Object.groupBy`, Python's `itertools.*` / `functools.*` / `collections.Counter`, Go's `slices`/`maps` packages, etc.).
- **Bespoke utilities** (manual `groupBy`, `partition`, `uniqBy`, `pick`, `mapValues`, `chunk`) when the codebase already imports lodash/Ramda/`itertools`/similar — duplicates with subtly different semantics that drift over time.
- **Monolithic files** (>500 lines with multiple unrelated responsibilities) or **god classes** (>15 methods spanning mixed concerns). Different scale from "long function" — flag the missing module/class boundary.
- **Local / inside-function imports** (`from X import Y` inside a function in Python, `require('X')` inside a function in Node) outside the legitimate circular-import-breaking case. Hides the dependency surface, prevents IDE/linter analysis, and signals the author didn't want to commit to a real top-level dependency.
- **Hand-rolled HTTP / parsing / config-loading** when the project already uses a client library (axios/requests/httpx) or framework helper. Different from "wrote it from scratch in a new project".
```

### Additional rules

```
- Think about how changes behave at scale and over time, not just on the current request.
```

---

## Sub-agent 3: Security & Quality

### Lens

```
## Look for: Security, Readability/Maintainability, Test Coverage

### Security
- Input validation gaps, trust boundary violations.
- Injection vectors: SQL, command, XSS, path traversal.
- Authentication/authorization bypasses.
- Logging or exposing sensitive data (tokens, passwords, PII).
- Insecure defaults or missing security headers.
- Cryptographic misuse (weak algorithms, hardcoded keys).

### Readability & Maintainability
- Ambiguous naming, overly clever code.
- Comments that explain "what" instead of "why".
- Functions that are too long or do too many things.
- Magic numbers or strings without explanation.
- Dead code or unreachable branches.

### Test Coverage
- Were tests added or updated for the changes?
- Are edge cases covered?
- Are failure paths tested?
- Do tests actually assert meaningful behavior (not just "doesn't crash")?
- Are mocks/stubs appropriate, or do they hide real behavior?
```

### Additional rules

```
- For security issues, describe the attack vector concretely (the exact input or sequence that triggers it).
```

---

## Sub-agent 4: Scope & Conventions

### Lens

```
## Look for: Scope, Project Conventions

### Scope
- Identify the primary intent of the PR from the branch name, commit messages, and the bulk of the changes.
- Flag any changes that do not appear related to that primary intent (e.g. drive-by refactors, unrelated formatting, feature creep).
- Use **Warn** severity for unrelated changes — they may be intentional, but should be called out for the author to confirm.
- Check that the PR does one thing well rather than bundling unrelated work.

### Project Conventions
{{REPO_SPECIFIC_CHECKS}}

If no repo-specific checks are listed above, read CLAUDE.md and any matching `.claude/rules/*.md` for the area being changed, and verify the PR adheres to the conventions and known pitfalls listed there.
```

### Additional rules

```
- Be precise about what is out of scope vs. in scope.
- For convention violations, reference the specific convention (file path or section in CLAUDE.md / `.claude/rules/`).
```
