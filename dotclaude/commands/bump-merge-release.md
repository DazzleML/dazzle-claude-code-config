---
description: Standard workflow for version bump, dev→main merge, and GitHub release
allowed-tools: Bash, Read, Edit, Write
---

Execute the standard release workflow for a single-repository project.

**Project Context:** "$ARGUMENTS"

## Workflow Steps

### Phase 1: Preparation & Version Bump (Dev Branch)

1. **Review Changes**
   - Run `git status` and `git log` to review commits since last release
   - Verify all fixes/features are committed to dev branch
   - Check that tests pass and code is ready for release

2. **Update Documentation**
   - **CHANGELOG.md**: Add new version entry with:
     - Fixed/Added/Changed sections
     - Technical details
     - Benefits
     - Related issues/documents
   - **README.md**: Update if features/usage changed
   - Check other docs that may need updates

3. **Bump Version Numbers**
   - **version.py**: Increment PATCH (bug fixes) or MINOR (new features) or MAJOR (breaking changes)
   - **pyproject.toml**: Update version to match
   - Commit: "Bump version to X.Y.Z for [brief description]"

### Phase 2: Merge to Main

4. **Switch to GitHub Directory**
   ```bash
   cd <CODE_ROOT>/[project-name]/github
   git status
   ```

5. **Restore version.py** (avoid merge conflicts)
   ```bash
   git restore version.py
   ```

6. **Merge Dev to Main** (no fast-forward)
   ```bash
   git merge dev --no-ff --no-edit
   ```

7. **Resolve version.py Conflict**
   - Edit version.py to accept dev version
   - Stage: `git add version.py`
   - Complete merge: `git commit` with message describing the release
   - Format: "Merge dev to main: Release vX.Y.Z with [features]"

8. **Push to GitHub**
   ```bash
   git push origin main
   ```

### Phase 3: Release Publishing

9. **Create Git Tag**
   ```bash
   git tag -a vX.Y.Z -m "Release vX.Y.Z: [brief description]"
   git push origin vX.Y.Z
   ```

10. **Create GitHub Release**
    ```bash
    gh release create vX.Y.Z --title "vX.Y.Z - [Title]" --notes "[Release notes]"
    ```

    **Release Notes Structure:**
    - Lead with primary feature/purpose
    - List bug fixes with before/after
    - Technical changes section
    - Benefits list (✅ format)
    - Installation/upgrade instructions
    - Link to full changelog

### Key Reminders

- **No emojis in headers** (keep professional tone)
- **No excessive praise** (avoid "comprehensive", "critical" unless truly applicable)
- **Git hooks will update version.py** automatically on commit (branch name changes)
- **version.py conflict is expected** during merge (dev vs main branch names)
- **Match previous release style** when writing notes (check with `gh release view`)

### Example Merge Commit Message

```
Merge dev to main: Release vX.Y.Z with [primary feature]

This merge brings N releases from dev branch to main:

## vX.Y.Z - [Current Version]
- [Primary features/fixes]

## vX.Y.Z-1 - [Previous Version]
- [Features/fixes from previous release in this batch]

All changes tested and documented. Ready for production release.
```

### Example Tag Message

```
Release vX.Y.Z: [primary feature/focus] + [secondary improvements]
```

**Project-Specific Notes:**
- Adjust paths based on project structure
- Some projects use `local/` directory for development
- Verify branch names (dev/main vs master/develop)
- Check if project has additional deployment steps
