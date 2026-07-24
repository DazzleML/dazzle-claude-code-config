---
name: oracle
description: "Knowledge oracle — query the project's design docs, MOCs, postmortems, GitHub issues, and code to get traced, sourced answers. The entry point when you need to understand how anything in the project works or connects."
allowed-tools: Bash, Read, Glob, Grep, Edit, Task, AskUserQuestion, WebSearch, WebFetch
---

# Oracle — Project Knowledge Query

## Context: "$ARGUMENTS"

## Overview

The oracle is the **reader** of the project's knowledge vault. It answers questions by traversing MOCs (Maps of Content), design docs, postmortems, GitHub issues, commit history, and code — returning traced answers with source citations.

**Relationship to other tools:**
- `/obsidian` **writes** to the vault (notes, MOC updates)
- `/oracle` **reads** from the vault (queries, traversal, connection discovery)
- `code-finder` agent searches **code** (functions, classes, patterns)

## Process

### 1. Determine Scope & Complexity

```bash
PROJ_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

Assess the question:
- **Simple lookup** (list MOCs, find a doc by name, check an issue) → handle inline below
- **Deep traversal** (trace evolution of a concept, connect issues to code to design docs) → spawn the `oracle` agent via Task tool

For deep traversal, delegate:
```
Task(subagent_type="oracle", prompt="<the user's question with project root context>")
```

### 2. Locate the Knowledge Vault

Scan for the standard project layout (check in order):
1. `$PROJ_ROOT/private/claude/` — primary vault
2. `$PROJ_ROOT/private/claude/_maps/` — MOC files (start here)
3. `$PROJ_ROOT/private/claude/_oracle/` — oracle metadata (manifest, concepts index)
3b. `$PROJ_ROOT/private/claude/notes/` — working notes (`ideas/`, `bugs/`, `meta/`, and any project-specific subdirs)
4. `$PROJ_ROOT/CLAUDE.md`, `README.md`, `CHANGELOG.md` — user-facing docs
5. `$PROJ_ROOT/docs/` — public documentation
6. `$PROJ_ROOT/tests/one-offs/` — experimental scripts
7. `$PROJ_ROOT/tests/one-offs/thinking/` — ephemeral investigation

If no `private/claude/` exists:
> "No knowledge vault found in this project. You can start one with `/obsidian` to capture notes and build a knowledge graph."

If `private/claude/` exists but has no `_maps/` directory or MOC files, report the gap:
> "This project has documents but no knowledge map. Consider running `/obsidian` (bare) to create an initial MOC and link existing documents."

**Minimum viable vault**: `private/claude/` + `_maps/` with at least one MOC file. The `_oracle/` metadata layer, `notes/`, `issues/`, `reference-docs/` etc. are created as the vault grows. See the oracle agent docs for the full bootstrapping guide.

### 2b. Check Oracle Metadata (if `_oracle/` exists)

The `_oracle/` directory contains processing metadata maintained by the oracle:

- **`_oracle/manifest.md`** — Tracks which documents have been read, synthesized, or linked into MOCs. Documents marked **NEW** need processing. Compare `ls` of vault against this file to find unprocessed docs. Also tracks **GitHub Issues** — which issues have been read, commented on, or need review.
- **`_oracle/concepts.md`** — Concept → document index for fast topic lookup. Check here before grepping when looking for where a topic is discussed.
- **`_oracle/backlinks.md`** — Auto-generated reverse-link index. Regenerate with `python scripts/generate-backlinks.py [vault-path] --validate`. Use this for "what references document X?" queries instead of grepping the vault.

When doing a bare invocation or processing new documents:
1. Read `_oracle/manifest.md` to identify **NEW** (unprocessed) files and issues
2. Process each new file: read it, determine which MOC(s) it belongs to, create synthesis notes if warranted
3. Check GitHub issues: `gh issue list --state all --json number,title,state,labels,updatedAt` — compare against manifest's GitHub Issues section to find new or changed issues
4. **Sync issue stubs**: For any tracked issue that has no local file in `issues/`, create an auto-generated stub (see Issue Stub Generation below)
5. Regenerate backlinks: `python scripts/generate-backlinks.py [vault-path] --validate` to refresh the reverse-link index
6. Update `_oracle/manifest.md` with the new status (both docs and issues)
7. Update `_oracle/concepts.md` if new concepts were introduced

### 3. Answer the Question

#### For simple lookups (no agent needed):

- Read relevant MOC files in `_maps/`
- Use Grep to find keyword matches recursively across `private/claude/`
- Follow wikilinks `[[filename|display]]` to connected documents
- For reverse-link queries ("what references X?"): read `_oracle/backlinks.md` directly. If stale or missing, regenerate first with `python scripts/generate-backlinks.py [vault-path] --validate`
- Check GitHub issues with `gh issue list` and `gh issue view N`
- Return answer with file paths and line references

#### For questions requiring external knowledge:

When the vault doesn't have the answer and the question involves external tools, APIs, competitors, standards, or evolving technologies:

- **WebSearch** — search the web for current information (e.g., API docs, library comparisons, best practices)
- **WebFetch** — read specific URLs referenced in vault docs or issues
- **`/ask` or `/askq`** — delegate to research agents for deeper multi-source investigation
- Synthesize external findings together with local vault knowledge for a complete answer

#### For deep traversal (spawn oracle agent):

Use the Task tool:
```
Task(
  subagent_type="oracle",
  description="Oracle knowledge query",
  prompt="Project root: $PROJ_ROOT\n\nQuestion: $ARGUMENTS\n\nTraverse the knowledge vault and return a sourced answer."
)
```

### 4. Format the Response

Structure every answer as:

```markdown
## Answer

[Clear, direct answer to the question]

### Sources

- `private/claude/_maps/Project-Knowledge-Map.md` — [what was found here]
- `private/claude/2026-02-25__14-08-29__full-postmortem_...md:45` — [specific finding]
- Issue #7 — [relevant context]

### Connections

- [Related documents or concepts the user might want to explore next]
```

### 5. Use Tools, Then Mention Them

**Core principle: Always do the work.** The oracle answers questions by using its tools — reading files, running scripts, querying APIs. The caller gets the answer, not instructions for finding it themselves. Tips exist to let the caller know what tools are *available* for their own future use.

| Question Type | Oracle Action (DO THIS) | Tip to Caller (MENTION THIS) |
|---------------|------------------------|------------------------------|
| "What references X?" | Read `_oracle/backlinks.md`, answer directly | `generate-backlinks.py --stats` for vault health |
| "What's in issue #N?" | Run `gh issue view N` or `gh_issue_full.py N`, report | `gh_issue_full.py` for full timeline context |
| Commit history questions | Run `git log`, report findings | `/commit` for structured commit workflow |
| Design decision questions | Read vault docs, trace the chain, answer | `/dev-workflow-process` for structured analysis |
| Code location questions | Search codebase, locate it, answer | `code-finder` agent for deep code search |
| Knowledge structure questions | Read MOCs, trace connections, answer | `/obsidian` to capture new notes |
| Documentation gaps found | Report the gap with specifics | `/obsidian` (bare) to discover orphaned docs |
| External/unknown topics | WebSearch + WebFetch, synthesize with local context | `/ask` or `/askq` for deeper research |

After answering, optionally include **one** brief tip. Format:
```
> Tip: `/obsidian` can capture new notes and update the knowledge graph when you discover something worth preserving.
```

**Rules for tips:**
- **Always answer the question first** — the tip is supplementary, never a substitute
- Maximum one tip per answer
- Only when directly relevant to what was just discussed
- Never repeat a tip the user has already seen in this session
- Skip the tip entirely if nothing is contextually relevant

## Bare Invocation (no arguments)

When invoked as just `/oracle` with no question:

1. Read `_oracle/manifest.md` to identify **NEW** (unprocessed) documents
2. Read all MOC files in `_maps/` for current graph state
3. Regenerate backlinks: `python scripts/generate-backlinks.py [vault-path] --validate`
4. For each NEW document:
   - Read YAML frontmatter only (`tags:`, `also-in:`, `type:`, `date:`) — this is sufficient to classify the document, assign it to MOC(s), and add concept index entries
   - Full read only when: frontmatter is missing/sparse, or the document is a MOC (always read MOCs fully)
   - Determine which MOC(s) it should link into
   - Create synthesis notes if the document introduces new themes
   - Update `_oracle/manifest.md` status from NEW → synth/read/linked
   - Update `_oracle/concepts.md` with new concept entries
   - Update relevant MOC files with new wikilinks
5. Scan `private/claude/` for any documents not in the manifest at all (added since last manifest update)
6. Report:
   - Documents processed this run
   - Knowledge vault summary (file counts, topic areas)
   - Orphaned documents (not linked from any MOC)
   - Remaining gaps or open questions
   - Available toolkit (brief list of related skills/agents)

## Issue Stub Generation

When the oracle or obsidian encounters a GitHub issue with no local file in `issues/`, create an auto-generated stub for wikilink resolution and quick local reference.

**When to create stubs:**
- During bare invocation (step 4): any tracked issue missing a local file
- During note capture: when a note wikilinks to an issue draft that doesn't exist
- During queries: when answering questions about issues that have no local record

**Filename**: `issues/issue_NN_slug.auto.md` — the `.auto` suffix distinguishes auto-generated stubs from user-authored or manually-drafted issue files.

**Stub format:**
```markdown
---
type: issue-stub
issue: NN
source: gh-sync
author: claude
synced: YYYY-MM-DD
---

# Issue #NN: Title

**State**: OPEN/CLOSED | **Labels**: label1, label2 | **Created**: YYYY-MM-DD

## Summary

[First paragraph of issue body, or brief description if body is short]

---
*Auto-generated stub from `gh issue view NN`. Last synced: YYYY-MM-DD.*
*This is NOT a user-authored document. Regenerate with `/oracle` or update manually.*
```

**Rules:**
- **Never overwrite** a user-authored file (any existing `issue_NN_*.md` without `.auto` in the name)
- **Accuracy disclaimer**: Stubs reflect issue state at sync time — the `synced:` date is the moment-in-time accuracy marker
- **Update on re-sync**: During subsequent oracle passes, update stubs if the issue state/title/labels changed (bump `synced:` date)
- **Graduation**: If a user later writes a full issue draft for the same issue, delete the `.auto` stub to avoid duplication

## Notes

- The **oracle agent** (spawned via Task tool) is **read-only** — it reports findings and recommends changes but never modifies files
- The **oracle skill** (this file, running in the main conversation) **can write** — it updates manifest, concepts, MOCs, and backlinks during bare invocation passes
- Always use `/dev/null` not `nul` for shell redirection (Windows/WSL compatibility)
- For GitHub queries, gracefully handle `gh` CLI failures (offline, rate-limited) — continue with local files
- Wikilinks may reference moved/renamed files — report broken links as findings, don't fail
- The standard project layout is a convention, not a requirement — adapt to what exists
