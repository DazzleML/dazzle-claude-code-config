---
name: merge-3-way-split
description: "Read-only pre-merge review. Lists dual-touched files, shows OURS / THEIRS / merge-base diffs, and flags likely-collision patterns so the integrator understands the full scope before running git merge. Accepts a target branch (default: main)."
allowed-tools: Bash, Read, Grep, Glob
---

# merge-3-way-split — pre-merge 3-way diff review

## Target: "$ARGUMENTS"

Read-only analysis of an upcoming merge. Inform the integrator about
what's coming in -- per-file, side by side -- BEFORE `git merge` runs.

Use when: you're about to merge a non-trivial branch (parallel work,
multiple authors, multiple days/weeks of changes) and want to
understand the full scope of incoming changes before letting git's
default 3-way merge mutate files.

If no target is given, default to `main`.

## Steps

### 1. Identify branches and base

- Current branch: `git rev-parse --abbrev-ref HEAD`
- Target branch (from $ARGUMENTS or default `main`)
- Merge base: `git merge-base HEAD <target>`
- Quick stats: how many commits each side has since the base
  (`git rev-list --count <base>..HEAD` and `<base>..<target>`)
- Summary line: "Merging N commits from <target> into M commits on
  <branch> diverged at <base-short-sha>."

### 2. Classify file sets

Compute three sets relative to the merge base:

- **only-ours**: files modified on HEAD but untouched on target
  (`git diff --name-only <base>..HEAD` MINUS
  `git diff --name-only <base>..<target>`)
- **only-theirs**: files modified on target but untouched on HEAD
  (the complement)
- **dual-touched**: files modified on both sides
  (intersection of the two diff lists)

Report counts. Highlight that only-ours / only-theirs will auto-merge
trivially -- dual-touched is where attention is needed.

### 3. Per-file 3-way view (dual-touched only)

For each file in the dual-touched set, emit a compact block:

```
=== <file> ===
[size: OURS +X / -Y lines, THEIRS +A / -B lines]

OURS  (HEAD vs base):
<git diff <base>..HEAD -- <file> output>

THEIRS  (target vs base):
<git diff <base>..<target> -- <file> output>
```

Truncate per-file diffs to ~80 lines each if they're huge; mention
how to see the full diff (`git diff <base>..HEAD -- <file>` etc).

Order files by "interesting-ness": smallest first if the file is
config / version (likely trivial), largest last (likely complex).

### 4. Flag likely-collision patterns

After the per-file diffs, surface a "Watch list" of patterns that
auto-merge handles wrong even when hunks don't overlap:

- **Function signature changes** on one side + still-extant calls on
  the other (grep both diffs for `def <name>` adds/removes, then
  grep the other side for `<name>(`)
- **Removed imports** on one side, still-referenced on the other
- **Renamed identifiers** on one side, original-name uses on the
  other
- **New control-flow branch** (if/elif/return early) on one side +
  the other side's logic below the new branch
- **Helper added on both sides with similar purpose** (potential
  duplication)

Be concrete: name the file, line area, and what the integrator
should look at. False positives are fine -- a quick re-check is
cheap, missing a real collision is expensive.

### 5. Recommend next steps

Print a short "What to do now":

- If dual-touched is empty: "Safe to `git merge <target>` -- only
  trivial auto-merges expected."
- If dual-touched has a few clean cases: "Run `git merge <target>`;
  expect conflict markers in <file1>, <file2>. Use git's normal
  resolution flow."
- If the watch list flagged anything: "Read the flagged sections
  before merging; auto-merge may produce code that parses but is
  semantically wrong. Consider drafting the resolution in your head
  per-file before running `git merge`."

### 6. Stop

This skill does NOT run `git merge`. It only informs. The integrator
runs `git merge <target>` separately, then resolves conflicts using
git's standard tooling (with full context from this review).

## Output style

- Compact. Per-file blocks should be a quick scan, not a wall of text.
- Use the `=== filename ===` separator so it's grep-able.
- For very large dual-touched sets (10+ files), summarize after the
  first 5 and offer to dump the rest on request.
- Read-only. Do not modify files, do not call `git merge`, do not
  stage anything.

## Why this exists

Git's default 3-way merge silently accepts non-overlapping hunks from
both sides. That can hide semantic conflicts -- a function rename
plus a still-extant call site, a new control-flow branch the other
side's logic bypasses, a helper added on both sides with similar
purpose. Catching these requires reading both sides' intent BEFORE
auto-merge runs, not after.

The previous attempt at this (a `.gitattributes` + `merge.<name>.driver
"false"` config that forced every dual-touched file to surface as a
conflict) was painful in practice -- when the driver fires, git leaves
HEAD's version verbatim with no 3-way view, so the integrator has to
re-derive what git would have given for free.

This skill is the read-only, information-first alternative. Run it,
read the output, then let git do the merge.
