Create a new git worktree for the task described below.

1. Read CLAUDE.md to understand the project structure and branching conventions.
2. Create a short, descriptive branch name based on the task (e.g. `fix/login-redirect`, `feat/add-search`).
3. Run `git worktree add ../$(basename $PWD)-<branch-name> -b <branch-name>` to create the worktree.
4. Confirm the worktree was created successfully with `git worktree list`.
5. Tell the user the full path to the new worktree so they can open it.

Rules:
- Always branch from {{BASE_BRANCH}} unless told otherwise.
- Use lowercase kebab-case for branch names.
- Prefix with `fix/`, `feat/`, `chore/`, `docs/`, or `refactor/` as appropriate.
- Do not start work in the worktree — just create it and report the path.

$ARGUMENTS
