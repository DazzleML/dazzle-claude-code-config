---
name: double-check
description: "Exhaustively validate every claim, number, calculation, code-fact, and command in a document or outbound communication. Extracts all claims into a prioritized ledger (flagging what is NOT covered), validates each by the right method (run the math, run the command, cite the file:line, quote the primary source), then calibrates certainty with CIA Words of Estimative Probability and a provenance tier — and proposes corrected, properly-hedged rewrites for any overclaim. Use before sending a message, filing an issue, committing analysis, or whenever you state exact numbers/assertions others will rely on."
allowed-tools: Bash, PowerShell, Read, Write, Edit, Grep, Glob, WebFetch, WebSearch, AskUserQuestion
---

# DOUBLE-CHECK — Exhaustive Claim Validation

*(working title during design: CHECK-THE-NUMBERS)*

## Target: "$ARGUMENTS"

Validate the claims in the target (a file path, a draft message, a section of analysis, or pasted text). The goal is to ensure we **are not overstating, understating, or fibbing** — and to say *how true* each claim is in calibrated terms.

## Three operating beliefs (the whole skill in one breath)
1. **A claim is only as strong as its provenance.** "I'm pretty sure" is not a source.
2. **Completeness must be proven, not implied.** If we didn't check something, we say so — out loud, in a list.
3. **Certainty must be stated, not assumed.** Every judgment gets a calibrated probability word, never a bare "possible" or unqualified "may."

## When to run it
- Before sending an external communication (issue reply, email, PR comment, docs).
- Before relying on your own analysis to make a decision (internal mode).
- Any time the text contains EXACT numbers, registry/config values, code behavior claims, shell commands, or definitive factual assertions.
- As the Ground-Truth engine for a `/dev-workflow-process`.

## Modes
- **internal** — validating our own work before we trust it. Emphasis: catch unverified numbers and inference-as-fact.
- **external** — validating something we will send. Everything in internal, PLUS grade tone/overclaim and propose hedged rewrites the recipient will read.

Default to **external** when the target is addressed to anyone but us.

---

# Phase 1 — EXTRACT (the prioritized sweep)

Read the target and pull **every** claim into a **claim ledger** file. Do not validate yet — just find and catalog, so nothing is missed.

**Ledger location:** `private/claude/thinking/claims_<slug>.md` — a **PRIVATE, gitignored** scratch area. Claim ledgers and validation scratch are tied to our private notes/process; they're opaque and not useful to the wider public, so they must NOT land in `tests/one-offs/` (which is public and committed). If a project has no `private/claude/`, fall back to the user's private notes folder (e.g. `~/claude/private/thinking/`). Reserve `tests/one-offs/` only for scratch that genuinely illuminates the codebase for others.

**Sweep in value-tiered passes — highest value first. This is the bound that stops the sweep from degrading into sentence-particles:**

| Tier | What | Coverage rule |
|---|---|---|
| **T1 — Definitive numeric** | Exact numbers, intervals, counts, percentages, versions, sizes ("every 15 seconds", "default is 8", "260 insertions", "fd00::/8") | **Exhaustive** — every one, no exceptions |
| **T2 — Definitive code / command / config** | "sets `X`", "binds to `::`", a shell command + what its prose says it does, registry values, file:line behavior | **Exhaustive** |
| **T3 — Definitive factual assertions** | Causal/mechanism claims, "X causes Y", attributions, "Windows downgrades to local network" | **By section** — sweep each section; log any section skipped |
| **T4 — Soft/qualitative** | Hedged opinions, framing, subjective characterizations | **On request only** — do not sweep by default |

**Stopping rule:** finish T1 and T2 completely; do T3 section-by-section; touch T4 only if asked. **Log the boundary you stopped at.**

**Every ledger MUST end with a Coverage Ledger:**
```
## Coverage Ledger
- COVERED:        T1 (all N), T2 (all M), T3 (sections: …)
- NOT YET COVERED: T3 (section X — deferred), T4 (all — not requested)
- OUT OF SCOPE:   <things deliberately excluded and why>
```
Never produce output that implies coverage you did not achieve. The "NOT YET COVERED" list is mandatory even when empty (say "none").

---

# Phase 2 — VALIDATE (per claim type, with the right instrument)

For each ledger claim, pick the method by type. **Validate against reality, don't re-assert from memory.**

| Claim type | How to validate |
|---|---|
| **Numeric / calculation** | Write a throwaway script in `private/claude/thinking/*.py` (private scratch — see Ledger location) and RUN it. A computed number beats an argued one. |
| **Code / registry / config** | Cite the exact `file:line` (read it), or run the code path. For registry/config values, read the live value. |
| **Command** | **Execute it** and confirm it does what the surrounding prose claims — not just that it runs, but that its *output matches the stated intent*. (E.g. a command claimed to "show whether you have a global address" must actually surface that.) |
| **Factual assertion** | Find a **primary source** and quote it **verbatim**. Distinguish primary docs from secondary/community sources from your own inference. |

## HOST-SAFETY CONTRACT (non-negotiable)
- **Read-only by default.** `Get-*`, `... show ...`, `--dry-run`, pure computation: run freely.
- **Mutation requires:** (1) a backup/snapshot first, (2) a written reversal step, (3) an explicit flag in the output that state was changed. Prefer `dz safedel` over destructive deletes.
- **If validating a claim would itself be destructive or irreversible** (e.g. "this registry write fixes X"): **do NOT auto-run it.** Mark it "requires live mutation to verify — not auto-run" and propose a reversible test plan for human approval.
- Never run a command whose effect you cannot predict and undo.

Record, per claim: the method used, the evidence (script output / `file:line` / command output / verbatim quote), and the source link.

---

# Phase 3 — CALIBRATE (two independent axes)

Grade every validated claim on **both** axes. They are not the same thing: a claim can be from a primary source (high provenance) yet still be a probabilistic estimate (moderate confidence), or a sound calculation (code-verified) that rests on an assumption (note it).

## Axis 1 — Provenance tier
- **Primary-verified (P)** — authoritative primary source, quoted.
- **Code-verified (C)** — verified against our own code at `file:line`, or by running it.
- **Host-verified (H)** — confirmed by running a read-only check on a real machine.
- **Synthesis (S)** — true, but stitched from 2+ sources; no single source says it as one sentence. *Flag the stitch.*
- **Secondary (2)** — community/secondary source or a research agent; not confirmed against a primary.
- **Inference (I)** — derived/assumed, NOT stated by any source. **The dangerous tier** — inference dressed as fact is the #1 overclaim. Never let an `I` wear a `P`'s clothes.

## Axis 2 — Confidence: Words of Estimative Probability
Use the house WEP vocabulary (must match `/analysis`):

| Phrase | Probability | When |
|---|---|---|
| **Almost certainly / Nearly certain** | 95-99% | Multiple corroborating high-quality sources |
| **Very likely / Highly probable** | 80-95% | Strong evidence, minor gaps |
| **Likely / Probable** | 55-80% | Preponderance of evidence |
| **Roughly even chance** | 45-55% | Balanced / ambiguous |
| **Unlikely / Improbable** | 20-45% | Leans against, can't rule out |
| **Very unlikely / Highly improbable** | 5-20% | Little support |
| **Almost certainly not / Remote** | 1-5% | Would require extraordinary circumstances |

**Rules (from `/analysis`):**
- Never use "possible" alone — everything is possible; specify likelihood.
- Never say "may"/"might" without a WEP qualifier.
- **"Insufficient information to judge" ≠ low probability.** If we lack the data to estimate, say *that* — do not collapse it to "unlikely." (Kent's distinction.)
- For any claim below **Likely**, write an **alternatives note**: what else could be true, and what evidence would move the estimate.

Also assign an overall **Analytic Confidence** to the assessment: **High / Moderate / Low**.

---

# Phase 4 — PROPOSE REWRITES (only when a change is warranted)

**Default posture: the audit IS the deliverable.** If validation finds nothing that needs changing, do NOT create a rewritten file — the audit doc (provenance + WEP + coverage metadata) is itself the confirmation that the target stands as-is. Never clobber or duplicate a clean original.

**When a change IS warranted** (overclaims, false numbers, unsupported assertions, command/prose mismatches), produce a corrected version:
- For every claim graded **Synthesis, Secondary, Inference**, or below **Likely** that the target asserts too strongly, hedge to the **validated WEP tier** — never stronger than the evidence supports, never weaker than warranted.
- Preserve the author's voice and length; change truth-strength, not style.
- Leave fully-verified claims (P/C/H, Almost-certain) alone — over-hedging verified facts is its own distortion.

**Delivery — NEVER clobber the original:**
- **Target is a file:** write the corrected version as a NEW file that continues the revision chain, with a `claude-` marker showing Claude authored it: `<original-basename>__claude-<N+1>.<ext>`, where `N` is the highest existing revision index in that file's chain (e.g. latest `..._01__edits3.md` → `..._01__claude-4.md`; if no prior revisions exist, `..._01__claude-1.md`). This keeps every revision diffable and never overwrites the original. Overwrite ONLY when the user explicitly says to clobber.
- **Target is pasted text (no file):** show **before → after** per changed sentence inline so the human can accept/reject each.

(This is the "fixing how true something is" work, automated. Run report-only to suppress rewrites entirely — the audit metadata then stands as the sole confirmation.)

---

# OUTPUT — the claim-audit document

Write a markdown audit (model it on the canonical example below):

- **Claim table:** `# | claim | tier (T1-4) | provenance | method+evidence | WEP | rewrite (if any)`
- **Coverage Ledger** (Phase 1) — including NOT-YET-COVERED.
- **Rejected/avoided claims** — tempting assertions we did NOT make and why (the inference-catch section).
- **Net assessment:** one paragraph — is anything false? what's the weakest link? overall Analytic Confidence.
- For external mode: the **before→after rewrites**.

---

# Canonical worked example (study this)

A real audit of an IPv6 networking issue reply (identifiers anonymized here) demonstrated every phase, and three real catch-types:
1. **Numeric (T1):** "every ~15 seconds" was un-sourced → verified verbatim against the primary Microsoft NCSI FAQ (`PassivePollPeriod`). Provenance upgraded to **P**.
2. **Command (T2) + host-verify:** running `Get-ItemProperty` on the live registry **upgraded** five `*V6` value claims from **Secondary → Host-verified**, and confirmed the ULA address in question (`fdxx:xxxx:xxxx::1`). Running `netsh ... show address` revealed its "Addr Type" column says `Other`, not "Unique Local"/"Link-Local" — a prose/command mismatch caught only by execution.
3. **Inference (I) caught:** a web-summary asserted a well-known forum expert "is a Microsoft employee," inferring it from his Q&A *reputation points* — an invalid inference. Graded **I**, rejected; we used the defensible "Windows internals expert" instead. **This is the prototypical overclaim the skill exists to stop.**

---

# Acceptance self-checks (the skill is working if…)
- **AC1** Every T1 numeric + T2 code/command claim appears in the ledger (none missed).
- **AC2** Output always contains a Coverage Ledger with a NOT-YET-COVERED list.
- **AC3** A wrong number is flagged with the correcting source.
- **AC4** An inference-dressed-as-fact is graded **I**, not P.
- **AC5** A command whose output doesn't match its prose is caught by running it.
- **AC6** No host state mutated without backup+reversal+flag; destructive-to-verify claims are refused, not auto-run.
- **AC7** Every graded claim carries a WEP phrase + provenance tier; sub-"Likely" claims carry an alternatives note.
- **AC8** Each flagged overclaim gets a rewrite hedged to its validated WEP tier (external mode).

## Design lineage
`2026-06-17__14-57-45__dev-workflow-process_check-the-numbers-skill.md` (project-private DWP, maintainers only); WEP vocabulary from the `/analysis` command (not yet in this public set).
