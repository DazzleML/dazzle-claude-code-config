---
description: [SYNC - Blocks briefly] Quick Q&A using help agent with time constraints. Faster than /longask (15-30 seconds). Saves comprehensive answer to questions folder. For non-blocking version use /askq.
allowed-tools: Task
---

I'll use the help agent to quickly answer your question and save it for future reference.

**Question**: "$ARGUMENTS"

The help agent will:
1. Provide a concise but thorough answer
2. Skip extensive research to prioritize speed
3. Save the Q&A for future reference
4. Complete within 15-30 seconds

Launching the quick help agent now...

<Task>
description: Quick Q&A research
prompt: |
  ## Session Context
  The main session needs a quick answer. This has been delegated to preserve context.
  
  ## User's Question
  $ARGUMENTS
  
  ## Your Task - QUICK ANSWER (15-30 seconds max)
  1. Provide a direct, comprehensive answer based on your knowledge
  2. **For current events/news/markets**: Do a QUICK WebSearch to get real data (don't give generic advice)
  3. For technical questions: Use your knowledge, minimal research if needed
  4. Focus on speed while maintaining accuracy
  5. Save the Q&A to the appropriate questions folder
  
  ## Time Constraint
  **IMPORTANT**: This is a QUICK answer request. Prioritize speed over exhaustive research.
  - For current events: One quick WebSearch is OK and encouraged
  - For technical topics: Use existing knowledge primarily
  - Keep research minimal but get REAL DATA when needed
  - Target completion in 15-30 seconds
  
  ## Documentation Requirements
  Create a Q&A document following this save logic:
  1. If `./private/claude/` exists:
     - Create `./private/claude/questions/` if it doesn't exist
     - Save to: `./private/claude/questions/YYYY-MM-DD__HH-MM-SS__quick-qa__(question_summary).md`
  2. If `./private/claude/` doesn't exist:
     - Create `~/claude/questions/` if needed
     - Save to: `~/claude/questions/YYYY-MM-DD__HH-MM-SS__quick-qa__(question_summary).md`
     - Note: `~/claude/` is `%USERPROFILE%\claude\` on Windows
  
  ## Response Format
  Provide:
  1. Direct answer to the question
  2. Key points and examples if relevant
  3. Path to the saved Q&A document
  4. Note that this was a quick answer (for user's reference)
  
  Remember: Speed is priority. Provide a good answer quickly rather than a perfect answer slowly.
subagent_type: help
</Task>