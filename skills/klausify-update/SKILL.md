---
name: klausify-update
description: Use when the user wants to refresh klausify-generated boilerplate (skills, settings, hooks, CLAUDE.md) after upgrading klausify itself. Re-runs the scaffold against the latest templates so this repo picks up new skills, prompt revisions, and convention rules.
argument-hint: "[--skip-enrich]"
allowed-tools: Read Bash(pipx *) Bash(klausify *) Bash(pip *) Bash(git *)
---

# Klausify update

Refresh this repository's klausify-generated boilerplate to match the latest klausify version.

## Steps

1. **Upgrade klausify first.** Run `pipx upgrade klausify` (or `pip install --user --upgrade klausify` if klausify wasn't installed via pipx). Verify the new version with `klausify --version`. Note the version for the report at the end.

2. **Read the existing version marker.** `cat .claude/skills/.klausify-version` captures the version that last generated the skills. If the new klausify version is the same as the marker, klausify will skip — surface that to the user and confirm they want to proceed anyway (rare; usually only useful if you've also bumped `conventions-cli` and want to re-run the path-scoped CLAUDE.md emission).

3. **Detect the base branch** the same way `klausify-init` does (`git branch --list dev develop main master | head -1`).

4. **Run `klausify init --force`.** The `--force` flag overrides the version-skip check and rewrites all generated files with the new templates:
   ```
   klausify init --force --base-branch <detected> $ARGUMENTS
   ```

5. **Diff the result.** Run `git diff CLAUDE.md .claude/` and summarize the substantive changes for the user:
   - New skills added or removed
   - Prompt body changes in `<repo>-plan` / `<repo>-review` / etc.
   - New / changed rule files under `.claude/rules/`
   - Settings or hook changes
   This is the user's chance to review before committing the refresh.

6. **Report.** Tell the user the old marker version → new version, what materially changed in the generated content, and remind them to commit.

## When NOT to use

- The repo isn't klausified yet — use the `klausify-init` skill instead (running `klausify init --force` on a clean repo works but the skill auto-detect is cleaner).
- The user only wants to update one specific surface (just skills, just hooks, just settings) — they can run `klausify skills`, `klausify hooks`, or `klausify settings` directly without `init --force`.
- The user pinned an older klausify version intentionally and doesn't want to upgrade — skip step 1 and re-run `klausify init --force` against the existing version, but flag that this is unusual.
