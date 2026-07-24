---
description: Memory-based postmortem for low-context situations (<6% remaining). Skips git diff/status gathering, works from conversation memory, designed for speed.
allowed-tools: Bash, Write, Read
---

# Full Postmortem (Lean) — Memory-Based

**Purpose**: Document session work when context is critically low (<6% remaining). Works entirely from conversation memory — no git diff, no file reads, no exploratory commands. Get straight to writing.

## When to Use

- Context window at <6% (compaction imminent)
- You need to capture session state before it's lost
- Standard `/fullpostmortem` would waste remaining tokens on git commands

## Process

Based on: "$ARGUMENTS"

### 1. Generate Timestamp (only command needed)

```bash
TIMESTAMP=$(date +%Y-%m-%d__%H-%M-%S)
```

### 2. Write Directly from Memory

**Do NOT run**: `git status`, `git diff`, `git log`, `git diff --name-only`, or any exploratory `Read`/`Grep`/`Glob` commands. Work entirely from what you remember from the conversation.

Write the postmortem immediately using the standard template sections but with these adaptations:

| Standard Section | Lean Adaptation |
|-----------------|-----------------|
| Problem Statement | From memory — user's request and context |
| What Was Done | Summarize from memory — files created/modified, key changes |
| Issues Encountered | From memory — problems hit and how they were resolved |
| Testing & Validation | From memory — test counts, what was verified |
| Lessons Learned | From memory — what went well, what to improve |
| Current State | From memory — what's committed vs uncommitted, what's next |
| Reference | Key files, commands, document paths from memory |

### 3. Add Review Flag

Include this note at the top of the postmortem (after YAML frontmatter):

```markdown
> **Note**: This postmortem was written from conversation memory at low context
> (<6% remaining). Review after compaction for accuracy — details may need
> correction against actual file state.
```

### 4. Save Location

Same rules as `/fullpostmortem`:
- **Project-specific**: `./private/claude/${TIMESTAMP}__lean-postmortem_(TOPIC).md`
- **General**: `~/claude/${TIMESTAMP}__lean-postmortem_(TOPIC).md`

## Key Rules

- **Speed over precision**: Approximate file lists and change descriptions are fine
- **No token-expensive operations**: Zero git commands beyond timestamp
- **Capture everything you remember**: Better to include uncertain details (flagged as such) than to lose them
- **Review after compact**: The postmortem can be refined in the next session after compaction restores context from the file itself
- **Same template structure**: Use the same YAML frontmatter and section headers as `/fullpostmortem` so postmortems are consistent regardless of method

## What This Captures That Would Otherwise Be Lost

- Session narrative (approaches tried, user feedback, course corrections)
- Intermediate failures and debugging steps
- User preferences and decisions expressed during the session
- Relationships between changes that aren't obvious from git diff alone
- "Why" context that git history doesn't preserve
