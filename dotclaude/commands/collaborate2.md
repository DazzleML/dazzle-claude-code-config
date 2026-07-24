# Collaborate2 Command - Two-Round Expert Consultation

## Purpose
Streamlined 2-round consultation with an AI expert for technical decisions, maintaining critical analysis while reducing overhead.

## Process Overview
Two rounds of exchange followed by independent decision:
- Round 1: Present context, get initial analysis
- Round 2: Critical evaluation and probe weaknesses
- Final: Independent decision based on analysis

## API Key Usage
**CRITICAL**: Always try in this order:
1. First attempt: Use `GEMINI_API_KEY` (free usage quota)
2. If GEMINI fails: Fallback to `OPENROUTER_API_KEY`
3. Document which API was used in the response file

## Detailed Steps

### Preparation
1. Gather relevant context:
   - Problem description
   - Code files involved
   - Previous attempts and failures
   - Current understanding
   - Constraints and requirements
   - Specific questions

### Round 1: Context & Initial Analysis
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`):
   - Complete overview of the problem
   - All relevant code structure
   - Work attempted so far
   - Specific questions needing answers
   - Request for simple/quick solutions vs. robust solutions vs. longterm solutions vs other possible factors as solutions
   - Request for solutions and considerations


2. **Send to expert using mcp__zen__chat**:
   - Try `model: "gemini-2.5-pro"` first
   - If fails, retry with `model: "openai/o3"` or Codex MCP or similar
   
3. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_(ModelUsed)_(topic).md`, with (ModelUsed) likely being Gemini25):
   - Save expert's response VERBATIM
   - No editing or summarizing
   - **CRITICAL**: Save the continuation_id at the top of the file for future reference

4. **Critical analysis** (internal):
   - Categorize each suggestion: Good / Neutral / Problematic
   - Note surrounding factors
   - Consider effects on other code/data
   - Identify weak points to probe

### Round 2: Critical Evaluation & Testing
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Claude_(topic).md`):
   - DO NOT blindly accept suggestions
   - Present your own analysis of proposals
   - Ask probing questions about weak points
   - Request test strategies to validate ideas (using the scientific method to falsify ideas)
   - Challenge assumptions
   - Explore edge cases
   - Form preliminary action plan

2. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Gemini25_(topic).md`):
   - Save VERBATIM
   - **CRITICAL**: Save the continuation_id at the top of the file for future reference

### Final: Final Assessment (Independent Decision)
Create `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_FINAL_ASSESSMENT_(topic).md`:
- Synthesize both rounds
- Apply dev-workflow-process if complex
- Problem Analysis (*SPCR: Story*)
- Considerations Analysis (*SPCR: Puzzle*)
- Solutions Evaluation (*SPCR: Content*)
- Synthesis & Recommendation (*SPCR: Result + PUVM*)
- Create action plan
- Note risks and mitigations
- Document YOUR decision, informed by but not dictated by expert input

## Key Principles
1. **Quality over quantity** - Two good rounds beat three rushed ones
2. **Critical thinking over compliance** - Challenge suggestions
3. **Independent decision** - You choose, not the expert
4. **Full documentation** - Verbatim records
5. **Structured analysis** - Use frameworks consistently

## File Naming Convention
All files in `~/claude/` or `./private/claude/`:
- Round 1 Claude: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`
- Round 1 Expert: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Gemini25_(topic).md`
- Round 2 Claude: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Claude_(topic).md`
- Round 2 Expert: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Gemini25_(topic).md`
- Final: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_FINAL_ASSESSMENT_(topic).md`

## When to Use
- Medium complexity problems
- Time constraints exist
- Need expert input but not exhaustive analysis
- Clear decision criteria exist

## When NOT to Use
- Highly complex architectural decisions (use collaborate3)
- Simple problems with obvious solutions
- Emergency fixes

## Comparison with Collaborate3
| Aspect | Collaborate2 | Collaborate3 |
|--------|-------------|--------------|
| Rounds | 2 + decision | 3 + assessment |
| Time | ~30-45 min | ~60-90 min |
| Depth | Good | Comprehensive |
| Best for | Clear problems | Complex issues |

Remember: Faster process, same critical thinking.