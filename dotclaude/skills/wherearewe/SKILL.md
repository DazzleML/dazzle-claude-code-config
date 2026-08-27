---
name: wherearewe
description: "Inbound context recovery: find existing WhereWeAre docs, postmortems, issues, and git state to answer 'what's going on in this project?' Companion to /whereweare (which writes snapshots)."
allowed-tools: Bash, Read, Glob, Grep, Agent
---

# Where Are We — Inbound Context Recovery

Find and present the current state of a project. This is the "fill me in" skill -- you're arriving at a project and need to understand what's happening.

**This is the reader. `/whereweare` is the writer.**
- `/wherearewe` — "What's going on?" (find and present existing context)
- `/whereweare` — "Let's capture this." (write a snapshot for the future)

## When to Use

- **Returning to a project** after time away
- **Starting a new session** and want the quick picture
- **Checking in** on a project you haven't touched recently
- **Before making decisions** -- get grounded in current state first

## Inputs

- `$ARGUMENTS`: Optional focus area or question (e.g., "what's the CI status?", "what issues are open?", "what was the last thing we worked on?")
- If no arguments, do a general project state scan

## Process

### Step 1: Find Existing WhereWeAre Docs

```bash
# Check for WhereWeAre snapshots in this project (most recent first)
ls -t private/claude/*whereweare* 2>/dev/null | head -5

# Also check other active projects for cross-project awareness.
# CLAUDE_CODE_ROOTS: space-separated list of your project root dirs.
# Defaults to ~/code and /c/code, so it works unconfigured on a POSIX box
# and on Windows where projects live under C:\code. Set it in your shell
# profile or settings env to scan somewhere else instead.
for root in ${CLAUDE_CODE_ROOTS:-"$HOME/code" /c/code}; do
for dir in "$root"/*/private/claude "$root"/*/*/private/claude; do
  latest=$(ls -t "$dir"/*whereweare* 2>/dev/null | head -1)
  if [ -n "$latest" ]; then
    project=$(basename $(dirname $(dirname $(dirname "$latest"))))
    echo "[$project] $latest"
  fi
done
done
```

**If a recent WhereWeAre doc exists (< 7 days old):**
- Read it and present it to the user
- Note how old it is: "This snapshot is from 3 days ago"
- Supplement with quick git/issue scan for anything that changed since
- Read the "This Session" section to understand what was last worked on
- Check the "Previous WhereWeAre" link to understand the chain of context

**If no WhereWeAre doc exists or it's stale (> 7 days):**
- Tell the user: "No recent WhereWeAre snapshot found."
- Proceed to Step 2 to build context from other sources
- At the end, suggest: "Run `/familiarize` then `/whereweare` to create a fresh snapshot."

**Cross-project WhereWeAre docs:**
- If other projects have recent WhereWeAre docs, mention them briefly: "Also active: <project> (last snapshot <date>)"
- This helps the user remember what else was in flight

### Step 2: Gather Context from Available Sources

Search in this order, building a picture:

#### 2a. Recent postmortems and design docs
```bash
ls -t private/claude/*.md 2>/dev/null | head -10
```
Read the most recent 2-3 docs. Extract:
- "Future Considerations" / "Next Steps" sections
- "Current State" / "Issues Encountered" sections
- Any "where we go from here" content

#### 2b. Git state
```bash
git log --oneline -10
git status --short
git tag --sort=-creatordate -n1 | head -3
git branch --show-current
```

#### 2c. Open GitHub issues
```bash
gh issue list --state open --limit 15 2>/dev/null
```
Pay special attention to `CurrentTask` and `NextTask` labeled issues.

#### 2d. Recent Claude Code sessions
Check if session logs exist that might have context:
```bash
ls -t ~/.claude/sessions/*.json 2>/dev/null | head -5
```

#### 2e. Related projects
```bash
git remote -v 2>/dev/null | grep -v origin
```

### Step 3: Present Summary

Deliver a concise verbal summary to the user in the conversation (NOT a file). Structure as:

```
## Project: <name>
**Branch:** <branch> | **Version:** <version> | **Last activity:** <date>

### State
- [what's done, in progress, blocked]

### Recent Work
- [from postmortems/git log]

### Open Issues
- [from gh issue list, highlight CurrentTask/NextTask]

### Next Steps
- [from postmortems' "Future Considerations" + issue labels]

### Key Docs
- [list recent postmortems/design docs with one-line summaries]
```

**Keep it conversational.** This output lives in chat, not on disk. It's meant to orient the user quickly so they can decide what to do next.

### Step 4: Recommend Next Action

Based on what was found:

- **Fresh WhereWeAre exists:** "You're up to speed. The snapshot from <date> covers the current state."
- **Stale/missing WhereWeAre but postmortems exist:** "I've assembled context from postmortems and git. Consider running `/whereweare` to save a snapshot."
- **Very little context available:** "This project has minimal documentation. Consider running `/familiarize` for a deeper scan, then `/whereweare` to capture state."
- **User asked a specific question:** Answer it directly from the gathered context, then offer the general summary if useful.

## Relationship to Other Skills

| Need | Skill | Notes |
|------|-------|-------|
| "What's going on?" | **`/wherearewe`** (this) | Reads existing docs + git/issues |
| "Let me save where we are" | `/whereweare` | Writes a snapshot to disk |
| "Deep project context rebuild" | `/familiarize` | More thorough, reads README/CHANGELOG/structure |
| "Investigate a specific topic" | `/investigate` | Chases references, creates design docs |
| "Query project knowledge" | `/oracle` | Searches MOCs, design docs, postmortems |

### Escalation Chain
If `/wherearewe` doesn't find enough context:
1. Suggest `/familiarize` for deeper automated scanning
2. Then `/whereweare` to capture the result
3. If investigating a specific feature/issue, suggest `/investigate`
