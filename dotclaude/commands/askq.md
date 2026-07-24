---
description: [ASYNC - Non-blocking WITH NOTIFICATIONS] Quick Q&A with safe character handling. Shows answer preview when ready. For full research use /ask. For blocking version use /quick-ask.
allowed-tools: Bash, BashOutput
---

I'll answer your question in background and **notify you when ready** with a preview!  
This handles all special characters safely including quotes, backticks, and shell variables.

**Question**: "$ARGUMENTS"

## Launching Quick Q&A

Starting safe quick research...

[Executing with proper character handling]

#!/bin/bash
# Make scripts executable if needed
chmod +x ~/.claude/scripts/async-quick-safe.sh 2>/dev/null

# Launch the quick Q&A script with safe character handling
# The script handles all escaping internally
~/.claude/scripts/async-quick-safe.sh "$ARGUMENTS" &

echo ""
echo "⚡ Quick Q&A launched!"
echo "📢 Notification coming in ~15-30 seconds"
echo "🔒 Special characters handled safely"
echo "👀 You'll see a preview of the answer"
echo ""
echo "Continue working - notification coming!"

## Safe Character Handling

Properly handles:
- Quotes: "double" and 'single'
- Shell: $variables, `commands`, ${expansions}
- Markdown: **bold**, _italic_, `code`
- Paths: C:\Windows\Path and /unix/path
- Special: @, #, %, ^, &, *, (), [], {}

## Notification Preview

When complete, you'll see:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ QUICK ANSWER READY!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Question: [safely displayed]
📄 Answer saved to: [path]
⏱️ Duration: X seconds

📖 Preview:
[First few lines of answer...]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Questions with "any `special` $characters" work perfectly!