---
description: Obsidian knowledge vault — capture notes, synthesize connections, and build Maps of Content. Use proactively when discovering relationships, or invoke manually for targeted note capture and knowledge graph maintenance.
allowed-tools: Bash, Write, Read, Glob, Grep, Edit, Task, AskUserQuestion, WebSearch, WebFetch
---

# Obsidian — Knowledge Vault Management

## Context: "$ARGUMENTS"

## Overview

This skill manages the project's Obsidian knowledge vault at `./private/claude/`. It operates in two modes:

1. **With arguments**: Capture a note (user text verbatim + Claude synthesis)
2. **Without arguments**: Synthesis mode — read MOCs, discover connections, update knowledge structure

## Process

### 1. Determine Mode & Context

```bash
TIMESTAMP=$(date +%Y-%m-%d__%H-%M-%S)
```

Identify the working context:
- **Project root**: Check for `.git`, `CLAUDE.md` to locate the project
- **Vault location**: `./private/claude/` (the Obsidian vault root)
- **Existing MOCs**: Read `_maps/` files to understand current knowledge graph
- **Recent notes**: Check `notes/` for recent activity

### 2. Mode A — Note Capture (when arguments provided)

When the user provides text via `/obsidian <text>`:

**2a. Record the user's words verbatim**

Create a new note file:
- **Location**: `./private/claude/notes/` (or appropriate subfolder based on topic)
- **Filename**: `YYYY-MM-DD__HH-MM-SS__both_<short-slug>.md`

**2b. Structure the note**

```markdown
---
type: note
date: YYYY-MM-DD
initiator: user
author: both
also-in: []
tags:
  - by/both
---

# <Title derived from content>

## User's Note

> <User's exact text, verbatim, in blockquote>

## Synthesis

<Claude's analysis: connections to existing knowledge, related documents, implications>

## Related

- [[relevant MOC or document links]]
```

**2c. Cross-reference**

- Scan the note text for references to GitHub issues (e.g., "#56", "Issue 23")
- For referenced issues: check if a local file exists in `issues/`. If not, create an auto-generated stub (see Issue Stub Generation in oracle skill) so wikilinks resolve
- Scan for references to known concepts (stf, primes, Lean, parser, etc.)
- Add wikilinks `[[document|display text]]` only where the target file exists — never create wikilinks to non-existent files
- Add `also-in:` paths if the note belongs in multiple topic areas
- Update relevant MOC files if a significant new connection is discovered

### 3. Mode B — Synthesis (no arguments)

When invoked as bare `/obsidian`:

**3a. Survey the landscape**

- Read all MOC files in `_maps/`
- Read recent notes in `notes/` (last 5-10 by timestamp)
- Check git log for recent commits and what changed
- Check for any new documents in the vault since last synthesis

**3b. Identify gaps and connections**

- Are there documents not linked from any MOC?
- Are there cross-cutting themes that deserve a new note?
- Do any existing notes need updated `also-in` or tag metadata?
- Are there new GitHub issues or closed issues that should be reflected?

**3c. Create or update structural documents**

- Create new notes for discovered connections
- Update MOCs with new links
- Create new MOCs if a topic cluster has grown large enough
- All new files use `initiator: claude, author: claude`

**3d. Report what was done**

Summarize to the user:
- What connections were discovered
- What notes/MOCs were created or updated
- What gaps remain

### 4. Proactive Use (Claude's Initiative)

Claude SHOULD use this skill proactively (without user invocation) when:
- A relationship between ideas is discovered during normal work
- A dev-workflow or postmortem reveals connections to prior work
- A GitHub issue's context illuminates patterns in the knowledge base
- A debugging session uncovers reusable insights

For proactive notes, use `initiator: claude, author: claude` and place in appropriate `notes/` subfolder.

### 5. Note Organization Rules

**Subfolder structure** in `notes/` (create as needed):
- `notes/math/` — Mathematical observations (stf, primes, number theory)
- `notes/lean/` — Lean 4 proof patterns, tactic discoveries
- `notes/cli/` — Parser, grammar, CLI design observations
- `notes/ideas/` — Cross-cutting ideas, future possibilities
- `notes/meta/` — Project health, process observations

**Tagging conventions**:

| Category | Format | Examples |
|----------|--------|---------|
| Authorship | `#by/claude`, `#by/user`, `#by/both` | Who wrote it |
| Status | `#wip`, `#draft`, `#stable`, `#archived` | Lifecycle |
| Lock | `#user-wip` | User is working — don't touch |
| Type | `#note`, `#moc`, `#observation`, `#connection` | What kind |
| Topic | `#yourtopic`, `#lean`, `#cli`, `#parser`, `#primes` | Subject |
| Cross-ref | `#issue/56`, `#version/v0.8.2` | Links |

**Content immutability rule**: When linking FROM existing dev-workflows, postmortems, or discussions, ONLY add:
- YAML frontmatter (top of file)
- Addendum sections (bottom of file)
- `## Related` section (bottom of file)
- NEVER alter existing body content

## Notes

- The `notes/` folder is Claude's primary workspace — Claude creates, edits, and reorganizes freely
- User can tag any note `#user-wip` to claim it (Claude leaves it alone)
- Always use `/dev/null` not `nul` for any shell redirection (Windows/WSL compatibility)
- YAML frontmatter includes `also-in:` for virtual multi-folder membership
- Wikilinks use aliases for readability: `[[long-timestamp-filename|Short Label]]`
