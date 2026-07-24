# GitHub Issue Creator

Create a well-structured GitHub issue following a consistent format. Adapts to bugs, features, and architecture issues.

## Usage

```
/github-issue <description of the issue to create>
```

If no arguments, prompt the user for a description.

## Instructions

### 1. Gather Context

Before writing, collect:
- **Current repo**: Run `gh repo view --json nameWithOwner -q .nameWithOwner` to identify the repo
- **Existing labels**: Run `gh label list` — only use labels that exist (create missing ones first with `gh label create`)
- **Open issues**: Run `gh issue list --state open --limit 20` — check for duplicates and cross-references
- **Related code**: If the issue references code behavior, read the relevant files to verify claims
- **Related docs**: Check `./private/claude/` (or project's analysis folder) for existing design docs or postmortems to reference

### 2. Choose Labels

Select appropriate labels based on issue type:
- **Bug**: `bug` (+ `enhancement` if proposing a fix beyond just correcting the bug)
- **Feature**: `enhancement` (+ `ideas` if exploratory, `epic` if large/multi-phase)
- **Architecture**: `architecture` (+ `enhancement` or `epic` as appropriate)
- Only use labels confirmed to exist on the repo (from step 1)

### 3. Write the Issue Body

Follow this structure. **Required sections** must always be present. **Conditional sections** are included when relevant.

```markdown
## [Descriptive title with subtitle context]

### Problem

[REQUIRED — What doesn't work, what's missing, or what friction exists]

- Clear statement of the issue
- Why it matters (user impact, developer experience, correctness)
- Motivating example: real output, error message, or workflow showing the current state
- What users currently have to do as a workaround (if applicable)

Include actual code snippets or CLI output demonstrating the problem when possible.

### Proposed solution

[REQUIRED — The ideal behavior or feature design]

- High-level approach (1-2 sentences)
- Code examples or command syntax showing ideal UX
- Multiple design options if choices exist (labeled Option A, B, C with trade-offs)
- How this solves the problem stated above

### [Domain-specific detail section]

[CONDITIONAL — Include when the feature requires detailed specification]

Use a descriptive heading like "Disambiguation rules", "API contract", "Migration strategy", etc.

- Tables for rules, behavior matrices, or inventories
- Code snippets showing data structures or algorithms
- Edge case enumeration

### Implementation approach

[CONDITIONAL — Include when architectural or code-level explanation is needed]

- Classes/modules affected
- Method signature changes
- Phased implementation if large (Phase 1, Phase 2, etc.)
- Code snippets showing the approach (pseudocode is fine)

### Design considerations

[CONDITIONAL — Include for features with non-obvious trade-offs]

- Bullet points covering design decisions and rationale
- Interaction with other features
- Performance implications
- Security implications
- What was considered but rejected (and why)

### Acceptance criteria

[REQUIRED — Checkbox list of concrete, testable conditions]

- [ ] Each item is independently verifiable
- [ ] Cover: code changes, tests, documentation, behavioral guarantees
- [ ] One checkbox per distinct requirement (don't combine multiple things)

### Related issues

[CONDITIONAL — Include when cross-references exist]

Format: `- Refs #N — brief context of the relationship`
Verbs: "Refs" (related), "Depends on" (blocker), "Closes" (only if this issue fully resolves it)

### Analysis

[CONDITIONAL — Include when a local design doc or postmortem exists]

Format:
```
See `filename.md` for detailed analysis.
```

Rules for referencing local documents:
- Include ONLY the filename or sub-path (e.g., `notes/cli/2026-02-14__example.md`)
- NEVER include `private/claude/` as a prefix
- Sub-paths within `private/claude/` are fine (e.g., `notes/ideas/`, `notes/cli/`)
- If the doc has a descriptive slug, that's sufficient context
```

### 4. Save Issue Body to File

Write the issue body to the project's `private/claude/issues/` folder:
- Filename: `issue_N_YYYY.MM.DD_NN.md` (N = issue number if known, else descriptive slug)
- Create the `issues/` directory if it doesn't exist

### 5. Create the Issue

```bash
gh issue create \
  --title "Descriptive title" \
  --label "label1" --label "label2" \
  --body-file private/claude/issues/issue_N_YYYY.MM.DD_NN.md
```

Always use `--body-file` to avoid shell escaping issues with complex markdown.

### 6. Companion Planning Document

Determine whether a local design doc already exists for this work:

- **Design doc came first** (common): A dev-workflow-process, Obsidian note, or postmortem already exists in `private/claude/` and was referenced in the issue's "Analysis" section. No additional doc needed — the serialized thinking already exists.

- **Issue came first** (this step): No prior design doc exists. Create a companion planning document that serializes the thinking behind the issue into the chronological `private/claude/` timeline.

#### When to create the companion doc

Create it when ALL of these are true:
1. No pre-existing design doc, postmortem, or Obsidian note covers this work
2. The issue is non-trivial (more than a simple bug fix or one-file change)
3. Implementation will require thinking through steps, trade-offs, or sequencing

#### Companion doc format

**Filename**: `YYYY-MM-DD__hh-mm-ss__<topic-slug>__GHIssue#<N>.md`

Example: `2026-02-14__11-30-00__namespace-collision-favorites__GHIssue#9.md`

**Structure** — this is NOT a copy of the issue. It's a thinking document:

```markdown
---
type: planning
date: YYYY-MM-DD
author: both
github_issue: N
tags:
  - by/both
  - planning
  - issue/N
---

# <Topic> — Implementation Planning (GH Issue #N)

## Context

Brief recap: what is the issue about, why does it matter, and what's the current state
of the codebase relevant to this work. Link to the issue file in `issues/`.

## Scope & Boundaries

What's IN scope for this issue vs what's deferred to other issues.
What files/modules are affected. What's NOT changing.

## Implementation Steps

Ordered, detailed steps to actually do the work. This is where the
dev-workflow-process thinking happens — not the high-level phases from
the ticket, but the actual sequence of edits, tests, and validations:

1. Step one — what file, what change, what to watch out for
2. Step two — dependencies on step one, expected behavior after
3. ...

## Considerations

Pros, cons, edge cases, risks, adjacent system impacts — the "puzzle"
portion of SPCR. Things that the GitHub issue's acceptance criteria
don't capture but that matter during implementation.

## Open Questions

Anything unresolved that needs user input or further investigation
before implementation can proceed.

## Related

- GitHub Issue: #N
- Issue file: `issues/issue_N_YYYY.MM.DD_NN.md`
- Other related docs (Obsidian notes, prior postmortems, etc.)
```

The key difference from the GitHub issue:
- **Issue** = what and why (public-facing, for anyone reading the repo)
- **Companion doc** = how, in what order, and what to watch out for (local, for the implementer)

### 7. Post-Creation

- Report the issue URL to the user
- If a companion doc was created, mention its filename
- If the project has an Obsidian vault or MOC, update it with the new issue number
- If this issue should be a sub-issue of another, offer to link them

## Section Usage Guide

| Section | Bug | Feature | Architecture | Required? |
|---------|-----|---------|-------------|-----------|
| **Problem** | Error/symptom | Limitation/friction | Design gap | Always |
| **Proposed solution** | Expected behavior | Ideal UX | New structure | Always |
| **Detail section** | Repro conditions | Spec/rules table | Design choices | As needed |
| **Implementation approach** | Fix location | Code changes | Architecture diagram | As needed |
| **Design considerations** | Root cause analysis | Trade-offs | Patterns/principles | As needed |
| **Acceptance criteria** | Regression tests | Feature checklist | Structural verification | Always |
| **Related issues** | Duplicate/blocker | Feature family | Dependencies | As needed |
| **Analysis** | Postmortem ref | Design doc ref | Study ref | As needed |

## Quality Checklist

Before creating the issue, verify:
- [ ] Problem section has a concrete example (code output, CLI interaction, or error message)
- [ ] Proposed solution shows what the UX looks like, not just what the code does
- [ ] Acceptance criteria are testable — each one answers "how do I verify this is done?"
- [ ] All referenced labels exist on the repo
- [ ] Related issues are real issue numbers (checked against open issues)
- [ ] Analysis doc references use filename only (no `private/claude/` prefix)
- [ ] Code snippets are accurate (verified by reading the actual source when claiming behavior)

## Notes

- The "Detail section" heading should be descriptive, not literally "Detail section" — use names like "Disambiguation rules", "Channel inventory", "Migration plan", etc.
- When multiple design options exist, present them objectively with trade-offs rather than only showing the recommended option
- For epics or large features, use phased implementation in the "Implementation approach" section
- Keep the Problem section focused on the user's experience, not internal code structure — save code details for Implementation
- Acceptance criteria should cover code, tests, AND documentation — not just code
