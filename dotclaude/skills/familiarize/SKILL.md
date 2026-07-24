---
name: familiarize
description: "Rebuild project context at session start by reading key docs, git state, issues, and design history. Accepts an optional argument describing the current focus or goal."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, AskUserQuestion, WebSearch, WebFetch
---

# Project Familiarization — Context Rebuild

## Focus: "$ARGUMENTS"

Rebuild context for the current project by systematically reading its key artifacts. If the user provided a focus argument above, prioritize areas relevant to that goal. If no argument was provided, do a general survey.

## Steps (run in parallel where possible)

### 1. Project Identity
- Read `README.md` (or equivalent) to understand what the project does
- Read `CHANGELOG.md` (or equivalent) to understand recent changes and current version
- Check for `CLAUDE.md` or `.claude/CLAUDE.md` project-level instructions
- Check for auto-memory files in `~/.claude/projects/` that match this project

### 2. Git State
- `git log --oneline -15` — recent commit history
- `git status` — working tree state (staged, unstaged, untracked)
- `git diff --stat` — summary of uncommitted changes
- `git branch -a` — branches (local and remote)
- If there are uncommitted changes, read the full `git diff` to understand work-in-progress

### 3. WhereWeAre Snapshots and Design History
- **First priority:** Check for WhereWeAre snapshots: `ls -t private/claude/*whereweare* 2>/dev/null | head -3`
  - If one exists, read the most recent — it's the fastest way to get oriented. It has the project state, next steps, key files, and links to postmortems.
  - Check its "Previous WhereWeAre" link to understand the chain of context.
- **Second priority:** Glob for `private/claude/**/*.md` — postmortems, design docs, analysis documents
- Read the most recent 2-3 documents (by filename date) to understand recent work context
- Check for any `commits/` subfolder with staged commit messages

### 4. Session Logs
- Session logs are stored in `~/.claude/sesslogs/`
- The `.sesslog_*` files are the most detailed and contain full conversation transcripts
- To find recent sessions that touched this project, grep across sesslogs by the current working directory path:
  ```
  grep -rl "$(basename $(pwd))" ~/.claude/sesslogs/.sesslog_* | xargs ls -lt | head -5
  ```
- Read the most recent matching sesslog (tail end) to understand what was being worked on last session
- This is especially useful when there's no context postmortem and you need to reconstruct what happened

### 5. GitHub Issues
- `gh issue list --state open --limit 10` — open issues
- If the focus argument references a specific issue number, read that issue in detail

### 6. Project Structure
- `ls` the top-level directory to understand layout
- Glob for key config files (`*.toml`, `*.json`, `*.yml` at root) to understand tooling
- Identify the main source files and test structure

### 7. Focus-Specific Deep Dive
If the user provided a focus argument:
- Search for files, functions, or patterns related to the stated focus
- Read the most relevant source files
- Check git log for recent commits touching those areas
- Look for related GitHub issues or design docs

## Output

After gathering context, provide a concise summary:
1. **Project**: What it is, current version
2. **Recent Activity**: Last few commits, what was being worked on
3. **Current State**: Any uncommitted changes, open branches
4. **Open Issues**: Key open GitHub issues
5. **Focus Context**: (if argument provided) Relevant files, recent changes, and design decisions related to the stated goal
6. **Ready to Work**: What's the logical next step given the current state and focus

Keep the summary to ~20-30 lines. The goal is efficient context loading, not exhaustive documentation. If the focus argument is detailed, let it guide which areas get deeper attention.

## Notes

- Use the `Explore` agent for broad codebase searches when the project is large
- Use the `oracle` agent when you need to trace design decisions or understand how components connect
- If `private/claude/` contains many docs, prioritize by recency — the last 2-3 sessions are most relevant
- **WhereWeAre docs (`*whereweare*`) are the single best starting point** — they're purpose-built for exactly this situation. Read the most recent one first, then follow its "Previous WhereWeAre" link and "Document Trail" section for the chain of context.
- Check for any context postmortems (`context-postmortem_*.md`) as these are specifically written for session handoffs
- Session logs in `~/.claude/sesslogs/` (especially `.sesslog_*` files) contain full conversation transcripts from previous sessions — grep by project directory path to find relevant ones. These are the last resort when no postmortem or design doc exists, but often the most detailed source of "what were we doing and why"
