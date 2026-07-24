# Release Notes Generator

Generate GitHub release notes following DazzleML's standard format.

## Usage

```
/release-notes [version]
```

## Instructions

Generate release notes for the specified version (or detect from version files if not provided). Follow this template structure:

### Template Structure

```markdown
## [Project Name] v[X.Y.Z]

[1-2 sentence description of what the project does and its main value proposition]

### What's New in v[X.Y.Z]: [Brief Theme]

[1-2 sentence summary of this release's focus]

#### [Feature/Fix Category 1]

[Details with code examples if applicable]

#### [Feature/Fix Category 2]

[Details]

### Core Features (v[X.Y].x)

| Feature | Description |
|---------|-------------|
| Feature 1 | Brief description |
| Feature 2 | Brief description |

### Version History (v[X.Y].x)

| Version | Key Change |
|---------|------------|
| [vX.Y.Z](link) | Most recent - description |
| [vX.Y.Y](link) | Previous - description |
| [vX.Y.0](link) | Initial X.Y - description |

### Platform Support (if applicable)

| Platform | Status |
|----------|--------|
| Platform 1 | Tested / Expected to work |
```

### Key Principles

1. **Version History is reverse-sorted** (newest first)
2. **Link version numbers** to their GitHub release tags
3. **Group changes by theme** (features, fixes, docs, etc.)
4. **Include code examples** for new commands/features
5. **Note testing status** honestly (tested vs expected to work)
6. **Keep the X.Y scope** - version history shows all releases in current minor version series

### Steps to Generate

1. Read CHANGELOG.md for recent changes
2. Read version.py or package.json for current version
3. Check git log for commits since last tag
4. Identify the theme/focus of this release
5. Generate release notes following the template
6. Output the markdown for review before creating the release

### Creating the Release

After user approves the notes:

```bash
# Write notes to temp file
# Create tag if needed: git tag -a vX.Y.Z -m "vX.Y.Z: [brief description]"
# Push tag: git push origin vX.Y.Z
# Create release: gh release create vX.Y.Z --title "vX.Y.Z - [Theme]" -F notes.md
```
