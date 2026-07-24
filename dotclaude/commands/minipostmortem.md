---
description: Creates a quick postmortem for active debugging, capturing current state, evidence, and hypotheses.
allowed-tools: Bash, Write, Read, Grep
---

# Mini Postmortem - Active Debugging

Creating a mini postmortem to capture current work and debugging state...

## Current Context: "$ARGUMENTS"

We should follow the normal postmortem analysis process, but with a focus on documenting:

1. **Current Symptoms** - What's happening right now
2. **Evidence Collected** - Logs, errors, test results
3. **Tests Run** - What passed, what failed, what's pending
4. **Current Hypotheses** - Theories about the cause
5. **Files Under Investigation** - What we're examining
6. **Next Steps** - Immediate actions to take

This mini postmortem helps:
- Organize scattered thoughts
- Avoid repeating failed attempts
- Identify patterns in evidence
- Plan systematic next steps
- Hand off to another session if needed

```bash
# Quick context capture (scripts to run)
TIMESTAMP=$(date +%Y-%m-%d__%H-%M-%S)
CURRENT_DIR=$(pwd)
RECENT_ERRORS=$(find . -name "*.log" -mmin -30 -exec tail -20 {} \; 2>/dev/null | grep -i error | head -10)
OPEN_FILES=$(lsof +D . 2>/dev/null | grep -E '\.(py|js|md)$' | awk '{print $NF}' | sort -u | head -10)
```

The mini postmortem will be saved to the most appropriate location:
- **Project-specific**: `./private/claude/${TIMESTAMP}__mini-postmortem_(TOPIC).md` (if within a project)
- **General/unclear**: `~/claude/${TIMESTAMP}__mini-postmortem_(TOPIC).md` (for cross-project or uncertain context)

This detailed document is designed to be:
- Immediately actionable
- Easy to update as investigation progresses with a follow-up document (we should treat postmortems as mostly immutable where we just add to the sequence for history)
- Perfect for "rubber duck debugging"
