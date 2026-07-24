# RepoKit Post-Creation Setup

Perform post-creation setup for a new repokit Python project. This handles the recurring manual steps that repokit doesn't yet automate (tracked in DazzleTools/git-repokit issues #4, #5, #6).

## Context

The user has just run `repokit create <project-name>` and has a fresh project with the standard repokit structure (`local/` on private branch, `github/` worktree on main). This command streamlines the post-creation workflow.

## Arguments

- `$ARGUMENTS` — The project path or name (e.g., a full path or just `teeclip` to look under your code root)

## Steps

### 1. Locate & Validate Project

```
- Find the project directory (check $ARGUMENTS as path, or under your code root)
- Verify it's a repokit project (check for .repokit.json or local/ + github/ structure)
- Read .repokit.json to get project name, language, package structure
- Show the user what was detected and confirm before proceeding
```

### 2. Simplify Branch Structure

```
- Ask user: Keep github/ worktree or remove it?
  - If remove: delete the github/ worktree (`git worktree remove github`)
  - Switch local/ to main branch: `cd local && git checkout main`
  - This makes local/ the single working directory on main
- If keep: note that we'll set up private/ symlink later
```

### 3. Copy Versioning Scripts

```
- Source: [wingather](https://github.com/DazzleTools/wingather) `github/scripts/` (reference implementation)
- Target: <project>/local/scripts/ (or <project>/scripts/ if no local/)
- Copy these files:
  - scripts/update-version.sh
  - scripts/install-hooks.sh
  - scripts/paths.sh (if exists)
  - scripts/hooks/pre-commit
  - scripts/hooks/post-commit
  - scripts/hooks/pre-push
  - scripts/hooks/pre-commit-basic (if exists)
- Make all scripts executable: chmod +x scripts/*.sh scripts/hooks/*
```

### 4. Adapt Scripts to New Project

```
- In update-version.sh: Replace "wingather" references with the actual package name
  - SOURCE_FILE path: "wingather/_version.py" → "<package>/_version.py"
  - Title/banner text
- In install-hooks.sh: Replace "wingather" with project name in banners
- In pre-commit: Update any project-specific patterns if needed
- In paths.sh: Update paths for new project structure
```

### 5. Create Version File

```
- Detect the package directory (src/<package>/ or <package>/)
- Create <package>/_version.py with:
  - MAJOR = 0, MINOR = 1, PATCH = 0
  - PHASE = "alpha" (or ask user)
  - __version__ string
  - get_version(), get_base_version(), get_pip_version() helpers
  - PIP_VERSION for pyproject.toml dynamic versioning
- Update <package>/__init__.py to import from _version if needed
```

### 6. Install Git Hooks

```
- Run: bash scripts/install-hooks.sh
- Verify hooks were installed in .git/hooks/
- Run initial version update: bash scripts/update-version.sh
```

### 7. Create Private Structure

```
- Create private/claude/ directory
- Create private/claude/notes/ directory
- Create private/claude/_maps/ directory (for Obsidian vault)
- Add CLAUDE.md if not already present
```

### 8. DazzleTools Integration (Optional)

```
- Ask: Is this a DazzleTools project?
- If yes:
  - Create symlink in your tools directory pointing to the project
  - Verify the GitHub org remote is set to DazzleTools/
```

### 9. Summary

```
- Show what was done
- Show the project structure
- Remind about next steps:
  - Create GitHub repo if not done: gh repo create DazzleTools/<name> --public
  - Push initial commit
  - Update pyproject.toml entry points
  - Start implementing!
```

## Notes

- This command will eventually be unnecessary once repokit handles all these steps natively (issues #4, #5, #6)
- The [wingather](https://github.com/DazzleTools/wingather) `github/scripts/` are the canonical reference for the versioning system
- Always use `/dev/null` not `nul` for null redirection (WSL compatibility)
- On Windows, prefer junctions (PowerShell New-Item -ItemType Junction) over symlinks for private/ links (no admin needed)
- Ask for confirmation before destructive operations (removing worktrees, overwriting files)
