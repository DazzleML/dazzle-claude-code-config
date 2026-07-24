# Collaborate3 Command - Three-Round Expert Consultation

## Purpose
Structured 3-round consultation with an AI expert (Gemini 2.5 Pro or similar) for complex technical decisions, ensuring critical analysis rather than blind acceptance of suggestions.

## Process Overview
Three rounds of exchange followed by final assessment:
- Round 1: Present complete context, get initial analysis
- Round 2: Critical evaluation, probe weaknesses, test viability
- Round 3: Final questions and proposed action plan
- Round 4: Independent final assessment using dev-workflow-process

## API Key Usage
**CRITICAL**: Always try in this order:
1. First attempt: Use `GEMINI_API_KEY` (free usage quota)
2. If GEMINI fails: Fallback to `OPENROUTER_API_KEY`
3. Document which API was used in the response file

## Detailed Steps

### Preparation
1. Gather all relevant context:
   - Problem description
   - Code files involved
   - Previous attempts and failures
   - Current understanding
   - Constraints and requirements

### Round 1: Context & Initial Analysis
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`):
   - Complete overview of the problem
   - All relevant code structure
   - Work attempted so far
   - Specific questions needing answers
   - Request for simple/quick solutions vs. robust solutions vs. longterm solutions vs other possible factors as solutions
   - Request for considerations and future implications

2. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Gemini25_(topic).md`):
   - Save expert's response VERBATIM
   - No editing or summarizing
   - **CRITICAL**: Save the Zen MCP continuation_id at the top of the file for future reference

3. **Critical analysis** (internal):
   - Categorize each suggestion: Good / Neutral / Problematic
   - Note surrounding factors
   - Consider effects on other code/data
   - Identify weak points to probe

### Round 2: Critical Evaluation & Testing
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Claude_(topic).md`):
   - DO NOT blindly accept suggestions
   - Present your own analysis of proposals
   - IMPORTANT: If possible run local tests and perform any tasks Gemini 2.5 asks you to do, to find out definitively whether something works or if more information is necessary for Gemini to make a good decision. The key point is we should be doing real-live tests at this stage and collecting data for Gemini.
   - Ask probing questions about weak points
   - Request test strategies to validate ideas (using the scientific method to falsify ideas)
   - Challenge assumptions
   - Explore edge cases

2. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Gemini25_(topic).md`):
   - Save VERBATIM
   - **CRITICAL**: Save the continuation_id at the top of the file for future reference

3. **Deep analysis** (internal):
   - Re-evaluate all proposals
   - Consider new information
   - Form preliminary conclusions

### Round 3: Final Questions & Action Plan
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_Claude_(topic).md`):
   - DO NOT blindly accept Round 2 feedback
   - Present YOUR assessment and reasoning
   - Ask remaining clarifying questions
   - Propose YOUR action plan (not theirs)
   - Request validation of specific concerns

2. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_Gemini25_(topic).md`):
   - Save VERBATIM
   - **CRITICAL**: Save the continuation_id at the top of the file for future reference

### Round 4: Final Assessment (Independent)
Create `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd4_FINAL_ASSESSMENT_(topic).md`:
- Use full DEV WORKFLOW PROCESS
- Problem Analysis (*SPCR: Story*)
- Considerations Analysis (*SPCR: Puzzle*)
- Solutions Evaluation (*SPCR: Content*)
- Synthesis & Recommendation (*SPCR: Result + PUVM*)
- YOUR decision, informed by but not dictated by expert input

## Key Principles
1. **Critical thinking over compliance** - Challenge everything
2. **Test before trust** - Validate all suggestions
3. **Your judgment matters** - You make the final call
4. **Document everything** - Full verbatim records
5. **Structured analysis** - Use frameworks consistently

## File Naming Convention
All files in `~/claude/` or `./private/claude/`:
- Round 1 Claude: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`
- Round 1 Expert: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Gemini25_(topic).md`
- Round 2 Claude: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Claude_(topic).md`
- Round 2 Expert: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Gemini25_(topic).md`
- Round 3 Claude: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_Claude_(topic).md`
- Round 3 Expert: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_Gemini25_(topic).md`
- Final: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd4_FINAL_ASSESSMENT_(topic).md`

## Example Usage
```
User: "We need to solve the export/import column alignment issue. Use collaborate3 with Gemini 2.5 Pro."

Claude: 
1. Prepares comprehensive context
2. Sends Round 1 to Gemini
3. Critically analyzes response
4. Challenges weak points in Round 2
5. Forms independent action plan in Round 3
6. Creates final assessment with YOUR decision
```

## When to Use
- Complex architectural decisions
- Multiple viable approaches exist
- Previous attempts have failed
- High-risk changes
- Need expert validation but maintain autonomy

## When NOT to Use
- Simple problems with clear solutions
- Time-critical issues
- Well-documented standard practices
- Problems you fully understand

Remember: The expert provides input, but YOU make the decision based on critical analysis and testing.