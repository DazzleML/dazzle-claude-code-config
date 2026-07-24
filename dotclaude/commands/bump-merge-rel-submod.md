---
description: Extended workflow for projects with git submodules (version bump, merge, submodule update, parent release)
allowed-tools: Bash, Read, Edit, Write
---

Execute the extended release workflow for a parent project that includes submodules.

**Project Context:** "$ARGUMENTS"

**Example**: DazzleNodes project with smart-resolution-calc submodule

## Workflow Overview

This workflow extends `bump-merge-release` with additional steps for updating the parent repository that contains the submodule.

## Phase 1-3: Complete Submodule Release

Follow **ALL steps** from `bump-merge-release.md` command first:
1. ✅ Update submodule CHANGELOG/README
2. ✅ Bump submodule version.py and pyproject.toml
3. ✅ Merge submodule dev→main
4. ✅ Push submodule to GitHub
5. ✅ Create submodule tag and release

**Checkpoint**: Submodule release is now live on GitHub

---

## Phase 4: Update Parent Repository Submodule

### Navigate to Parent Local Directory

```bash
cd <CODE_ROOT>/[parent-project]/local
```

Example: `cd <CODE_ROOT>/DazzleNodes/local`

### Update Submodule to Latest

1. **Navigate to submodule directory**
   ```bash
   cd nodes/[submodule-name]
   git fetch origin
   git checkout main
   git pull origin main
   ```

2. **Return to parent directory**
   ```bash
   cd ../..  # Back to parent root
   ```

3. **Stage submodule update**
   ```bash
   git add nodes/[submodule-name]
   git status  # Should show submodule updated to new commit
   ```

### Update Parent Version

4. **Bump Parent version.py**
   - **Patch bump ONLY** (unless adding new node or major parent feature)
   - Rationale: Submodule updates are minor changes to parent package
   - Only bump MINOR/MAJOR if:
     - Adding new node to parent
     - Major parent-level feature changes
     - Breaking changes in parent structure

5. **Update Parent pyproject.toml**
   - Match version from version.py
   - Update any submodule-related dependencies if needed

### Update Parent Documentation

6. **Update Parent CHANGELOG.md**
   - Add entry for new parent version
   - Format:
     ```markdown
     ## [X.Y.Z] - YYYY-MM-DD

     ### Changed
     - **[Submodule Name] Updated** - Updated to vX.Y.Z
       - [List key submodule changes that affect parent usage]
       - See [submodule changelog](link) for full details
     ```

7. **Update Parent README.md** (if needed)
   - Update version badges
   - Update feature descriptions if submodule added major features
   - Update installation instructions if submodule requirements changed

### Commit Parent Changes

8. **Commit to parent dev branch**
   ```bash
   git add .
   git commit -m "Update [submodule] to vX.Y.Z and bump parent to vX.Y.Z"
   ```

---

## Phase 5: Parent Merge to Main

Follow merge steps from `bump-merge-release` for parent repo:

9. **Switch to parent GitHub directory**
   ```bash
   cd <CODE_ROOT>/[parent-project]/github
   git restore version.py
   ```

10. **Merge parent dev to main**
    ```bash
    git merge dev --no-ff --no-edit
    ```

11. **Resolve conflicts and commit**
    - Message: "Merge dev to main: Release vX.Y.Z with [submodule] vX.Y.Z update"

12. **Push to GitHub**
    ```bash
    git push origin main
    ```

---

## Phase 6: Parent Release Publishing

13. **Create parent tag**
    ```bash
    git tag -a vX.Y.Z -m "Release vX.Y.Z: Updated [submodule] to vX.Y.Z"
    git push origin vX.Y.Z
    ```

14. **Create parent GitHub release**
    ```bash
    gh release create vX.Y.Z --title "vX.Y.Z - [Submodule] Update" --notes "[Release notes]"
    ```

    **Parent Release Notes Structure:**
    ```markdown
    ## [Submodule Name] Update to vX.Y.Z

    Updated [submodule-name] submodule to vX.Y.Z with [primary features].

    ### Key Changes from Submodule
    - [Feature 1]
    - [Feature 2]
    - [Bug fix 1]

    See the full [submodule-name] changelog:
    https://github.com/[org]/[submodule-repo]/releases/tag/vX.Y.Z

    ## Installation

    [Standard installation instructions]

    ## Upgrading

    [Standard upgrade instructions]
    ```

---

## Key Differences from Standard Workflow

**Submodule-Specific:**
- Parent version bumps are typically **PATCH only** (X.Y.Z → X.Y.Z+1)
- Parent CHANGELOG focuses on submodule update impact
- Parent release notes link to submodule release for details
- Submodule update must be staged as a commit in parent repo

**Version Bump Rules:**
- Submodule bug fix → Parent PATCH bump
- Submodule new feature → Parent PATCH bump (unless affects parent API)
- New node added to parent → Parent MINOR bump
- Parent structure changes → Parent MINOR/MAJOR bump as appropriate

**Testing:**
- Test parent functionality with updated submodule before releasing
- Verify submodule integration points work correctly
- Check that parent builds/installs correctly with new submodule version

---

## Example: DazzleNodes + Smart Resolution Calc

```bash
# Phase 4: Update submodule
cd <CODE_ROOT>/DazzleNodes/local/nodes/smart-resolution-calc
git fetch && git checkout main && git pull
cd ../..

# Stage submodule update
git add nodes/smart-resolution-calc

# Bump DazzleNodes version (patch only)
# version.py: PATCH = X+1
# pyproject.toml: version = "X.Y.Z"

# Update DazzleNodes CHANGELOG.md
# Commit
git commit -m "Update smart-resolution-calc to v0.6.5 and bump DazzleNodes to vX.Y.Z"

# Phase 5-6: Merge and release DazzleNodes
cd <CODE_ROOT>/DazzleNodes/github
git restore version.py
git merge dev --no-ff
# Resolve conflicts, push, tag, release
```

---

## Troubleshooting

**Submodule not updating:**
- Check submodule remote: `git remote -v` (inside submodule dir)
- Ensure submodule tracking correct branch: `git branch -vv`
- Try: `git submodule update --remote --merge`

**Parent build fails:**
- Verify submodule version compatibility
- Check submodule dependencies in parent pyproject.toml
- Ensure submodule files accessible to parent build process

**Merge conflicts:**
- Expected in version.py (branch name differences)
- Unexpected conflicts may indicate concurrent development
- Resolve carefully, preserving both branches' intent
