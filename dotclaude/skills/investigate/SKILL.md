---
name: investigate
description: "Start a structured investigation for new work — gather context from files, issues, git, and agents, then synthesize into design docs, create a plan, and file GitHub issues. Accepts a goal description with hints about information sources."
---

# Investigation — From Idea to Plan

## Goal: "$ARGUMENTS"

Start a structured investigation for new work. The user provides a goal and hints about where to find relevant information. Claude gathers context, synthesizes understanding, creates a formal plan, and optionally files GitHub issues.

This is the **beginning-of-work** counterpart to `/fullpostmortem` (end-of-work).

## Phase 1: Gather

**Goal**: Build a complete picture of the problem space from all available sources.

### 1a. Parse User Input

Extract from the user's message:
- **Goal statement**: What are we trying to accomplish?
- **File hints**: Any `*.md` filenames, paths, or document references → read them
- **Issue hints**: Any `#N` references or issue descriptions → fetch with `gh_issue_full.py --full`
- **Keywords**: Technical terms, feature names, component names → search for related docs
- **Scope signals**: "small fix", "new feature", "refactor", "epic" → calibrate depth

### 1b. Read Referenced Sources (parallel where possible)

Launch up to 3 agents in parallel based on what was referenced:

**Local files** (most common starting point):
- Read all files the user mentioned by name
- Search `private/claude/` for related design docs (grep by keywords from goal)
- Check for existing plans in `~/.claude/plans/`

**GitHub issues** (CRITICAL — always chase references):
- For each referenced issue: `python scripts/gh_issue_full.py N --full --repo OWNER/REPO`
  - Look for `gh_issue_full.py` in project's `scripts/` folder first
  - Fallback: `scripts/repokit-common/gh_issue_full.py` (ships with any repo consuming the git-repokit-common subtree)
  - ALWAYS use `--full` flag to get complete body and all comments
- If issue has sub-issues or parent issues, read those too
- Check for CurrentTask/NextTask labeled issues: `gh issue list --label CurrentTask`
- **MANDATORY: Chase all references** — after reading an issue, scan the body and comments for:
  - Markdown filenames (e.g., `2026-03-16__23-20-59__dev-workflow-*.md`) → read those files
  - Other issue references (`#N`, `Refs #N`, `Closes #N`) → read those issues
  - URLs/URIs to external resources → fetch if relevant
  - Code file references → read those files
  - The "Analysis" or "Related" sections at the bottom often contain the most important references
- This reference-chasing step is what separates thorough investigation from piecemeal research

**Git context**:
- `git log --oneline -10` — recent history
- `git branch -a` — active branches
- `git status` — any in-progress work

**Code exploration** (when the goal touches specific code):
- Launch Explore agent to understand relevant code areas
- Use oracle agent to trace design decisions if needed

**External research** (when topic is unfamiliar or user requests it):
- Launch help agent for web search
- Use senior-engineer agent for architectural guidance

### 1c. Present Findings

Summarize what was gathered:
- Key documents read and their relevance
- Open questions or gaps in understanding
- Whether existing design docs already cover the topic

**Ask the user**: "Is there anything else I should read before we proceed to analysis?"

## Phase 2: Synthesize

**Goal**: Create or update a design document that captures the problem, approaches, and trade-offs.

### 2a. Assess Existing Coverage

Before creating a new document:
- Do existing design docs already cover this topic adequately?
- If yes: summarize what they say and skip to Phase 3
- If partially: create an addendum to the existing doc
- If no: create a new dev-workflow-process document

### 2b. Create Design Document

If new analysis is needed, use the `/dev-workflow-process` pattern:

```
./private/claude/YYYY-MM-DD__HH-MM-SS__dev-workflow-<topic>.md
```

Include:
1. **Problem Analysis** — user's verbatim goal + context gathered
2. **Considerations** — constraints, trade-offs, edge cases, affected systems
3. **Solutions** — evaluate approaches with pros/cons
4. **Synthesis** — recommended approach with PUVM summary

### 2c. Refine with User

Present the key findings and recommended approach. This is the checkpoint where the user provides feedback, corrections, or redirections before we commit to a plan.

Common user responses at this stage:
- "That looks right, let's plan it" → proceed to Phase 3
- "Actually, we should also consider..." → iterate on the design doc
- "Let's discuss this with Gemini" → trigger `/collaborate` skill
- "That's too complex, let's simplify" → narrow scope and re-analyze

## Phase 3: Plan

**Goal**: Create a concrete implementation plan.

### 3a. Enter Plan Mode

Use Claude's plan mode to create a structured implementation plan:
- Reference the design document from Phase 2
- Break work into concrete steps with file paths
- Include verification/testing strategy
- Identify risks and mitigations

### 3b. Back Up Plan

After plan approval, copy to project's `private/claude/`:
```
./private/claude/YYYY-MM-DD__HH-MM-SS__claude-plan__<topic>.md
```

### 3c. Create Feature Branch (if appropriate)

If the work warrants a branch (not all work does ask the user):
```bash
git checkout -b feature/<topic>
```

## Phase 4: Track

**Goal**: Ensure the work is properly tracked in GitHub and linked to related work.

### 4a. Review Existing Issues

Check if GitHub issues already exist for this work:
- `gh issue list --state open --limit 20`
- Search for related issues by keyword

### 4b. Propose New Issues (user approves)

If new issues are needed:
- Draft issue body to `private/claude/issues/`
- Present to user for review
- Only create after explicit approval
- Link sub-issues to parent epics if applicable

### 4c. Update Labels

- Apply `CurrentTask` label to the active issue
- Promote `NextTask` if there was one queued
- Reference the design doc filename in the issue body

## Adaptive Behavior

Not every investigation needs all 4 phases. Adapt based on signals:

| Signal | Behavior |
|--------|----------|
| User says "small fix" or references a single file | Skip Phase 2, lightweight Phase 3 |
| Existing design docs cover the topic | Summarize existing docs, skip to Phase 3 |
| User says "let's discuss" or "think about" | Focus on Phase 2, may skip Phases 3-4 |
| Topic is greenfield / unfamiliar | Heavy Phase 1 with research agents |
| User provides a detailed spec | Light Phase 1, skip Phase 2, focus on Phase 3 |
| User says "epic" or references multiple issues | Full 4-phase investigation |

## Output at Each Phase

| Phase | Output | User Checkpoint? |
|-------|--------|-----------------|
| **Gather** | Summary of sources read, gaps identified | Yes — "anything else to read?" |
| **Synthesize** | Design doc (dev-workflow-process) | Yes — "approach look right?" |
| **Plan** | Implementation plan (plan mode) | Yes — plan approval |
| **Track** | GitHub issues drafted | Yes — "create these issues?" |

## Example Invocations

```
/investigate We want to add image_purpose widget per #36. Read the design doc at
  2026-03-16__23-20-59__dev-workflow-image-purpose-widget-and-output-decoupling.md
  and check issue #42 for the epic context.

/investigate How should we handle the ComfyUI Registry submodule problem?
  The issue is that tarballs don't have .git directories.

/investigate #56 — I want to understand this issue and plan the fix.

/investigate Let's think about refactoring the serialization layer.
  Start with the collaborate3 results in private/claude/ and the Gemini feedback.
```

## Design Rationale

This skill was created from observing the repeated pattern of starting new work. The full design
rationale, including the exact user observations that led to this skill and the dev-workflow-process
analysis, is documented in:

a maintainer-private design document (not included in this repo)

Reading that document provides context for WHY each phase exists, what problem it solves, and how
the user typically interacts with the investigation process. Key insight: the user provides **hints**
(file paths, issue numbers, keywords) and expects Claude to bootstrap the investigation from those
hints rather than requiring manual orchestration of each step.

## Agent Orchestration

Each agent has a distinct role during investigation. Use the right agent for the right job:

| Agent | Role | When to Use |
|-------|------|-------------|
| `oracle` | MOC/backlink navigation, document relationships | Understanding how documents and concepts connect |
| `Explore` | Codebase search, file discovery | Finding code patterns, understanding current implementation |
| `senior-engineer` | Deep content analysis, architectural insight | Analyzing complex code, evaluating approaches |
| `help` | External research, web search | When topic is unfamiliar or needs external context |
| Zen/Gemini MCP | Difficult problems requiring outside perspective | Rare — triggered via `/collaborate1`, `/collaborate2`, or `/collaborate3` (number = exchange rounds) |

**Orchestration pattern**: Start with `oracle` to understand existing knowledge structure, use `Explore` to find relevant code, escalate to `senior-engineer` for deep analysis, and only reach for external consultation (`help` agent or `/collaborate`) when internal resources are insufficient.

## Notes

- Always save the user's verbatim message in any design doc created
- Never create GitHub issues without user approval
- The investigation may span multiple conversation turns — that's expected
- If context is getting low, create a context postmortem before compaction
- **Reference chasing is mandatory** — every referenced file, issue, or URL must be read before Phase 1 is complete
