---
name: whereweare
description: "Forward-looking project snapshot: what was done, what's next, key files, open issues, related projects, and everything needed to resume work after time away."
allowed-tools: Bash, Read, Write, Glob, Grep, Agent, WebFetch
---

# Where We Are — Project State Snapshot

A thin, scannable departure briefing for when you're stepping away from a project. Captures the vitals, next steps, and pointers so your future self (or another developer) can resume without context rebuilding.

**This is NOT a postmortem.** Postmortems look backward at what happened and why. This looks forward at what's active and where to go next. Think of it as the complement:
- **Postmortem**: "Here's what we did and what we learned"
- **WhereWeAre**: "Here's what's live and what to do next"

## When to Use

- **Stepping away** from a project for days/weeks/months
- **After a postmortem** to create the forward-looking companion doc
- **Resuming cold** — if no WhereWeAre exists, build one from postmortems, git history, and issues using `/familiarize`, `/investigate`, and oracle/senior-engineer agents as needed
- **Session handoff** when another person or future session needs to pick up work

## Inputs

- `$ARGUMENTS`: Optional focus area or notes (e.g., "focusing on the CI pipeline" or "about to pause for 2 weeks")
- If no arguments, produce a general project-wide snapshot

## Pre-Check: Previous WhereWeAre and Postmortems

Before writing, find the last WhereWeAre doc and recent postmortems:

```bash
# Find previous WhereWeAre docs (most recent first)
ls -t private/claude/*whereweare* 2>/dev/null | head -3

# Find recent postmortems
ls -t private/claude/*postmortem* private/claude/*full-postmortem* 2>/dev/null | head -3
```

**If a previous WhereWeAre exists:**
- Read it. This is your **checkpoint**. The new doc should reference it and clearly show what evolved since then.
- The "This Session" section captures what's new. The high-level sections can overlap but should reflect current reality.
- Link to it in the header: `**Previous:** <filename>`

**If no previous WhereWeAre exists:**
- Be as detailed as possible in every section -- this is the first baseline and future docs will diff against it.

**If a recent postmortem exists (from this session or today):**
- Reference it in the WhereWeAre doc. The postmortem has the details, WhereWeAre has the forward-looking pointers.

**If no recent postmortem and significant work was done this session:**
- Ask the user: "No postmortem exists for this session's work. Want me to run `/fullpostmortem` first?"
- If the user declines or the session was light (just review/planning), proceed without.

**If building from cold start (no active session context):**
- Skip postmortem check. Rely on `/familiarize` for context gathering.

## Cross-Project Awareness

We often work across multiple projects simultaneously. Before writing, scan for WhereWeAre docs in other active projects:

```bash
# Check other known project directories for recent WhereWeAre docs.
# CLAUDE_CODE_ROOTS: space-separated list of your project root dirs.
# Defaults to ~/code and /c/code, so it works unconfigured on a POSIX box
# and on Windows where projects live under C:\code. Set it in your shell
# profile or settings env to scan somewhere else instead.
for root in ${CLAUDE_CODE_ROOTS:-"$HOME/code" /c/code}; do
for dir in "$root"/*/private/claude "$root"/*/*/private/claude; do
  latest=$(ls -t "$dir"/*whereweare* 2>/dev/null | head -1)
  if [ -n "$latest" ]; then
    project=$(basename $(dirname $(dirname $(dirname "$latest"))))
    date=$(echo "$latest" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}")
    echo "$project: $latest ($date)"
  fi
done
done
```

If other projects have recent activity, note them in the "Related Projects" section. This gives the reader a sense of what else was happening in parallel and whether any cross-project coordination is needed.

## Source Priority

The WhereWeAre doc should reflect the **most current understanding** of the project. Sources are prioritized:

1. **Active session context** (primary) -- what was discussed, decided, and done in this conversation. This is the freshest, most accurate source.
2. **Git history and status** -- recent commits, branches, tags, dirty files. Always gathered automatically.
3. **GitHub issues** -- open issues, labels (CurrentTask/NextTask/evergreen), recent comments. Always gathered automatically.
4. **Recent postmortems and design docs** -- `private/claude/*.md` files. Scanned automatically for "Future Considerations" and "Next Steps" content.
5. **Oracle agent** (on demand) -- when the session context is thin or the project has deep history that needs tracing. Use the oracle to query design docs, MOCs, and postmortems for connections and decisions that aren't obvious from git log alone.

**Rule of thumb:** If the session was active and productive, items 1-4 are sufficient. If you're building a WhereWeAre after a `/familiarize` pass or from a cold start, lean heavily on items 2-5 and use the oracle agent to fill gaps.

## Information Gathering

Auto-gather these (skip sections that don't apply):

```bash
# Project identity
basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)
git branch --show-current
git log --oneline -1  # current HEAD

# Version state
git tag --sort=-creatordate -n1 | head -3
cat */_version.py 2>/dev/null | grep -E "^(MAJOR|MINOR|PATCH|PHASE|PROJECT_PHASE)" | head -6

# Recent activity
git log --oneline -10
git status --short

# Open issues
gh issue list --state open --limit 20 2>/dev/null

# Recent docs
ls -t private/claude/*.md 2>/dev/null | head -10

# Related repos (subtree remotes, submodules)
git remote -v 2>/dev/null
git submodule status 2>/dev/null

# Claude Code session info (auto-detect session name and ID)
# Find session state file for current working directory
grep -rl "$(pwd)" ~/.claude/session-states/*.json 2>/dev/null | head -3
# Or find by most recent update
ls -t ~/.claude/session-states/*.json 2>/dev/null | head -3
# Read the matched file to extract: session_id, current_name, sesslog_dir
```

**Session info extraction:** Always include the Claude Code session name and ID in the document header. The session state lives at `~/.claude/session-states/<uuid>.json` and contains `session_id`, `current_name`, `sesslog_dir`, and `cwd`. Search by matching `cwd` to the current working directory, or by finding the most recently updated state file. Include as `**Session:** <name> (<uuid>)` in the header.

## Document Template

Save to: `./private/claude/YYYY-MM-DD__HH-MM-SS__whereweare.md`

Always run `date +%Y-%m-%d__%H-%M-%S` for the timestamp.

```markdown
# Where We Are: <project-name>

**Date:** YYYY-MM-DD
**Session:** <session_name> (<session_id>)
**Branch:** <branch> (<clean/dirty>)
**Version:** <version or tag>
**Last commit:** <hash> <message>
**Previous WhereWeAre:** `<filename>` (or "None -- first snapshot")
**Session postmortem:** `<filename>` (or "None")

## Project State (High Level)

The big picture first -- the reader needs to understand everything that's going on before drilling into session specifics. Should overlap with previous WhereWeAre docs to provide full context -- each snapshot should stand on its own as a complete orientation.

**Done:**
- [completed items, accumulated across sessions]

**In Progress:**
- [anything partially done, with notes on where it left off]

**Blocked:**
- [anything waiting on external input, decisions, or dependencies]

## This Session

What specifically happened since the last WhereWeAre checkpoint. This is the delta -- the reader already has the big picture above, now they see what's fresh.

- [What was worked on, key decisions made, problems solved]
- [Commits produced, with hashes]
- [What evolved from where the previous WhereWeAre left off]
- [Reference postmortem filename for full details if one exists]

> If no previous WhereWeAre exists, this section covers the most recent session or work cycle.

## Next Steps

1. [Highest priority -- what to do first when resuming]
2. [Second priority]
3. [Third priority]
- [Additional items, less urgent]

> For each item: include file paths, issue numbers, or doc references so you can jump straight in.

## Key Files

| Purpose | Path |
|---------|------|
| Main code | `<path>` |
| Config | `<path>` |
| Tests | `<path>` |
| Docs | `<path>` |
| Design docs | `private/claude/` |

## Open Issues

Use `owner/repo#N` format so issue numbers render as clickable links (e.g., `DazzleTools/dazzlesum#2`).

| # | Title | Labels | Status/Notes |
|---|-------|--------|-------------|
| owner/repo#N | Title | labels | brief note on state |

## Related Projects

| Project | Relationship | State |
|---------|-------------|-------|
| project-b | subtree dependency | v0.2.2, up to date |
| project-c | shares component X | needs sync after our changes |

## Document Trail

Links to previous WhereWeAre docs and recent postmortems, forming a chain of context.

- **Previous WhereWeAre:** `<filename>` -- [one-line summary of where things stood]
- **Postmortems since last checkpoint:**
  - `YYYY-MM-DD__...__full-postmortem_topic.md` -- [one-line summary]
- **Design docs since last checkpoint:**
  - `YYYY-MM-DD__...__dev-workflow_topic.md` -- [one-line summary]

## Notes for Future Self

- [Gotchas, warnings, things that are easy to forget]
- [Decisions that were made and why (brief -- link to postmortem for details)]
- [Environment setup notes if non-obvious]
```

## Guidelines

- **Be thin.** Target 1-2 pages. Link, don't repeat. If a postmortem has the details, reference it by filename.
- **Be scannable.** Tables and bullet points over paragraphs. Someone should grasp the state in 60 seconds.
- **Be honest about unknowns.** If something is unclear or risky, say so. "Not sure if X works after Y change" is more useful than silence.
- **Include file paths.** Every reference to code, docs, or issues should be actionable -- someone should be able to open the file or URL directly.
- **Cross-project awareness.** If this project depends on or affects others, note their state too. This is especially important for subtree/submodule relationships.

## Building WhereWeAre from Cold Start

**IMPORTANT:** If building this doc after time away (not at the end of an active session), **always run `/familiarize` first**. The familiarize pass loads project context into the conversation -- recent git activity, open issues, design docs, project structure -- which ensures the WhereWeAre doc is grounded in current reality rather than stale assumptions.

**Chain: `/familiarize` -> `/whereweare`**

The familiarize output stays in conversation context and directly feeds the synthesis here. Without it, the WhereWeAre doc risks being shallow or outdated.

After familiarize, supplement with:

1. **Read recent postmortems** in `private/claude/` — extract "Future Considerations" and "Next Steps" sections
2. **`gh issue list`** — check open issues for CurrentTask/NextTask labels
3. **Oracle agent** — query project knowledge vault for recent decisions and connections
4. **Investigate agent** — if the project has changed significantly, chase references in issues and docs
5. **Senior-engineer agent** — for technical assessment of partially-completed work

Then synthesize into the WhereWeAre template above. This turns the scattered artifacts into a single actionable document.

## After Postmortems

When running this after a `/fullpostmortem` or other postmortem variant, the postmortem's "Future Considerations", "Follow-up Tasks", and "Lessons Learned" sections are primary inputs for the "Next Steps" and "Notes for Future Self" sections here. Reference the postmortem by filename rather than duplicating its content.

## Companion Skill: `/wherearewe`

`/wherearewe` is the **reader** -- it finds and presents existing WhereWeAre docs and project state. This skill (`/whereweare`) is the **writer** -- it creates new snapshots.

- If someone runs `/wherearewe` and no snapshot exists, it suggests running `/familiarize` then `/whereweare`
- If someone runs `/whereweare` and no postmortem exists for recent work, it offers to create one first
- The two skills form a read/write pair for project state continuity
