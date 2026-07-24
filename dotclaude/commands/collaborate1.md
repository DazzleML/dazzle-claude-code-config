# Collaborate1 Command - Single-Round Focused Consultation

## Purpose
Quick, focused single-round consultation with an AI expert for technical questions or validation, when you need expert input on a narrow topic without extensive back-and-forth.

## Process Overview
One focused exchange followed by immediate action:
- Round 1: Present specific question(s) with context, get expert analysis
- Action: Integrate insights and proceed with implementation

## API Key Usage
**CRITICAL**: Always try in this order:
1. First attempt: Use `GEMINI_API_KEY` (free usage quota)
2. If GEMINI fails: Fallback to `OPENROUTER_API_KEY`
3. Document which API was used in the response file

## Detailed Steps

### Preparation
1. Focus on a specific issue or decision point
2. Gather relevant context:
   - Problem description
   - Code files involved
   - Previous attempts and failures
   - Current understanding
   - Constraints and requirements
   - Specific questions
3. Formulate clear, answerable questions

### Round 1: Focused Question(s) & Expert Response
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`):
   - Complete overview of the problem
   - All relevant code structure
   - Work attempted so far
   - Specific question(s) needing answers
   - Clear success criteria
   - Request for simple/quick solutions vs. robust solutions vs. longterm solutions vs other possible factors as solutions
   - Request a final concrete recommendation with solutions and considerations

2. **Send to expert using mcp__zen__chat**:
   - Try `model: "gemini-2.5-pro"` first
   - If fails, retry with `model: "openai/o3"` or Codex MCP or similar
   
3. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_(ModelUsed)_(topic).md`, with (ModelUsed) likely being Gemini25): 
   - **CRITICAL**: Save the `continuation_id` at the very top of the file
   - Note which API/model was used
   - Save response VERBATIM
   - No editing or summarizing
   - Format:
     ```markdown
     # Expert Response - [Topic]
     
     **CONTINUATION_ID**: [id-here]
     **MODEL_USED**: [gemini-2.5-pro or fallback]
     **REMAINING_TURNS**: [number]
     
     ---
     
     [Full verbatim response]
     ```

### Final: Final Assessment (Independent Decision)
Create `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_FINAL_ASSESSMENT_(topic).md`:
- Synthesize discussion
- Apply dev-workflow-process if complex
- Problem Analysis (*SPCR: Story*)
- Considerations Analysis (*SPCR: Puzzle*)
- Solutions Evaluation (*SPCR: Content*)
- Synthesis & Recommendation (*SPCR: Result + PUVM*)
- Create action plan
- Note risks and mitigations
- Document YOUR decision, informed by but not dictated by expert input

## Key Principles
1. **Quality over quantity** - One focused round on specific questions to narrow in on actionable items
2. **Critical thinking over compliance** - Challenge suggestions
3. **Independent decision** - You choose, not the expert
4. **Full documentation** - Verbatim records
5. **Structured analysis** - Use frameworks consistently


## File Naming Convention
All files in `~/claude/` or `./private/claude/`:
- Your question: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`
- Expert response: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_(Expert)_(topic).md`

## When to Use
- A focused specific technical question
- Need quick validation of an approach
- Clarification on best practices
- Syntax or API usage questions
- Performance optimization tactics
- "Is X better than Y for Z?" questions

## When NOT to Use
- Complex architectural decisions (use collaborate2 or collaborate3)
- Multiple interrelated questions (use collaborate2)
- Need to challenge and test ideas (use collaborate2)
- Critical decisions requiring thorough analysis (use collaborate3)

## Example Usage
```
User: "Quick question for Gemini - is asyncio.gather or asyncio.create_task better for our use case?"

Claude: 
1. Prepares focused question with specific context
2. Sends to Gemini 2.5 Pro (or falls back to OpenAI)
3. Saves response with continuation_id
4. Implements based on recommendation
```

## Comparison with Other Collaborate Commands
| Aspect | Collaborate1 | Collaborate2 | Collaborate3 |
|--------|-------------|--------------|--------------|
| Rounds | 1 | 2 + decision | 3 + assessment |
| Time | ~5-10 min | ~30-45 min | ~60-90 min |
| Depth | Focused | Good | Comprehensive |
| Best for | Quick questions | Clear problems | Complex issues |
| Critical thinking | Minimal | Moderate | Extensive |
| Documentation | Light | Full | Exhaustive |

## Key Principles
1. **Speed over depth** - Get quick expert input
2. **Focus over breadth** - One question, one answer
3. **Trust with verification** - Accept expert input for narrow scope
4. **Always save continuation_id** - Enable follow-up if needed
5. **Try free tier first** - Use GEMINI before OPENAI

Remember: This is for quick, focused questions where you mostly trust the expert's input. For critical decisions or when you need to challenge ideas, use collaborate2 or collaborate3.