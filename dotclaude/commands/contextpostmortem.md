---
description: Creates a context handoff postmortem for session transitions, preserving all critical state and continuation instructions.
allowed-tools: Bash, Write, Read, TodoWrite, Glob
---

# Context Postmortem - Session Handoff

Creating a comprehensive context handoff document...

## Session Context: "$ARGUMENTS"

We should do a full normal postmortem analysis. The focus with the "context postmortem" is to preserve:

1. **Mission Status** - Original goal and current progress
2. **Completed Work** - What's been finished
3. **Active Work** - Current task and exact state
4. **Pending Work** - Queued tasks and priorities
5. **Critical Context** - Information that MUST not be lost
6. **File State** - All modified files and their status
7. **Environment State** - Services, configs, databases
8. **Resume Instructions** - Exact commands to continue

This context postmortem ensures:
- Zero context loss between sessions
- Immediate productivity on resume
- No repeated work or debugging
- Clear understanding of current state

```bash
# Comprehensive state capture (commands to run and use)
TIMESTAMP=$(date +%Y-%m-%d__%H-%M-%S)
GIT_STATUS=$(git status 2>/dev/null)
GIT_DIFF=$(git diff --stat 2>/dev/null)
MODIFIED_FILES=$(git diff --name-only 2>/dev/null)
SERVICE_STATUS=$(systemctl status "$PROJECT_SERVICE" 2>/dev/null | grep Active)  # if the project runs a service
TODO_STATUS=$(cat /tmp/current_todos.txt 2>/dev/null || echo "No todos found")
```

Key information being captured:
- Exact position in work stream
- All uncommitted changes
- Environmental dependencies
- Decision points reached
- Open questions requiring answers

The context postmortem will be saved to the most appropriate location:
- **Project-specific**: `./private/claude/${TIMESTAMP}__context-postmortem_(TOPIC).md` (if within a project)
- **General/unclear**: `~/claude/${TIMESTAMP}__context-postmortem_(TOPIC).md` (for cross-project or uncertain context)

This document enables:
- Seamless session continuation
- Handoff to different Claude instance
- Recovery from unexpected termination
- Clear work state communication

**IMPORTANT**: This document should be created whenever:
- Approaching context window limits
- Switching to different work
- Ending work session
- Complex state needs preservation
