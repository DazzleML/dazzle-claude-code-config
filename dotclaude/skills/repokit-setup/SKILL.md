---
name: repokit-setup
description: "Set up a new project using DazzleTools git-repokit-template and git-repokit-common. Creates repo, adds subtree, initializes standard structure."
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch, WebSearch
---

# RepoKit Project Setup

Full initialization of a new DazzleTools project from the git-repokit-template.

## User Input

- $ARGUMENTS: Project name, org (DazzleTools/djdarcy/DazzleNodes), description, and project type (python-pypi, python-comfyui, cpp, other).

## Process

### Step 1: Create GitHub Repo from Template

```bash
gh repo create <ORG>/<PROJECT_NAME> \
  --template DazzleTools/git-repokit-template \
  --public \
  --description "<description>"
```

The template auto-substitutes `$PROJECT_NAME`, `$PACKAGE_NAME`, `$GITHUB_ORG`, `$CLI_COMMAND` based on the repo name (via `.github/workflows/setup-from-template.yml`).

### Step 2: Clone Locally

If the target directory already exists with content (e.g., vendor/ source):
```bash
cd <CODE_ROOT>/<PROJECT_NAME>
git clone https://github.com/<ORG>/<PROJECT_NAME>.git /tmp/<project>-template
cp -r /tmp/<project>-template/.git .
cp -r /tmp/<project>-template/.github .
cp /tmp/<project>-template/.gitignore .
cp /tmp/<project>-template/LICENSE .
cp /tmp/<project>-template/.repokit.json .
git checkout -- CONTRIBUTING.md README.md docs/.gitkeep private/claude/.gitkeep \
  private/claude/commits/commit_v0.1.0_initial-template.txt \
  tests/conftest.py tests/one-offs/README.md tests/output/.gitkeep \
  pyproject.toml
```

If starting fresh:
```bash
git clone https://github.com/<ORG>/<PROJECT_NAME>.git <CODE_ROOT>/<PROJECT_NAME>
cd <CODE_ROOT>/<PROJECT_NAME>
```

### Step 3: Add git-repokit-common as Subtree

```bash
git subtree add --prefix=scripts https://github.com/DazzleTools/git-repokit-common.git main --squash
git remote add repokit-common https://github.com/DazzleTools/git-repokit-common.git
```

This populates `scripts/` with: `install-hooks.sh`, `paths.sh`, `sync-versions.py`, `update-version.sh`, `gh_issue_full.py`, `gh_sub_issues.py`, hooks, etc.

### Step 4: Install Git Hooks

```bash
bash scripts/install-hooks.sh
```

### Step 5: Customize for Project Type

**For Python (PyPI):**
- Edit `pyproject.toml` with project metadata
- Ensure `[tool.repokit-common]` section is configured

**For Python (ComfyUI):**
- Replace `pyproject.toml` with `scripts/pyproject.toml.comfyui` as starting point
- Add ComfyUI-specific fields

**For C++ (like Dazzle-Locate32):**
- The Python-specific template files need adaptation:
  - Remove or repurpose `<Package>/__init__.py`, `__main__.py`
  - Update `.gitignore` for C++ artifacts (*.obj, *.exe, *.pdb, *.lib, build dirs)
  - Replace `pyproject.toml` with a project metadata file or CMakeLists.txt
  - Update `tests/` structure for C++ testing
  - Keep `scripts/` subtree (hooks and tools are language-agnostic)
  - Keep `private/claude/` structure (design docs, postmortems)

### Step 6: Customize .gitignore

Add project-specific patterns under the `# Project Specific` section.

### Step 7: Initialize Standard Issues

Use `/github-issues-setup` to create:
- Issue #1: Roadmap (evergreen)
- Issue #2: Notes & Quick Ideas (evergreen)

### Step 8: Initial Commit

Stage the customized files and create the initial project commit. Do NOT commit until the user reviews and approves.

## Directory Structure (Final)

```
<PROJECT>/
  .git/
  .github/              # Issue templates, workflows, dependabot
  docs/
  private/
    claude/             # Design docs, postmortems, issue drafts (gitignored)
      issues/
      commits/
  scripts/              # git-repokit-common subtree
    hooks/
    install-hooks.sh
    paths.sh
    gh_issue_full.py
    ...
  tests/
    one-offs/           # Experimental scripts
    output/             # Test output (gitignored)
  src/ or <package>/    # Project source
  vendor/               # Third-party source (if applicable)
  .gitignore
  CONTRIBUTING.md
  LICENSE
  README.md
  pyproject.toml        # or CMakeLists.txt for C++
```

## Updating repokit-common Later

```bash
git subtree pull --prefix=scripts repokit-common main --squash
```

## Reference

- Template: https://github.com/DazzleTools/git-repokit-template
- Common scripts: https://github.com/DazzleTools/git-repokit-common
- First project using this: DazzleNodes/ComfyUI-DazzleKSampler
