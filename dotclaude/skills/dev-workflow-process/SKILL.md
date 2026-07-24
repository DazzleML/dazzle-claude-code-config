---
name: dev-workflow-process
description: "Initiates a structured analysis of a problem using the DEV WORKFLOW PROCESS with specific contextual guidance."
allowed-tools: Bash, Read, Write, Glob, Grep, Task, AskUserQuestion, WebSearch, WebFetch
---

Your goal is to please apply the **DEV WORKFLOW PROCESS**, to the following problem.

# DEV WORKFLOW PROCESS (DWP) -- Structured Problem Analysis

**What this is.** The DEV WORKFLOW PROCESS (abbreviated "DWP" below) is a structured way to analyze a problem BEFORE building a solution: gather the facts/background, enumerate the problem/considerations, evaluate competing approaches, and synthesize a single recommendation -- all written to a durable markdown document so the reasoning (not just the conclusion) survives for future readers, human or AI. This file is **self-contained**: everything needed to run the process is defined here. No other project document is required to interpret it.

**When to use it:** any time multiple approaches exist, risk is non-trivial, or a decision shapes something others will build on -- architecture choices, public APIs, schemas, integrations, security-sensitive changes, multi-component features. (See "When a full DWP is required" near the end for the line between this and a quick question.)

## Context: "$ARGUMENTS"

Apply the process defined below to this problem:

**Problem Statement:** "$ARGUMENTS"

---

## The process at a glance

Four stages, each building on the last. (The stage nicknames Story/Puzzle/Content/Result come from the mnemonic **SPCR** -- [S]tory -> [P]uzzle -> [C]ontent -> [R]esult -- but you do not need to know anything beyond what is written here.)

| Stage | Nickname | Question it answers |
|---|---|---|
| 1. Problem Analysis | Story | What is actually being asked, and what is true right now? |
| 2. Considerations | Puzzle | What constraints, risks, and unknowns must any solution reconcile? |
| 3. Solutions Evaluation | Content | What are the candidate approaches, and how do they compare? |
| 4. Synthesis & Recommendation | Result | Which path do we take, why, and how will we know it worked? |

Two preliminary steps (0 and 0.5) shape how the four stages are written. The output is one timestamped markdown document (format at the end).

---

## Step 0: Declare the MODE (contractive vs expansive)

Before analyzing, declare which mode this analysis is in. The mode determines what shape Stage 4's Result must take -- and resolves a real tension: "make the Result testable" is the right default, but some analyses exist to map territory, not to converge.

- **`mode: contractive`** -- you are converging on a buildable decision. The Result MUST name its **acceptance checks**: the concrete tests, invariants, or measurable verifications the recommendation will be judged against once built. The acceptance checks are what make the analysis *chainable*: the next piece of work gets verified against them, so each analysis hands the following one its starting puzzle instead of a pile of prose. (Observed in practice: one analysis produced a reusable test harness as its Result; the next analysis validated its design against that harness; months later an unrelated design question was settled by simply *running* it. Three analyses chained through one testable artifact -- none of that happens if the Result is only prose.)

- **`mode: expansive`** -- you are mapping a territory: a multi-system synthesis, a philosophy/concept grounding, an audit of how several efforts relate. A single set of acceptance checks would be premature. The Result instead consists of: (a) **declared relationships and boundaries** ("mechanism A is NOT mechanism B; they compose but are distinct") -- not testable, but they prevent whole categories of future confusion -- and (b) **the named follow-up analyses this one spawns**, each a seeded contractive DWP. Expansion emits *multiple* next puzzles rather than one set of checks. Both modes chain; they chain differently.

- **`mode: both`**: it's also possible a DWP is both EXPANSIVE first and then CONTRACTIVE second internal to itself, this is an example of trying to VIEW the forest and then FIND the tree. The first expansive stage maps the territory and spawns contractive analyses for each candidate path; the second stage evaluates those paths and converges on one. This is a more complex DWP but it is a real pattern that comes up frequently. 

  Keep in mind when you choose "mode: both", more often than not, you should do TWO discrete dev-workflow-process (DWP) skill calls back-to-back, as two separate documents that are simply merged into a SINGLE DWP file. The first DWP should analyze the high-level EXPANSIVE aspects. Next the second DWP is the contractive-level. This means you should do an EXPANSIVE DWP {step 0.5, stage1, stage2, stage3, stage4} finalizing your high-level thoughts; and then segue into the more focused constricted bit of research as a separate CONTRACTIVE DWP as {step 5.5, stage6, stage7, stage8, stage9} synthesizing BOTH sequences in your final analysis. Note if you want to explore MANY "trees" in the forest that is DESIRABLE as even more additional DWP docs. When analyzing many "trees", the best strategy might be to fork and spawn the "dev-workflow-process" agent to analyze all the alternatives where each DWP-agent writes its own report. If the the number of DWPs get difficult to synthesize, read the Claude Code command `~/.claude/commands/collaborate3.md` and/or `~/.claude/skills/collabN-local` to get ideas on how to serialize long DWP analysis chains. The last step would be to generate a final DWP doc that synthesizes all the results to make the best choice amongst all the options. 

When unsure, default to either **both** or **contractive** -- expansive is the deliberate exception, chosen on purpose. 

Record the mode in TWO places (frontmatter alone is not enough -- readers skim the preamble, not YAML):

1. **Frontmatter:** `mode: both` / `mode: contractive` / `mode: expansive`.
2. **The document PREAMBLE (header block):** a visible `**Mode:**` line stating the mode AND a one-sentence rationale for HOW the analysis is being approached -- e.g. `**Mode:** both -- expansive first (does a renderer-contract reshape subsume the one-off fix?), then contractive (the chosen change + acceptance checks).` This tells every future reader what shape of Result to expect before they read a word of analysis.

Note: It's possible you might want a hybrid or custom "mode" that doesn't quite fit these patterns (that you come up with on the fly). That's fine -- the point of declaring the mode is to be intentional about how you write the Result, so if you deviate from these patterns, just be clear about what shape the Result will take and how it will chain to future work.


## Step 0.5: Ground truth FIRST

Before writing any analysis prose, produce a **Ground Truth** section: the verified facts, each backed by a specific citation (file and line number, command output, document reference) -- explicitly separated from beliefs, recollections, and assumptions. Run the reconnaissance (search, read, count, measure) BEFORE forming the narrative.

Why this ordering is load-bearing (observed in practice, twice):
- A classification table written from memory misstated a key property of one transition; the error stood until a human corrected it. The recon that would have caught it took minutes.
- Conversely, an analysis that opened with an exhaustive enumeration of every affected call site (a dozen lines of grep output) produced a synthesis decisive enough to approve in one pass.

If a claim in the analysis can be checked empirically in minutes -- **check it, don't assert it**. When the question is "what does the real population look like?" (how many instances exist, what shapes do they take), write a small throwaway experiment script and run it against ALL real instances in the project, not against synthetic examples. Keep the script (in whatever scratch/experiments location the project uses) and cite its output in Ground Truth; a measured population beats an argued hypothetical every time.

---

## Stage 1: Problem Analysis (Story)

- **Begin with the user's COMPLETE VERBATIM MESSAGE** that triggered this analysis -- the entire text in a code block, nothing skipped or summarized. Future readers need the unfiltered original, not your paraphrase of it.
- Summarize the request, the business/project context, and the background story.
- List known facts (cross-referenced to Ground Truth) and open uncertainties, with any tests needed to resolve them.
- State the goals and how success will be measured.

## Stage 2: Considerations (Puzzle)

Walk through all possible reasons and issues that could be at play. Identify everything a solution must reconcile. Cover, at minimum:

- **Files/components affected** -- the concrete blast radius.
- **Possible root causes** (for problem-driven analyses) -- brainstorm widely before narrowing.
- **Pros / Cons / Neutral facts** for the situation as it stands.
- **Edge cases** -- unusual scenarios needing special handling.
- **Long-term implications** -- technical debt, future features this constrains or enables.
- **Adjacent systems** -- what else is touched, even indirectly.
- **Known-unknowns and potential unknown-unknowns** -- what you cannot yet see, and what experiment would reveal it.

It's often best to do this both as a narrative and a bulleted list, so we can think about both the breadth of considerations and the reasoning behind the problems / issues we identify.

## Stage 3: Solutions Evaluation (Content)

For EACH candidate approach (aim for genuinely distinct alternatives, not strawmen). Aim for about 4-6 possible candidates (less is okay if there are truly less), but if there are more we want to be exhaustive and list all of them. The goal is to explore the space of ALL possibilities before converging on a single recommendation. For each we need to establish the:

- **Strengths** / **Weaknesses**
- **Edge cases** where this approach fails or degrades
- **Ripple effects** on adjacent systems and long-term maintenance
- **Future considerations** -- how it scales, evolves, or blocks later work
- Any other relevant trade-offs (cost, complexity, migration burden, team familiarity)

Like with the "Stage 2: Puzzle", we should have a detailed thoughtful narrative and bulleted list for each candidate that aims to solve the issue(s), so we can think about both the breadth of considerations and the reasoning behind them.

This section should be one of the most robust as it explores the possible ways to address the the desired result. We can't make a good choice about which option to choose (or which hybrid solution as a mix of the possible options) unless we truly detail each so we can see how they weigh when compared side-by-side.

## Stage 4: Synthesis & Recommendation (Result)

Choose the single best path (or a mix of the given options) and give the **why** -- the rationale, grounded in Stages 1-3. The synthesis shouldn't pretend to be a fail-proof "recipe", but rather should discuss nuances and all considerations, including how things can go sideways and what to look out for. Provide a strong narrative explanation and also include an ordered **build-step list** (each step independently verifiable where possible) while using the correct strength of wording (like the CIA's words of estimative probability) recognizing steps may not be complete and what to test.
- Per Step 0's mode:
  - *Contractive*: name the **acceptance checks** -- the tests/invariants/measurements each build step will be verified against.
  - *Expansive*: list the **declared relationships** and the **spawned follow-up analyses**.
- Include risk mitigations for the chosen path.
- Close with a **PUVM summary** -- one row or short paragraph or two capturing: **P**hilosophy (what belief or intention drives this choice), **U**tility (what it functionally does), **V**alue (why it is worth doing as compared to other options), **M**arketing (the internal appeal of this option, whether for aesthetic reasons, or the soft-sell for why this choice stands out). The Philosophy entry often matters most: state the *intention* behind the design, because future conflicts are usually intention mismatches, not code mismatches.

## The Decision Ledger (rejected and deferred alternatives)

Every rejected or deferred alternative gets an entry recording **the condition that would reopen it** -- e.g., "defer the typed wrapper -> reopen when feature X starts *writing* this data and the real population materializes." A deferral without a trigger is a decision that will be re-litigated from scratch by someone who cannot tell whether it was considered; a deferral WITH a trigger is a pre-seeded puzzle for a future analysis. For deferrals that matter beyond this document, mirror the entry to the project's issue tracker (a comment on the issue where the trigger lives), so it survives outside private notes.

## Verbatim corrections become test cases

If the user corrects the analysis (a misclassification, a wrong assumption), carry the correction **verbatim** in the document AND map it to at least one acceptance criterion or test in the Result. A correction that only updates prose can silently regress; a correction that became a named test cannot. (Observed in practice: a user's correction about whether an operation was reversible became a literal test case in the shipped suite -- that is the standard.)

---

## Document output

Write the complete analysis to a new markdown file:

- **Location:** the project's private analysis folder if one exists (e.g., `./private/claude/`); otherwise the user's general notes folder; otherwise alongside the project with a clear name.
- **Filename:** `YYYY-MM-DD__hh-mm-ss__(topic).md` -- generate the timestamp by actually running `date +%Y-%m-%d__%H-%M-%S` (never guess the time), with a short descriptive `(topic)` slug.
- **Frontmatter:** include at least `type: dev-workflow-process`, `date`, `mode:` (from Step 0), and `status: design` (see next section for how status evolves).

Normally, hold off on implementation until the plan is approved -- unless told otherwise.

## After the build ships: the Outcome Addendum

A DWP document is not finished when the analysis is approved -- it is finished when reality has answered it. When the recommendation is implemented, **append an Outcome addendum** to the document: the commit hash(es), the acceptance checks' actual results (test counts, gate outputs, measurements), and any deviation from the plan with its reason. Update the frontmatter `status:` through its lifecycle: `design` -> `implemented` -> `verified`. This closes the loop empirically -- the document stops being a frozen plan and becomes a record of what the design DID -- and makes "which designs actually shipped" answerable by grep. Without this, every analysis says `status: design` forever and the chain of evidence breaks.

## When a full DWP is required vs when a quick question suffices

A quick multiple-choice question to the user (2-4 options with trade-off descriptions) is appropriate for **mechanism** choices inside an already-settled design: which helper shape, which file layout, which of two equivalent idioms. It is NOT sufficient for anything that shapes a **public or durable contract**: API surfaces, schema/data formats, persistence layouts, security/trust boundaries, anything other code or other people will build against. Those require the full process. (Observed in practice: a public-contract decision made via a quick prompt under deadline momentum had to be completely re-analyzed days later -- and the re-analysis found a real data-loss bug the quick decision had sailed past. The quick path saved an hour and cost a day.)

## Notes

- If appropriate use research/consultation agents like the oracle-agent or the senior-engineer agent or the brainstorm-agent. Use them for reconnaissance: a project-knowledge oracle agent (design-doc/decision history) for "why is it this way"; a codebase-search agent when the problem spans many files; a senior-engineer agent for deep technical consultation on architectural trade-offs. **Always make the final call yourself and verify details yourself** rather than trusting any agent's report implicitly.
- The analysis document must always include the user's complete verbatim trigger message at the top (no exceptions -- the entire original text, not an abridged version).

## Background vs. Inline Usage

- **Inline (this skill):** `/dev-workflow-process <problem>` -- runs in the active session; results are part of the conversation context. Use when you want to discuss and iterate on the analysis.
- **Background (agent):** This is a *RARE* case and should NOT be the default pathway -- only use when we truly do not need any information from our current discussion. If your environment provides a `dev-workflow-process` agent like `dwp-background`, it can be spawned in the background to produce the document without consuming main-session context; it writes the document to disk and returns the file path. Use when the analysis is self-contained enough to not need mid-flight discussion. 
