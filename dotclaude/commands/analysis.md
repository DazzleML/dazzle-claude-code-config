---
description: Intelligence-style assessment of actors, motivations, situations, or claims. Uses CIA estimative language and PUVM to evaluate what's happening, why, and how to respond.
allowed-tools: Bash, Write, Read, WebFetch, WebSearch, Grep, Glob
---

# Intelligence Estimate: Structured Assessment

Perform a structured intelligence-style assessment of the following situation, actor, or claim.

**Subject:** "$ARGUMENTS"

## Framework

This analysis uses three integrated frameworks:

### 1. Words of Estimative Probability (WEP)

Use precise probabilistic language throughout. Every judgment must use one of these calibrated phrases:

| Phrase | Probability | When to Use |
|--------|-------------|-------------|
| **Almost certainly / Nearly certain** | 95-99% | High-quality evidence from multiple corroborating sources |
| **Very likely / Highly probable** | 80-95% | Strong evidence with minor gaps |
| **Likely / Probable** | 55-80% | Preponderance of evidence supports this |
| **Roughly even chance** | 45-55% | Evidence is balanced or ambiguous |
| **Unlikely / Improbable** | 20-45% | Evidence leans against, but can't rule out |
| **Very unlikely / Highly improbable** | 5-20% | Little evidence supports this |
| **Almost certainly not / Remote** | 1-5% | Would require extraordinary circumstances |

**Rules:**
- Never use "possible" alone — everything is "possible." Specify likelihood.
- Never say "may" or "might" without a WEP qualifier (e.g., "likely may" → just say "likely")
- "We cannot rule out" = acknowledging a remote scenario worth mentioning despite low probability
- Always pair WEP language with the reasoning that drives the estimate

### 2. Analytic Confidence Levels

Rate overall confidence in the assessment:

| Level | Meaning |
|-------|---------|
| **High** | Multiple trustworthy sources, minimal conflict, solid analytical basis |
| **Moderate** | Credible sources, plausible conclusions, but insufficient corroboration or some conflicting signals |
| **Low** | Sparse, fragmented, or poorly corroborated information; conclusions are tentative |

### 3. PUVM Framework (Philosophy, Utility, Value, Marketing)

Apply PUVM to understand the subject's motivations and the situation's dynamics:

- **Philosophy (P)**: Why does this exist? What belief or intention drives the actor/claim/situation? What worldview or assumption is operating?
- **Utility (U)**: What function does it serve? What does it actually DO for the actor or audience?
- **Value (V)**: How is it weighed against alternatives? What's the comparative worth — what's gained and what's sacrificed?
- **Marketing (M)**: Why does it resonate or appeal? What's the inherent draw that makes this attractive to the actor or their audience? (Not just external promotion — the internal "cool factor" or identity signal)

## Analysis Structure

### I. Situation Summary
- State the situation clearly and concisely
- Identify all actors, their known positions, and the context
- Note the triggering event or question

### II. Key Judgments
Present 3-7 key analytical judgments, each formatted as:

> **[JUDGMENT TITLE]** (WEP: [phrase], Confidence: [level])
>
> [1-3 sentence assessment with reasoning]
>
> *Evidence basis: [what supports this]*
> *Counter-indicators: [what argues against, if any]*

### III. Actor PUVM Analysis
For each significant actor, construct their PUVM:

| | Actor A | Actor B | ... |
|---|---------|---------|-----|
| **Philosophy** | What they believe / their intention | | |
| **Utility** | What this does for them | | |
| **Value** | What they gain vs. sacrifice | | |
| **Marketing** | Why this appeals to them / their self-image | | |

Include 1-2 paragraphs on the **intention** behind each actor's behavior — what problem are they trying to solve for themselves? How does their worldview shape their actions?

### IV. Claims Assessment
For each factual claim made by any party, evaluate:

| Claim | Assessment | WEP | Evidence |
|-------|------------|-----|----------|
| "[exact claim]" | True / Misleading / False / Unverifiable | [probability phrase] | [basis] |

### V. Alternative Hypotheses
List at least 2-3 alternative explanations for the situation, ranked by likelihood:

1. **[Most likely hypothesis]** (WEP: [phrase]) — [reasoning]
2. **[Second hypothesis]** (WEP: [phrase]) — [reasoning]
3. **[Least likely but worth considering]** (WEP: [phrase]) — [reasoning]

Explicitly note which hypothesis you'd need to discard and what evidence would cause you to revise your estimates.

### VI. Strategic Assessment
- **What's actually happening here?** (Cut through noise to the core dynamic)
- **What does each actor want?** (Stated vs. actual goals)
- **What are the second-order effects?** (What happens next, regardless of action taken)
- **What information would change this assessment?** (Key unknowns that matter)

### VII. Recommended Response (if applicable)
If the situation calls for a response:
- **Recommended action** with rationale
- **Tone and framing** guidance
- **What NOT to do** (common mistakes)
- **Escalation/de-escalation** considerations
- **Success criteria** — how do you know the response worked?

### VIII. Assessment Metadata
| Field | Value |
|-------|-------|
| **Overall Confidence** | High / Moderate / Low |
| **Information Gaps** | What we don't know that matters |
| **Shelf Life** | How long this assessment stays valid before needing update |
| **Revision Triggers** | What new information would change key judgments |

## Output

Write the analysis to a markdown file:
- **Location**: Project's `./private/claude/` if available, otherwise `~/claude/`
- **Filename**: `YYYY-MM-DD__hh-mm-ss__analysis_(topic).md` (generate timestamp with `date +%Y-%m-%d__%H-%M-%S`)
- Keep the analysis focused and actionable — intelligence estimates are concise by design
- Use tables and structured formatting for scanability
- Bold all WEP phrases in running text so probability language stands out

## When to Use This Command

- Evaluating someone's motivations or claims (online interactions, business dealings, negotiations)
- Assessing a situation with incomplete information where you need structured reasoning
- Understanding why someone did something and predicting what they'll do next
- Analyzing competing narratives to determine which is most credible
- Any situation where "what's really going on here?" is the core question

## When NOT to Use

- Pure technical/code problems (use `/dev-workflow-process`)
- Simple factual questions with clear answers
- Situations where you have complete information and no ambiguity
