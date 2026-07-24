# Move Code — Copy-Don't-Rewrite Code Migration

A discipline for relocating code (function, class, module, region) from one file to another **without losing lines, comments, edge cases, or subtle invariants**. The core rule: never have the LLM rewrite from memory. Use the OS to copy the source verbatim, paste it in place, trim, then modify.

## Context

LLMs paraphrase. When asked to "move this function from A to B," an LLM may subtly:
- Reword a docstring
- Rename a variable
- Drop a comment that looked ornamental but encoded a real invariant
- Lose a specific error message
- Skip an edge-case branch
- Forget a defensive check

The result LOOKS right and PASSES type checks. It silently changes behavior. This is the same failure mode that makes "explain this code and write it in your own words" produce subtly wrong explanations.

The fix is procedural, not LLM-skill-based: **start from the verbatim source as a known-good baseline**. Diffs against that baseline are obviously-correct or obviously-wrong; rewriting from memory makes wrongness invisible.

## When to Use

Apply this skill any time you are MOVING code — not authoring new code:

- **Library extraction** (e.g., dazzlecmd `_cmd_list` → dazzlecmd-lib `render_list`)
- **Module split** (one file becomes two)
- **Function extraction** (large function → smaller helpers)
- **Refactoring a region** (cut from one file, paste into another)
- **Promoting private helpers to public APIs** (rename `_foo` → `foo`, move to public module)
- **Consolidating duplicated logic** (two near-identical functions → one shared)
- **Lifting code from a fork or vendor** into your codebase (or vice versa)

DO NOT use for:
- Authoring new code (no source to copy from)
- Trivial moves (single-line, single-comment)
- Pure renames (Edit tool with `replace_all: true`)
- Deletions (Edit tool removing a region; no destination)

## When NOT to use

- **Emergency fixes**: if something is broken in production, get it working first; refactor with this discipline second.
- **Authoring new code that resembles existing code**: copying-with-attribution is great for moves; for new code, do the design work fresh.

## The 4-Step Procedure

### Step 1 — OS-level capture (verbatim)

Use the OS to copy the EXACT source text. Choose one:

**Best**: use Claude Code's `Read` tool with a precise `offset` + `limit` to capture the source range. The tool reads disk byte-for-byte; the LLM can paste from its tool output without reconstructing.

**Acceptable**: shell command to extract the range:

| Shell | Command |
|---|---|
| **POSIX (bash/zsh)** | `sed -n '${start},${end}p' source_file > captured.txt` |
| **PowerShell** | `Get-Content source_file \| Select-Object -Skip $(($start-1)) -First $(($end - $start + 1)) > captured.txt` |
| **cmd.exe** | (use PowerShell — cmd has no native row-range tool) |

**Wrong**: telling the LLM "read the file and then write it back to the new location." That invites paraphrase.

### Step 2 — Paste in place (as-is, no edits yet)

Write the captured text to the destination file. Preserve EXACTLY:

- All comments (including ornamental-looking ones)
- All whitespace (indentation matters; tabs/spaces consistency matters)
- All variable names (don't rename until Step 4)
- All docstrings (even if the new home would phrase them differently)
- All error messages
- All defensive checks (`if x is None: ...`)
- All edge-case branches

If you need to insert the captured text into the middle of an existing file (e.g., adding a function alongside others), use `Edit` with the surrounding lines as `old_string` to position the insert precisely.

### Step 3 — Trim (mechanical removal only)

Delete only the lines that don't belong in the destination:

- The function definition shell if you're migrating just the body
- Callsite-specific bits (e.g., the calling-side `args.foo` references when the helper is being moved)
- Docstring fragments that reference the OLD location ("called from cli.py:..." → delete; the new location speaks for itself)
- `import` statements that only the old caller needed

Trim is **mechanical removal**, NOT rewriting. If you find yourself wanting to rephrase rather than delete, stop — that's Step 4 work.

### Step 4 — Modify (small reviewable diffs)

Now — and ONLY now — make the modifications needed to fit the new design:

- Signature changes (e.g., `def render_list(args, projects)` → `def render_list(args, projects, engine=None)`)
- Import path updates (`from .cli import _foo` → `from .module import _foo`)
- Renames as part of public-API promotion (`_build_list_entries` → `build_list_entries`)
- Adapter shims for callers (the OLD location now has a thin wrapper that calls the new location)

Each modification should be a small, reviewable diff against the verbatim baseline. If a modification is large or hard to explain, split it into smaller modifications.

## Pre-Move Checklist (run BEFORE Step 1)

Inventory every reference to the symbol(s) being moved. Use multiple Grep calls in parallel for breadth:

```
Grep pattern: "<symbol_name>" — find all callsites, definitions, tests, imports
Grep pattern: "from <module> import .*<symbol_name>" — explicit imports
Grep pattern: "<symbol_name>\\(" — function calls specifically
Grep pattern: "from <old_path>" — anyone importing from the old location
Grep across: project source/, tests/, docs/, private/claude/, projects/<adopters>/
```

Classify each match:
- **Stays put** (callsite OK as-is — won't break)
- **Needs update** (import path will change; rename if applicable)
- **Delete after move** (the OLD location's definition; duplicate references)

## Post-Move Checklist (run AFTER Step 4)

Verify nothing was lost:

1. **Run the full test suite** — should be the same green count as before
2. **Capture golden output** for any user-facing surface affected:
   - Before: `<command> > /tmp/before.txt`
   - After: `<command> > /tmp/after.txt`
   - `diff /tmp/before.txt /tmp/after.txt` — **should be byte-equivalent if behavior is meant to be unchanged**
3. **Live-verify with downstream consumers** — invoke the consumer (e.g., `wtf list`) to confirm the move didn't break anyone
4. **Re-grep the same patterns** — every match should now point at the NEW location, or be a comment/historical reference
5. **Audit duplicate tests** — when the new location has tests, the old location's tests for the same logic become redundant. Delete or convert to integration tests.

## Cross-Shell Notes

For Windows-target projects (and dazzlecmd-family projects all are):

- **Don't use `cat` or `head`/`tail` in cmd.exe** — use `type` (cmd) or `Get-Content` (PowerShell)
- **Don't use `>nul` in WSL/bash** — use `>/dev/null` (WSL/bash) or `>NUL` (pure cmd.exe)
- **Path quoting**: Windows paths with spaces need double quotes; forward-slashes work in PowerShell

## Failure Modes (and what they mean)

| Symptom | Likely cause | Fix |
|---|---|---|
| Tests pass, golden output differs | Step 4 modification subtly changed behavior | Diff against verbatim baseline; isolate the change |
| Tests fail with `ImportError` | Step 4 didn't update consumer imports | Re-grep for `from <old_path>` and update |
| Tests fail with subtle assertion errors | Step 2 paraphrased a comment that encoded an invariant | Re-capture verbatim and redo |
| Linter complains about unused imports | Step 3 left old-location imports behind | Run `flake8` or equivalent; clean up |
| Downstream consumer breaks | Step 4 broke a public API | Add a back-compat shim at the OLD location |

## Companion Discipline: Thorough Cleanup

This skill is a sibling of the **thorough-cleanup principle** (`feedback_thorough-cleanup-on-migrations.md` in dazzlecmd's project memory). Move-code handles the SOURCE side (what's moving); thorough-cleanup handles the AFTERMATH (greps, tests, audits, no leftovers).

For any commit that involves substantial code movement, BOTH disciplines apply:
- **move-code**: how to move the code itself without paraphrase
- **thorough-cleanup**: how to verify nothing was left behind

## Provenance

This skill was created during the dazzlecmd 0.7.x → 0.7.31 transition (commit `781b3e8`, "v0.7.30 fix(lib,cli): closes #56"). The trigger was the discovery during sign-off that shadow-status logic had been ported to dazzlecmd's CLI but not the library — caught only because a downstream consumer's info command showed no shadow block. The fix took an emergency mid-sign-off port. User stated:

> Note that we should ALWAYS copy the code directly from the file and then rewrite that. We should NOT try to rewrite it. In other words "copy the file" chop it down, then use that output as the basis so comments and all code is identical on initial copy. Then after the file has been copied in place to its final location and trimmed to the code we want to relocate then we can consider modifications to make it work with the new design. This guarantees that we do not lose lines of code in the process.

## When invoking this skill

You can:
- Reference it implicitly when about to make a substantial code move ("I'll apply move-code discipline")
- Call it explicitly via `/move-code` if a slash command wrapper exists
- Or just follow the 4-step procedure manually

The procedure matters more than the invocation.
