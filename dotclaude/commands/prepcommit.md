---
description: Prepare for commit - version bump, update docs, verify tests, stage files, propose commit message
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

Prepare all changes for commit with proper version management and documentation updates.

**Arguments:** "$ARGUMENTS"

Expected format: `[major|minor|patch|none] [optional description]`
- `major` - Breaking changes (1.0.0 → 2.0.0)
- `minor` - New features (0.5.0 → 0.6.0)
- `patch` - Bug fixes (0.5.0 → 0.5.1)
- `none` - No version change needed

---

## Pre-Commit Preparation Workflow

### Phase 1: Understand Current State

1. **Check Git Status**
   - Run `git status` to see modified/untracked files
   - Run `git diff --stat` to summarize changes
   - Identify what type of changes we're dealing with

2. **Find ALL Version Locations**
   - Search for ALL files containing version strings. Projects often have multiple:
     - `VERSION` file (plain text)
     - `version.py` or `__version__` in main module
     - `pyproject.toml` under `[project]` or `[tool.poetry]`
     - `package.json` for Node.js projects
     - `setup.py` or `setup.cfg`
     - Registry-specific files (e.g., ComfyUI `pyproject.toml [tool.comfy]`)
     - Alias/forwarder packages in subdirectories (e.g., `packages/*/pyproject.toml`)
   - Run a RECURSIVE search -- do not just check root-level files:
     ```bash
     # Find all toml/json/cfg files that contain version strings
     grep -rn --include="*.toml" --include="*.json" --include="*.cfg" --include="*.py" "version" . 2>/dev/null | grep -i "[0-9]\.[0-9]" | grep -v __pycache__ | grep -v node_modules
     ```
   - Show ALL version strings found and flag any that are out of sync
   - Projects vary - some use one file, some use multiple that must stay in sync

### Phase 2: Version Bump (if requested)

3. **Bump Version in ALL locations**
   - If user specified major/minor/patch, update EVERY file that contains a version string
   - After updating, verify all version files agree (no mismatches)
   - If "none" specified, still check that existing versions are in sync and flag mismatches

### Phase 3: Update Documentation

4. **Update CHANGELOG.md**
   - Add new version section with today's date
   - Categorize changes: Added, Changed, Fixed, Removed, Deprecated
   - Reference any GitHub issues addressed
   - Keep entries concise but informative
   - **Verify CHANGELOG is current**: If a CHANGELOG.md exists, confirm it has an entry for the version being committed. Flag if the `[Unreleased]` section is empty or if the version section is missing.

5. **Update README.md** (if needed)
   - Update if features, usage, or installation changed
   - Update version badges if applicable
   - Check examples are still accurate

6. **Check Other Documentation**
   - Look for docs/, documentation in code comments
   - Update module/function docstrings if APIs changed
   - Check for outdated references

### Phase 4: Verify Testing

7. **Run Tests**
   - Look for test runner: run_tests.py, pytest, npm test, etc.
   - Execute test suite and verify all tests pass
   - Report any failures that need addressing before commit

### Phase 5: Stage Files

8. **Stage Appropriate Files**
   - Use `git add` for modified and new files
   - Respect .gitignore rules
   - Exclude:
     - Private/sensitive files (.env, credentials, settings with secrets)
     - Temporary files, caches, __pycache__
     - IDE-specific files unless project includes them
   - Show staged files summary

### Phase 6: Sync Private Repo (if applicable)

9. **Sync private/ nested repo**
   If the project has a `private/` nested git repo (check for `private/.git/`), stage and note it for sync after the parent commit:
   ```bash
   if [ -d "private/.git" ]; then
     echo "private/ nested repo detected -- will sync after parent commit"
     cd private && git status && cd ..
   fi
   ```
   - Do NOT commit the private repo yet -- that happens in `/commit` Step 8 after the parent commit
   - Flag any untracked files in private/ that should be added (design docs, issue drafts, commit messages)
   - **NEVER push the `private/` repo.** It is local-only by design. Do not include push reminders for it in summaries or hand-off messages.

### Phase 7: Hand Off to /commit

10. **Summarize and hand off**
   - Show all staged files and the version bump summary
   - Prompt the user to run `/commit` for the full commit workflow:
     git log convention analysis, GitHub issue references, design doc references,
     commit message written to file for editing, code review, and sign-off
   - Do NOT write a commit message or execute `git commit` -- that's `/commit`'s job
   - `/commit` will handle: git log convention analysis, commit message file, code review, sign-off, commit, AND private/ repo sync (Step 8)
   - Follow project's existing commit message style
   - NO attribution lines (no "Generated with Claude Code" or "Co-Authored-By")
   - Avoid inflated language ("comprehensive", "critical" unless truly warranted)

---

## Critical Rules

- **NEVER commit without explicit user approval**
- **NEVER include attribution or credits in commit messages**
- **NEVER commit sensitive files** (check .gitignore and use judgment)
- **ALWAYS run tests before staging** to catch issues early
- **ALWAYS show the full commit message** for user review
- **Version bump is user's decision** - they specify major/minor/patch/none

---

## Example Usage

```
/prepcommit patch Fix GPU overflow handling
/prepcommit minor Add new authentication system
/prepcommit none Update documentation only
/prepcommit major Breaking API changes for v2.0
```
