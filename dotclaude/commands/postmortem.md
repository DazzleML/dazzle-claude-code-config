---
description: Creates a postmortem analysis document. Automatically selects the appropriate type based on context or prompts for selection.
allowed-tools: Bash, Write, Read, Glob
---

# Postmortem Analysis

This command will help you create a postmortem analysis. Let me determine the most appropriate type based on the context.

## Analyzing Context...

```bash
# Check if we have completed work (git commits)
recent_commits=$(git log --oneline -5 2>/dev/null | head -3)

# Check if we're debugging (error logs, test failures)
debugging_indicators=$(find . -name "*.log" -mmin -30 2>/dev/null | wc -l)

# Check session duration
session_duration=$(($(date +%s) - ${SESSION_START:-$(date +%s)}))
```

Based on the current context, I'll help you create the appropriate postmortem:

**Options Available:**
1. **Full Postmortem** - For completed work documentation (see file: "@~/.claude/commands/fullpostmortem.md")
2. **Mini Postmortem** - For current active debugging/problem-solving (see file: "@~/.claude/commands/minipostmortem.md")
3. **Context Postmortem** - For session handoff/context preservation (see file: "@~/.claude/commands/contextpostmortem.md")

Please specify which type you'd like, or provide context about what you're documenting:
- If you've just **completed significant work**, I'll create a Full Postmortem
- If you're **stuck or in the middle of a problem**, I'll create a Mini Postmortem
- If you're **ending a session or near the Claude context-window boundary**, I'll create a Context Postmortem

**Your Input:** "$ARGUMENTS"

Based on your input, I'll now create the appropriate postmortem document with:
- Proper timestamp and filename
- All relevant sections filled out
- Key information captured
- Actionable next steps documented

The postmortem will be saved to the most appropriate location:
- **Project-specific**: `./private/claude/YYYY-MM-DD__hh-mm-ss__[type]-postmortem_(TOPIC).md` (if within a project)
- **General/unclear**: `~/claude/YYYY-MM-DD__hh-mm-ss__[type]-postmortem_(TOPIC).md` (for cross-project or uncertain context)
