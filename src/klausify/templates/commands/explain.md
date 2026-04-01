Explain code changes or a specific concept in this project.

If no arguments are provided, explain the current diff:
1. Run `git diff {{BASE_BRANCH}}...HEAD` to see all changes on this branch.
2. If there are no committed changes, run `git diff` for unstaged and `git diff --cached` for staged changes.
3. Read the full files involved to understand the surrounding context.
4. Explain what changed and why, covering:
   - The purpose of the changes as a whole
   - How the modified components interact
   - Any non-obvious behavior or edge cases introduced

If arguments are provided, explain the specified code or concept:
1. Read CLAUDE.md to understand the project structure and conventions.
2. Find the relevant code using Grep and Glob.
3. Read the full files involved to understand context.
4. Trace the call chain and data flow end-to-end.
5. Explain how it works in plain language, covering:
   - What it does and why it exists
   - Key components and how they interact
   - Important design decisions or trade-offs
   - Any non-obvious behavior or edge cases

Rules:
- Tailor the depth to the question — a "what does this function do" needs less than "how does auth work".
- Use concrete examples from the code, not abstract descriptions.
- If something looks like a bug or smells off, mention it, but stay focused on explaining.
- Don't suggest changes unless asked.

$ARGUMENTS
