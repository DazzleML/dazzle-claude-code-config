---
description: [SYNC - Blocks session] Launches the help agent to research and answer questions in isolated context. Creates comprehensive Q&A documentation. This is the full-featured research command that may take 2-5 minutes. For non-blocking version, use /ask instead.
allowed-tools: Task
---

I'll use the help agent to research and answer your question while preserving the main session context.

**Your Question**: "$ARGUMENTS"

The help agent will:
1. Research your question using local files, web search, and optionally advanced AI models
2. Provide a comprehensive answer
3. Document the Q&A session for future reference
4. Save the results to `./private/claude/questions/` or the global questions folder

Launching the help agent now...

<Task>
description: Research question
prompt: |
  ## Session Context
  The main session is currently working on development tasks. This question has been delegated to preserve context.
  
  ## User's Question
  $ARGUMENTS
  
  ## Your Task
  1. Research this question thoroughly using available tools
  2. **IMPORTANT**: For ANY questions about current events, news, stock markets, recent dates, or real-world information - ALWAYS use WebSearch as your PRIMARY tool
  3. For code/technical questions: Start with local codebase if relevant (Read, Grep, Glob)
  4. Use WebSearch liberally - it's encouraged for any factual information
  5. Use WebFetch to get details from specific URLs found via search
  6. Only use mcp__zen__ or mcp__gpt-codex__ if explicitly requested
  7. If using MCP tools, ALWAYS capture session/continuation IDs for future reference
  8. Provide a comprehensive answer with actual data, not generic advice
  9. Document everything in a structured Q&A file
  
  ## Critical Instructions for Current Events
  - Questions about dates, markets, news, or events REQUIRE WebSearch
  - Do NOT give generic advice when specific data is requested
  - If asked about "yesterday" or specific dates, search for that exact date
  - Financial/market questions: Search for actual prices, percentages, and movements
  
  ## Documentation Requirements
  Create a detailed Q&A document following this save logic:
  1. If `./private/claude/` exists:
     - Create `./private/claude/questions/` if it doesn't exist
     - Save to: `./private/claude/questions/YYYY-MM-DD__HH-MM-SS__(question_summary).md`
  2. If `./private/claude/` doesn't exist:
     - Create `~/claude/questions/` if needed
     - Save to: `~/claude/questions/YYYY-MM-DD__HH-MM-SS__(question_summary).md`
     - Note: `~/claude/` is `%USERPROFILE%\claude\` on Windows
  
  Use the format specified in your agent configuration for the documentation.
  
  ## Response Format
  Provide:
  1. Direct answer to the question
  2. Supporting evidence and sources
  3. Path to the saved Q&A document
  4. Any MCP session/continuation IDs (if applicable) for future reference
  5. Any critical findings that might affect the main development session
  
  Remember: You're operating in isolated context to preserve the main session's tokens. Make your research thorough but focused.
subagent_type: help
</Task>