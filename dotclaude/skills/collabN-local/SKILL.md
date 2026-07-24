---
name: collabN-local
description: "Run an N-round expert consultation with one of our own sub-agents (default: brainstorm) that has repo access -- like collaborate3, but the consultant can read the code, trace design docs, and run real tests. Spawn once, continue via SendMessage each round; saves 2N+1 verbatim round files plus an independent dev-workflow final assessment. N defaults to 3."
---

# collabN-local Skill - N-Round Local-Agent Consultation

## Purpose
Run the `collaborate3` consultation pattern entirely **in-house**: instead of consulting an external model (Gemini 2.5 Pro via Zen/OpenRouter), consult one of **our own sub-agents** (`brainstorm`, `senior-engineer`, `oracle`, `Explore`, etc.).

The decisive advantage over the external `collaborate*` commands: a local agent **has the files**. It can read the actual code, trace design docs and postmortems, and run real tests — none of which the external expert could ever do. You are effectively holding a structured, multi-round technical review *with a second instance of yourself that can see the repo*.

`N` is the number of consultation rounds (default **3**), always followed by one independent final assessment (Round `N+1`). **This command works exactly like `collaborate3`, with two swaps: the consultant is a local agent instead of Gemini, and the continuity handle is the agent's `agentId` + `SendMessage` instead of a Zen `continuation_id`. Everything else — the per-round files, the verbatim saving, the critical analysis, the independent final assessment — is identical.**

## Invocation & Arguments
```
/collabN-local [N] [agent] <topic / problem statement>
```
- **`N`** (optional integer) — number of consultation rounds. **Default `3`.** If omitted, assume 3 (do not block to ask).
- **`agent`** (optional) — which sub-agent to consult. **Default `brainstorm`.** Recognized values map to the Agent tool's `subagent_type`:
  - `brainstorm` — **default.** Thought-partner that blends the senior-engineer's hands-on judgment with the oracle's doc/knowledge tracing, runs tests against the real repo, and delegates to either specialist when a sub-question is squarely theirs. Best general-purpose consultant for this command.
  - `senior-engineer` — pure expert-engineering role; architecture, debugging, hands-on fixes.
  - `oracle` — for "how/why does this work" questions; traces design docs, postmortems, MOCs, issues, git history with sourced citations.
  - `Explore` — read-only "where is X / what calls Y" codebase mapping; lighter weight, cannot run tests or edit.
  - any valid agent type (`Plan`, `investigate`, `general-purpose`, …) is also acceptable.
- **`<topic>`** — the problem/decision. If omitted, use the current conversation as the topic.

**Parsing rule:** if the first token is an integer, it's `N`; if the next token matches a known agent type, it's `agent`; the remainder is the topic.

Examples:
- `/collabN-local 3 "export/import column alignment is off"` → 3 rounds with `brainstorm`.
- `/collabN-local oracle "why does the clone formula use MIN not subtraction"` → 3 rounds (default) with `oracle`.
- `/collabN-local 2 Explore "where is widget serialization handled"` → 2 rounds with `Explore`.
- `/collabN-local 1 "is asyncio.gather or create_task better here"` → 1 round (quick) with `brainstorm`.

## MANDATORY OUTPUT CONTRACT — read this before you start
**This command is defined by the files it leaves on disk, exactly like `collaborate3`.** A run that produces only a final synthesis has **FAILED**, no matter how good the analysis was. As you go, you MUST write:
- one **Claude message** file per round (what you sent the agent), and
- one **agent response** file per round (the agent's reply, saved **VERBATIM**), and
- one **final assessment** file.

For the default 3-round run that is **7 files** (3 Claude + 3 agent + 1 final). For `N` rounds it is **`2N + 1` files**.

> **⚠️ THE TRAP THAT BREAKS THIS COMMAND.** Unlike Gemini — whose replies arrive via `mcp__zen__chat` and exist *nowhere else*, forcing you to save them — a local sub-agent's reply arrives as an `Agent`/`SendMessage` **tool result that is already sitting in your context**. That makes it *feel* saved. **It is NOT saved.** You must write the file anyway, every round, before moving on.
>
> **Hard gate:** treat each round's two files as a barrier — **do not begin round `k+1` until round `k`'s Claude-message file AND agent-response file both exist on disk.** Do not batch all the file-writing to the end. Write the agent's response immediately after each spawn/`SendMessage` returns, verbatim, the same way you would for Gemini.

## Consultant mechanism (the local analog of `continuation_id`)
To hold a real multi-round conversation with one agent, **spawn it once and keep talking to the same instance** so its context persists across rounds:

1. **Round 1 — spawn:** call the `Agent` tool with `subagent_type: <agent>` (consider `run_in_background: true` so you get a stable `agentId` to resume). Capture the returned **`agentId`** (format `a...-...`) — this is your continuation handle; record it at the top of every response file.
2. **Rounds 2..N — continue:** use **`SendMessage(to: <agentId>, message: <next round>)`** to resume the *same* agent with its context intact. A fresh `Agent` call would start from zero and defeat the purpose.

**Fallback (if resuming isn't available in this harness build):** spawn a fresh agent each round but embed the **verbatim transcript of all prior rounds** (read it back from the round files you saved) so it reconstructs context. This is exactly what external `collaborate3` does with Gemini, so it is a safe degradation — just more tokens. Note in the response file that you fell back.

## Process Overview
Three rounds of exchange followed by final assessment (this is the default `N=3` shape; see *Adapting to other N* below):
- Round 1: Present complete context, get initial analysis
- Round 2: Critical evaluation, probe weaknesses, run real tests, test viability
- Round 3: Final questions and proposed action plan
- Round 4: Independent final assessment using dev-workflow-process

## Detailed Steps

### Preparation
Gather all relevant context: problem description, the files/dirs involved (point the agent at real paths — it can open them), previous attempts and failures, current understanding, constraints, and the specific questions needing answers.

### Round 1: Context & Initial Analysis
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_Claude_(topic).md`) — write this file:
   - Complete overview of the problem and relevant code structure (real paths).
   - Work attempted so far and why it failed.
   - Specific questions; request simple/quick vs. robust vs. long-term options plus considerations and future implications.
   - If the agent is NOT `brainstorm`, paste in the **anti-echo-chamber standing instructions** (below). `brainstorm` already has them baked in.
2. **Spawn the agent** via the `Agent` tool (`subagent_type: <agent>`); capture its **`agentId`**.
3. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd1_(Agent)_(topic).md`) — **write this file now, before doing anything else.** The reply is already in your context; save it to disk anyway.
   - Save the agent's response **VERBATIM** — no editing or summarizing.
   - **CRITICAL:** record the **`agentId`** and **agent type** at the very top (the local `continuation_id`). Format:
     ```markdown
     # Consultant Response - [Topic]

     **AGENT_ID**: [a...-...]
     **AGENT_TYPE**: [brainstorm | senior-engineer | oracle | ...]
     **ROUND**: 1 of N

     ---

     [Full verbatim response]
     ```
4. **Critical analysis** (internal): categorize each suggestion Good / Neutral / Problematic; note effects on other code/data; identify weak points to probe.

### Round 2: Critical Evaluation & Testing
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_Claude_(topic).md`) — write this file:
   - DO NOT blindly accept suggestions. Present your own analysis of the proposals.
   - **Run real local tests** for anything the agent asked you to validate, and include the actual output/data — use the scientific method to *falsify* ideas. (You can also ask the agent to run its own diagnostics, since it has tools; cross-check the two.)
   - Ask probing questions about weak points, challenge assumptions, explore edge cases.
2. **Continue the same agent** via `SendMessage(to: <agentId>, message: <this message>)` (fallback: re-spawn with full prior transcript embedded).
3. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd2_(Agent)_(topic).md`) — **write this file now**, VERBATIM, with `AGENT_ID` and `ROUND: 2 of N` at the top.
4. **Deep analysis** (internal): re-evaluate proposals against the new data; form preliminary conclusions.

### Round 3: Final Questions & Action Plan
1. **Prepare message** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_Claude_(topic).md`) — write this file:
   - DO NOT blindly accept Round 2 feedback. Present YOUR assessment and reasoning.
   - Ask remaining clarifying questions.
   - Propose YOUR action plan (not the agent's) and request validation of specific concerns.
2. **Continue the same agent** via `SendMessage(to: <agentId>, message: <this message>)`.
3. **Save response** (`YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd3_(Agent)_(topic).md`) — **write this file now**, VERBATIM, with `AGENT_ID` and `ROUND: 3 of N` at the top.

### Round 4: Final Assessment (Independent)
Create `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd4_FINAL_ASSESSMENT_(topic).md` using the full **DEV WORKFLOW PROCESS**:
- Problem Analysis (*SPCR: Story*)
- Considerations Analysis (*SPCR: Puzzle*)
- Solutions Evaluation (*SPCR: Content*)
- Synthesis & Recommendation (*SPCR: Result + PUVM*)
- YOUR decision, informed by but not dictated by the consultant. Include risks and mitigations.

### Adapting to other N
The four blocks above are the standard `N=3` walk. For other values, keep Round 1 (context) and make the **last consultation round** the "final questions & action plan" round; the Final Assessment is **always Round `N+1`**:
- **N=1:** Round 1 → Final Assessment is Round 2. (3 files total.)
- **N=2:** Round 1, then Round 2 = "final questions & action plan" → Final Assessment is Round 3. (5 files.)
- **N=3:** as written above. (7 files.)
- **N≥4:** Round 1, then repeat the **Round 2 (critical evaluation & testing)** pattern for rounds `2..N-1`, then Round `N` = "final questions & action plan" → Final Assessment is Round `N+1`. (`2N+1` files.)

In **every** case the deliverable is `2N+1` files: `N` Claude-message files, `N` verbatim agent-response files, and 1 final assessment.

### Closeout checklist (do this before declaring done)
List the files you created and confirm the count is `2N+1`. If any round's two files are missing, you have not finished — go back and write them. Example for `N=3`:
```
[x] DISCUSS_Rnd1_Claude_(topic).md
[x] DISCUSS_Rnd1_(Agent)_(topic).md
[x] DISCUSS_Rnd2_Claude_(topic).md
[x] DISCUSS_Rnd2_(Agent)_(topic).md
[x] DISCUSS_Rnd3_Claude_(topic).md
[x] DISCUSS_Rnd3_(Agent)_(topic).md
[x] DISCUSS_Rnd4_FINAL_ASSESSMENT_(topic).md   → 7 files = 2(3)+1 ✓
```

## Anti-echo-chamber: the consultant's standing instructions
Because the sub-agent is also Claude, the value comes from *structure and framing*, not from a different model. The default **`brainstorm`** agent already bakes the rules below into its persona — when you use it, you mainly pass context + the round number. When you point the command at a *different* agent (`senior-engineer`, `Explore`, etc.), paste these instructions into the round prompt. Every round's prompt to the agent must instruct it to:
- Act as an **independent, skeptical reviewer** — its job is to find what's wrong, not to agree.
- **Read the actual files** before opining; cite `file:line`, don't speculate.
- **Disagree explicitly** with the main thread's framing when warranted, and say *why*.
- Offer **simple/quick vs. robust vs. long-term** options and name the trade-offs.
- When it proposes something testable, **run the test itself** (if it has tools) and report real output — or specify the exact test for Claude to run.
- Flag assumptions and unknowns rather than papering over them.

## Key Principles
1. **Document everything as you go** — full verbatim records, written to disk each round. The in-context tool result is not a substitute for the file. This is the principle this command most often violates; honor it.
2. **Critical thinking over compliance** — the agent is a sparring partner, not an oracle of truth; challenge everything.
3. **Test before trust** — validate suggestions against the real repo and real test output. This is the whole point of going local.
4. **Persist the same agent** — reuse the `agentId` so context carries across rounds; never silently start a fresh agent mid-consultation.
5. **Independent decision** — you make the final call in Round `N+1`.
6. **Beware the echo chamber** — a same-model consultant tends to agree; force genuine adversarial framing.

## File Naming Convention
All files in `./private/claude/` (project work) or `~/claude/` (cross-project), matching the other collaborate commands. Use a short PascalCase token for `(Agent)` — e.g. `Brainstorm`, `SeniorEng`, `Oracle`, `Explore`:
- Round k (Claude): `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd{k}_Claude_(topic).md`
- Round k (Agent): `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd{k}_(Agent)_(topic).md`
- Final: `YYYY-MM-DD__hh-mm-ss__DISCUSS_Rnd{N+1}_FINAL_ASSESSMENT_(topic).md`

(Always run `date` to get the real timestamp for filenames.)

## Example Usage
```
User: "We need to solve the export/import column alignment issue. Use collabN-local with 3 rounds."

Claude:
1. Writes Rnd1_Claude (context) → spawns brainstorm → writes Rnd1_(Agent) VERBATIM (agentId saved)
2. Runs the failing case, writes Rnd2_Claude (analysis + test output) → SendMessage(agentId) → writes Rnd2_(Agent) VERBATIM
3. Writes Rnd3_Claude (own action plan) → SendMessage(agentId) → writes Rnd3_(Agent) VERBATIM
4. Writes Rnd4_FINAL_ASSESSMENT (dev-workflow-process, YOUR decision)
5. Closeout: confirms 7 files exist
```

## When to Use
- You want the `collaborate3` rigor but the consultant **needs to actually see/run the code**.
- Offline / no external API, or you want to avoid OpenRouter cost and dependency.
- The question is repo-specific (architecture, debugging, "how does X connect to Y", "why was this designed this way").

## When NOT to Use
- You specifically want an **outside, different-model perspective** to avoid groupthink — use `collaborate3` (external Gemini) instead; that's the one thing a local agent can't give you.
- Trivial problems with obvious solutions, or pure-syntax lookups.

## Relationship to the collaborate family
| Command | Rounds | Consultant | Repo access |
|---------|--------|------------|-------------|
| collaborate1 | 1 + decision | External (Gemini 2.5) | No |
| collaborate2 | 2 + decision | External (Gemini 2.5) | No |
| collaborate3 | 3 + assessment | External (Gemini 2.5) | No |
| **collabN-local** | **N + assessment** | **Local sub-agent** | **Yes** |

| PUVM | Summary |
|------|---------|
| Philosophy | Rigorous review doesn't require an outside model — it requires *structure* and an opponent who can read the actual code; we can be our own adversarial expert. |
| Utility | N-round, file-aware, test-backed consultation with a persistent local agent, ending in an independent DEV-WORKFLOW decision. |
| Value | Same critical-thinking discipline as collaborate3, but grounded in the real repo and free of external-API cost/latency/dependency. |
| Marketing | "collaborate3, but the expert has the keys to the codebase." |

Remember: the local agent provides input and can prove things against the real repo — but **YOU** make the decision, and you must actively guard against it simply agreeing with you. And **the run is only complete when all `2N+1` files exist on disk.**
