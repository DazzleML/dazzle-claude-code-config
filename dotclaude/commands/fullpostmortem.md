---
description: Creates a comprehensive postmortem for completed work, focusing on problem-solution-lessons learned cycle.
allowed-tools: Bash, Write, Read, Glob, Grep
---

# Full Postmortem Analysis

Creating a comprehensive postmortem for completed work. Note in general you should try to:  **Talk about everything that was done in the session, what we learned, issues we are still having, where we are, what's next, and where we go from here.** 

## Information to Document:

Based on: "$ARGUMENTS"

I'll create a full postmortem covering:

1. **Problem Statement** - The original issue/request
2. **Root Cause Analysis** - What actually caused the problem
3. **Solution Journey** - Each approach tried, why it failed/succeeded
4. **Implementation Details** - Exact changes made
5. **Testing & Validation** - How we verified the solution
6. **Lessons Learned** - Key insights gained
7. **Time Analysis** - Where time was spent
8. **Future Improvements** - What would save time next time

The document will include:
- Exact commands that worked
- File modifications with line numbers
- Error messages encountered
- False leads explored
- Outstanding issues

```bash
# Gathering information... (commands to run)
TIMESTAMP=$(date +%Y-%m-%d__%H-%M-%S)
GIT_STATUS=$(git status --short 2>/dev/null)
RECENT_COMMITS=$(git log --oneline -10 2>/dev/null)
MODIFIED_FILES=$(git diff --name-only HEAD~1 2>/dev/null)

# Claude Code session info (auto-detect session name and ID)
# Search session state files for one matching current working directory
grep -rl "$(pwd)" ~/.claude/session-states/*.json 2>/dev/null | head -3
# Read matched file to extract: session_id, current_name, sesslog_dir
```

**Session info:** Always include the Claude Code session name and ID in the postmortem header as `**Session:** <name> (<uuid>)`. The session state lives at `~/.claude/session-states/<uuid>.json` containing `session_id`, `current_name`, `sesslog_dir`, and `cwd`. Find the right file by matching `cwd` to the current working directory, or by finding the most recently updated state file. This enables tracing from postmortem back to the full conversation transcript.

The full postmortem will be saved to the most appropriate location:
- **Project-specific**: `./private/claude/${TIMESTAMP}__full-postmortem_(TOPIC).md` (if within a project)
- **General/unclear**: `~/claude/${TIMESTAMP}__full-postmortem_(TOPIC).md` (for cross-project or uncertain context)

This document will serve as a complete reference for:
- Future debugging of similar issues
- Knowledge transfer to other developers
- Process improvement insights
- Time estimation for similar work

