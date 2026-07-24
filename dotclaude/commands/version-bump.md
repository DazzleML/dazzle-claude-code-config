---
description: Analyze what version change to make and apply it. Encodes project versioning philosophy and PEP 440 mapping.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Version Bump Advisor

Analyze the current state, recommend the correct version change, and apply it.

**Arguments:** "$ARGUMENTS"

Expected format: `[description of what changed]` or `[major|minor|patch|pre] [description]`
- If a bump level is specified, validate it against the rules below
- If only a description is given, recommend the correct level

---

## Versioning Philosophy

### Core Principles

| Component | Meaning | When to bump |
|-----------|---------|-------------|
| **MAJOR** | Paradigm shift or breaking API change | Fundamentally different tool, incompatible changes |
| **MINOR** | A whole new big feature set | New capability area (e.g., "history support", "plugin system") |
| **PATCH** | Iteration toward completing the minor | Feature additions within the current minor's scope |
| **PHASE** | Stability indicator for a MAJOR.MINOR.PATCH | Alpha → Beta → RC → Stable (drops when feature set is complete) |
| **PRE_RELEASE_NUM** | Iteration within a phase | Multiple alphas of the same patch before stabilizing |

### The Version Ladder

```
0.2.0a1  →  Minor 2 begins: initial feature set (alpha quality)
0.2.0a2  →  Fixes/polish to 0.2.0 (still alpha)
0.2.0    →  0.2.0 is stable
0.2.1a1  →  New feature added within minor 2's scope
0.2.1a2  →  Iteration on 0.2.1
0.2.1    →  0.2.1 is stable
0.3.0a1  →  Minor 3 begins: whole new feature set
1.0.0    →  First stable major release
```

### Decision Matrix

| What changed? | Bump | Example |
|---------------|------|---------|
| New major capability area | MINOR | Adding clipboard history to a clipboard tool |
| New feature within current capability | PATCH | Adding OS auth to existing encryption |
| Bug fix or polish within current patch | PRE_RELEASE_NUM | Fixing DPAPI edge case in 0.2.1a1 → 0.2.1a2 |
| Breaking API or behavioral change | MAJOR | Removing `--encrypt` password mode entirely |
| Phase graduation (alpha → stable) | Drop PHASE | 0.2.1a3 → 0.2.1 (feature set proven stable) |

### Key Rules

1. **MINOR = new capability area**. Don't bump minor for adding features to an existing area.
2. **PATCH = iteration within the minor**. Each patch adds or improves features in the current minor's scope.
3. **PRE_RELEASE_NUM = iteration within a patch**. Multiple alphas before the patch stabilizes.
4. **Bumping PATCH resets PRE_RELEASE_NUM to 1**. (0.2.0a3 → 0.2.1a1)
5. **Bumping MINOR resets PATCH to 0 and PRE_RELEASE_NUM to 1**. (0.2.3 → 0.3.0a1)
6. **Dropping PHASE means "this patch is stable"**. Only drop when the feature set is proven.

### PEP 440 Mapping

| Internal | PEP 440 | Display |
|----------|---------|---------|
| `0.2.0` alpha pre=1 | `0.2.0a1` | `PREALPHA 0.2.0-alpha` |
| `0.2.1` alpha pre=2 | `0.2.1a2` | `PREALPHA 0.2.1-alpha` |
| `0.2.1` beta pre=1 | `0.2.1b1` | `PREALPHA 0.2.1-beta` |
| `0.2.1` (no phase) | `0.2.1` | `PREALPHA 0.2.1` |
| `1.0.0` (no phase, stable) | `1.0.0` | `1.0.0` |

---

## Process

### Step 1: Read Current Version

```
Read the project's _version.py (or equivalent) to get:
- MAJOR, MINOR, PATCH
- PHASE, PRE_RELEASE_NUM
- PROJECT_PHASE
- Current __version__ string
```

### Step 2: Understand What Changed

- Check `git diff` or `git log` since last tag/commit
- Identify the nature of changes using the decision matrix
- Consider: Is this a new capability area (MINOR) or iteration on existing (PATCH)?

### Step 3: Recommend the Bump

Present a clear recommendation:

```
Current:  0.2.0a1
Proposed: 0.2.1a1

Reason: Added OS session-based encryption — this is a new feature
within the existing encryption capability (PATCH), not a new
capability area (MINOR). First alpha of this patch (a1).

Changes to _version.py:
  PATCH: 0 → 1
  PRE_RELEASE_NUM: 1 (reset, since PATCH bumped)
```

### Step 4: Apply (After Approval)

Update `_version.py` (or equivalent version file) with the new values.

Verify with: `python -c "from module._version import *; print(PIP_VERSION)"`

Also update CHANGELOG.md if a new version section is needed.

---

## Quick Reference Card

```
"I added a bug fix to the current feature"     → bump PRE_RELEASE_NUM
"I added a new feature to the current scope"   → bump PATCH (reset pre to 1)
"I started a whole new feature area"            → bump MINOR (reset patch+pre)
"I broke backward compatibility"                → bump MAJOR (reset all)
"The current alpha is stable enough to release" → drop PHASE
```

---

## Examples

```
/version-bump Added OS session auth to encryption
  → Recommend: PATCH bump (0.2.0a1 → 0.2.1a1)

/version-bump Fixed DPAPI edge case on Windows
  → Recommend: PRE_RELEASE_NUM bump (0.2.1a1 → 0.2.1a2)

/version-bump Added plugin system for custom backends
  → Recommend: MINOR bump (0.2.1 → 0.3.0a1)

/version-bump patch Completed config wizard
  → Validate: PATCH is correct, apply it

/version-bump The encryption feature set is solid, ready to release
  → Recommend: Drop PHASE (0.2.1a3 → 0.2.1)
```
