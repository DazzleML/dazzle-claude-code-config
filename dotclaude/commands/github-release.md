---
description: Create git tag and GitHub release with standardized notes — draft to file, review, sign-off, publish
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

Create a GitHub release following the structured approach: gather context → detect version → draft release notes to file → present for review → sign-off → tag + push + publish

Arguments: "$ARGUMENTS" (optional - version tag like "v0.2.1-alpha", or leave empty for auto-detection)

---

## Process Steps:

### 1. **Gather Context**

Collect all information needed to draft release notes. Run these in parallel:

```bash
# Current version from version files
# Check: _version.py, version.py, package.json, pyproject.toml, Cargo.toml
```

```bash
# Existing tags and releases
git tag -l --sort=-version:refname
gh release list --limit 10
```

```bash
# CHANGELOG for this version's entry
# Read CHANGELOG.md or CHANGES.md
```

```bash
# Commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~10")..HEAD --oneline
```

```bash
# Repository info
gh repo view --json nameWithOwner,description -q '.nameWithOwner + " | " + .description'
```

### 2. **Detect Version**

If version not provided in arguments:
- Read from version file (_version.py, package.json, etc.)
- Construct tag name: `v{MAJOR}.{MINOR}.{PATCH}` with phase suffix if applicable (e.g., `v0.2.1-alpha`)
- Confirm the tag doesn't already exist

If version IS provided in arguments, use it directly.

### 3. **Detect Prerelease**

Check if the version contains a prerelease indicator:
- `alpha`, `beta`, `rc`, `dev` → use `--prerelease` flag on release
- No indicator → stable release (no `--prerelease`)

### 4. **Draft Release Notes**

Write release notes to `./private/claude/releases/release_{tag}.md` (create `releases/` directory if needed).

Follow this template structure:

```markdown
## [Project Name] [tag]

[1-2 sentence project description — what it does, main value proposition]

### What's New in [tag]

#### [Feature/Change Category] (#issue)

[Description of what changed and why it matters. Include code examples
for new commands/features/CLI flags.]

#### [Next Category] (#issue)

[Description]

### Installation

[Project-specific install instructions — pip, npm, cargo, etc.]

### Version History ([major.minor].x)

| Version | Key Change |
|---------|------------|
| [vX.Y.Z](release-link) | Current — description |
| [vX.Y.Y](release-link) | Previous — description |
| [vX.Y.0](release-link) | Initial — description |

### Platform Support

| Platform | Status |
|----------|--------|
| Platform 1 | Tested |
| Platform 2 | Expected to work |

### Requirements

[If applicable — language version, dependencies, etc.]
```

**Template rules:**
- **Version History** is reverse-sorted (newest first), links to GitHub release tags
- **Scope to current minor version** series (e.g., all v0.2.x releases)
- **Group changes by theme** with issue references (#N)
- **Include code examples** for new commands/features
- **Note platform testing status honestly** (tested vs expected to work)
- Versions without a GitHub release link get no link (just the version number)

### 5. **Derive Release Title**

Format: `{tag} - {Short Theme Description}`

Examples:
- `v0.2.1-alpha - Suspicious-Only Default, Auto-Trust & LOLBin Exclusion`
- `v1.0.0 - Stable Release with Cross-Platform Support`
- `v0.3.0-beta - Real-Time Monitoring and Process Ancestry`

### 6. **Present for Review**

Show the release details in the conversation:
- **Tag**: the tag name
- **Title**: the release title
- **Prerelease**: yes/no
- **Release notes**: displayed inline (full markdown)
- **File path**: so the user can edit the notes directly before publishing

Wait for explicit user sign-off before proceeding.

### 7. **Publish (After Sign-off)**

Only after explicit user approval:

```bash
# Create and push signed tag (if it doesn't exist yet)
# Note: tag.gpgsign=true is set globally, so -a auto-signs.
# Use -s explicitly if gpgsign is not configured.
git tag -a {tag} -m "{tag}: {short description of release}"
git push origin {tag}

# Create GitHub release using the file
gh release create {tag} \
  --title "{title}" \
  --notes-file {path-to-release-file} \
  {--prerelease if applicable}
```

### 8. **Confirm**

Show the release URL and remind the user about any CI/CD workflows that may trigger (e.g., PyPI publish on release event).

**If the project has a `private/` nested repo**, you may sync the release-notes draft into it via a local commit (`cd private && git add -A && git commit -m "sync: add {tag} release notes" && cd ..`). **NEVER push the `private/` repo** — it is local-only by design. Do not include private-repo push reminders in the confirmation summary.

---

**CRITICAL SAFETY RULES:**

- **NEVER create a tag or release without explicit user sign-off**
- Always present the full release notes for review first
- Save the release notes file BEFORE publishing (user may want to edit)
- Check for existing tags before creating — never overwrite
- Use `--notes-file` (or `-F`) not inline `--notes` to avoid shell escaping issues
- Detect prerelease status from version string automatically
- User handles any force-push or tag deletion if needed

**Example Usage:**
- `/github-release` — Auto-detect version, draft and publish
- `/github-release v0.2.1-alpha` — Release a specific version
- `/github-release v1.0.0 First stable release` — Version with theme hint
