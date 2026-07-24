---
description: [ASYNC - Non-blocking WITH NOTIFICATIONS] Launches help agent research in background with safe character handling. Returns immediately. Notifies when complete. For blocking version use /longask.
allowed-tools: Bash, BashOutput
---

I'll launch the help agent in a background subprocess. **You'll be notified when it completes!**  
This handles all special characters safely including quotes, backticks, and shell variables.

**Question**: "$ARGUMENTS"

## Launching Async Research

Running background research with character escaping...

[Starting help agent subprocess]

#!/bin/bash
# Make scripts executable if needed
chmod +x ~/.claude/scripts/async-ask-safe.sh 2>/dev/null

# Launch the research script with safe character handling
# The script handles all escaping internally
~/.claude/scripts/async-ask-safe.sh "$ARGUMENTS" &

echo ""
echo "🚀 Research launched in background!"
echo "📢 You'll receive a notification when complete (2-5 minutes)"
echo "🔒 Special characters handled safely"
echo "💡 Continue with your work - no need to check manually"
echo ""
echo "📝 Results will be saved to:"
echo "   ./private/claude/questions/ or ~/claude/questions/"
echo ""
echo "The notification will show:"
echo "  ✅ File location of comprehensive Q&A documentation"
echo "  ⏱️ Time taken to complete"
echo "  📋 Your question (safely truncated if long)"

## What's Happening

- **Full help agent** running with web search, file operations, and MCP tools
- **Non-blocking** - this session continues immediately  
- **Safe escaping** - handles quotes, $variables, backticks, markdown
- **Auto-notification** - you'll see when research completes
- **MCP session IDs** preserved if Zen/Codex tools are used

The help agent creates comprehensive documentation just like `/longask`, but without blocking your workflow and with automatic completion alerts.