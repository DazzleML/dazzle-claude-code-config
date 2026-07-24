---
name: test-checklist
description: Produce a hand-runnable human test checklist alongside automated tests. Run after writing automated test suites for a phase/feature that ships user-visible behavior. Creates a markdown doc (public by default in tests/checklists/, or in a project-private location for sensitive content) that a human walks through to verify end-to-end behavior that mocks can't cover -- shell rendering, Windows codepages, real subprocess behavior, interactive prompts, file atomicity under real conditions, config isolation, and other "the mocks say it works but does it REALLY" scenarios.
---

# Test Checklist Skill

Produce a **human-runnable test checklist** alongside significant automated test work. This document complements automated tests — it captures what the mocks can't, and it serves as a durable record of "what should we test" for each phase/feature.

## When to use

Trigger this skill broadly — **err on the side of producing a checklist**. Automated tests catch regressions in mocked paths; human checklists catch the subtle behavior drift that mocks miss. The cost of producing one is low; the cost of shipping a "pure refactor" that silently breaks metadata preservation or subprocess handling is high.

Produce a checklist when you finish writing automated tests for:

- A new Phase, epic, or major feature
- A new CLI command or user-visible surface area
- A refactor that touches dispatch, configuration, file I/O, subprocess execution, metadata handling, or discovery — **even if the refactor claims no user-visible change**
- Any commit with a substantive CHANGELOG entry (Added, Changed, or Fixed for a real bug with user impact)
- Anything where a subtle regression could affect users in non-obvious ways

If the user explicitly says "let's write tests" or "add tests for this," ask at the end: **"Do you also want a human test checklist for the phase/feature we just tested?"** Default to yes unless the work is clearly trivial.

## When NOT to use

Skip the checklist ONLY for genuinely trivial work:

- Single-line bug fixes with truly no interaction surface
- Doc-only commits (no code change)
- Test-only commits that add tests for existing behavior (no new features, no refactor)
- Dependency version bumps that don't expose new behavior
- Version metadata commits / CHANGELOG-only edits
- Comment-only or whitespace-only changes

**Critical**: refactors do NOT belong on this skip list. Even "pure internal" refactors (e.g., migrating to a library primitive) can introduce subtle behavior changes in I/O paths, metadata preservation, error message phrasing, or performance characteristics. If a refactor touches any code path with side effects, write a checklist.

**Example filter** from a real project (dazzlecmd):

| Commit | Checklist? | Reason |
|---|---|---|
| v0.7.7 safedel phase 3a (per-volume trash) | yes | new user-visible behavior |
| v0.7.8 safedel phase 3b+3c (ctime, xattrs) | yes | new preservation primitives |
| v0.7.9 Phase 2 (recursive FQCN dispatch) | yes | new dispatch semantics |
| v0.7.10 safedel Phase 8 (filekit migration) | yes | refactor touching metadata preservation — subtle regressions possible |
| v0.7.10 docs (safedel TODO/ROADMAP) | no | doc-only |
| v0.7.11 Phase 3 (kit management + config write) | yes | large new CLI surface |

**Rule of thumb**: if you're unsure whether a commit needs a checklist, write one. Five minutes of checklist work is cheap insurance against a user-reported regression three months later that nobody can reproduce.

## Why human checklists matter alongside automation

Automated tests cover what a mock can verify: function inputs and outputs, mocked subprocess calls, in-memory data structure correctness, regression prevention. But they systematically miss:

- **UI and UX issues**: readability, spacing, column alignment, table vs list choices, the difference between "works" and "feels good to use." A table with cramped columns passes every assertion but users hate it.
- **Design problems that only surface in real use**: a command might be functionally correct but the wrong shape for the task — wrong verb, wrong argument order, wrong default, wrong level of nesting. Mocks happily verify whatever you wrote; humans notice when what you wrote solves the wrong problem.
- **Shell/terminal rendering**: ASCII characters on Windows codepage 437/1252, line wrapping, color codes, trailing whitespace, terminal width assumptions
- **Real subprocess behavior**: git submodule add against a real URL, file locking, process exit codes in the wild
- **Interactive prompts**: stdin handling, TTY detection, Ctrl-C behavior, y/N prompt rendering
- **File atomicity under real conditions**: disk full, permission denied, write crashes mid-way, antivirus interference
- **Config isolation**: tests use temp dirs; real users share the process with their actual dotfiles
- **Cross-platform portability**: most tests run on one OS; checklists get executed on all of them
- **Performance feel**: "does the discovery feel snappy?" — not a number, but users notice
- **Error message quality**: is the wording actually helpful, or does it just not crash?
- **Discoverability**: can a new user find `dz kit --help` and figure out what to do?

These are the things that make software feel finished versus feel broken. Automated tests guard against regressions; human checklists guard against "technically correct but unusable, unreadable, or solving the wrong problem."

## Output location — PUBLIC vs PRIVATE

Checklists live in two parallel directories:

### `./tests/checklists/` (PUBLIC — default)

Ships with the repo in public git history. External testers, contributors, and users can read it. Use this location when the checklist contains:

- Standard feature verification
- Expected CLI output with dummy/example data
- Configuration examples users would also see in the docs
- Anything matching CHANGELOG entries
- General regression testing

**Default to this location** unless the checklist genuinely contains sensitive content.

### `./private/claude/checklists/` (PRIVATE — sensitive content only)

Local-only, never pushed publicly. Use this location when the checklist contains:

- Credentials or API keys (even placeholders that reveal internal format)
- Internal staging URLs, hostnames, customer identifiers
- Work-in-progress drafts not ready for public consumption
- Customer-specific scenarios
- Internal testing infrastructure details
- Anything a contributor reading the public repo shouldn't see

**Escape hatch only** — don't reflexively put things here to be "safe." Public checklists are more useful to the project long-term.

### Dual-variant case

If a feature needs both public and private verification steps, produce two checklists:

- `tests/checklists/v0.7.15__Feature__oauth-flow.md` — public: verifies basic OAuth flow with example client
- `private/claude/checklists/v0.7.15__Feature__oauth-flow-internal.md` — private: verifies internal staging env with real client secrets

Cross-reference them in each other's "Related" sections.

## Filename format

```
vX.Y.Z__<Type>__<descriptive-slug>.md
```

Where:

- **`vX.Y.Z`** — version the checklist ships with (version-first for sortable browsing)
- **`<Type>`** — one of:
  - `Phase1`, `Phase2`, `Phase3`, ... for architectural epoch phase work
  - `Feature` for non-phase new features
  - `Tool` for new tool additions (e.g., `dz find`, `dz tree`)
  - `Refactor` for refactors with user-visible behavior changes (rare — most refactors skip the checklist)
  - `Epic` for large multi-commit work tracked by a GitHub epic issue
- **`<descriptive-slug>`** — hyphenated description of what was done

**Examples**:

```
v0.7.11__Phase3__kit-management-and-config-write.md
v0.7.5__Tool__dz-find-cross-platform-search.md
v0.7.3__Feature__fixpath-search-fallback.md
v0.8.0__Epic__dazzlecmd-lib-extraction.md
```

Version-first naming means `ls tests/checklists/` shows a linear project history. Type marker groups similar work. Slug provides discoverability.

## Document structure

Use this template. Adapt sections to the specific phase/feature.

```markdown
# Human Test Checklist: <Phase/Feature Name>

**Target version:** <version this work ships in>
**Ships with commit:** <commit subject, or TBD if pre-commit>
**Companion automated tests:** <counts by file, e.g., "75 tests in tests/test_engine_config.py (28), tests/test_cli_kit.py (23), tests/test_cli_tree.py (11)">

## What this is

One paragraph: why this document exists, who runs it, what it covers.

## Planning lineage

**Public (in this repo)**:
- `docs/guides/<relevant-doc>.md` — user-facing reference
- `CHANGELOG.md` [<version>] — summary of what shipped
- GitHub issues #N, #M (public)

**Project-private** (not in public git history, for project maintainers):
- `<timestamp>__dev-workflow-process_<topic>.md` — design analysis
- `<timestamp>__<decisions-or-Q-and-A>.md` — decision resolution
- `<timestamp>__DISCUSS_Rnd<N>_<topic>.md` — architectural discussion rounds

External testers can use this checklist without reading any of the above.
Project maintainers can follow the lineage to understand the "why."

## Prerequisites

1. Environment requirements (OS, installed version, access to specific repos/files)
2. Setup steps (env vars for test isolation, backups to make)
3. How to reset state between sections

Always use test-isolation env vars or a throwaway config path. Never
write to the user's real dotfiles during a checklist run.

---

## High-Value Verification (~5 minutes)

**If you only have 5 minutes**, run these N tests. They cover the highest-impact
user-visible behavior this commit introduces. If any of them fail, the work is
broken and the detailed sections below probably can't save you.

Each test here is also covered in detail later in this document, but these are
the "did the work actually ship" smoke tests. 4-6 tests is the sweet spot — any
fewer misses coverage, any more becomes another detailed section.

### HV.1 — <Name of the most important thing>

Validates: <the specific behavior / code path / user value>.

- [ ] **Steps:**
  1. Exact command or action
  2. Next command
- [ ] **Expected:** Observable outcome
- [ ] **Why this matters:** One sentence on what breaks if this fails. This
  sentence is the "elevator pitch" for the test — if you can't write it
  clearly, the test probably doesn't belong in HV and should move to a
  detailed section.

### HV.2 — <Next most important thing>

(continue...)

### HV.3, HV.4, HV.5, HV.6 — <...>

(continue — typically 4-6 total)

---

After these pass, you have high confidence the work shipped correctly. The
detailed sections below cover edge cases, error handling, idempotency,
env var overrides, interactive prompts, and integrations.

---

## Section 1: <Topical group>

### 1.1 <Specific test name>

- [ ] **Steps:**
  1. Exact command to run
  2. Exact next command
- [ ] **Expected:**
  - Observable output, exit code, side effect
  - What should NOT happen
- [ ] **Check:**
  - File contents to verify
  - Disk state changes
  - Config file state

### 1.2 <Next test>

(continue...)

## Section 2: <Next topical group>

(continue...)

## What the automated tests DO cover

Quantitative table of coverage so humans don't re-test what's verified:

| Area | Test file | Count |
|---|---|---|
| ... | ... | ... |

## What the automated tests DON'T cover

Explicit gaps that ONLY manual testing can verify:

- Shell rendering (Windows codepage, terminal width, color)
- Real subprocess/network/git behavior
- Interactive prompts
- File locking/concurrency
- Cross-platform portability
- Error message clarity and discoverability
- Performance feel

## Reporting issues found

1. Note the section and step number
2. Capture the exact command and output
3. Save relevant state files
4. File an issue referencing this checklist
5. Link back to the triggering commit/version

## Related documents

Cross-references to other docs in the project.
```

## Required content (non-negotiable)

Every checklist MUST include:

1. **Target version and commit** — anchors the checklist in project history
2. **Automated test count reference** — quantitative link to the automation
3. **Planning lineage section** — public and project-private document references, clearly labeled
4. **Prerequisites with state isolation** — how to run without corrupting the user's real config/data
5. **Step-by-step checkboxes** — each test independently runnable, not sequential-only
6. **High-Value Verification section** — 4-6 top-impact smoke tests for the 5-minute verification pass
7. **Explicit "what mocks don't cover" section** — the whole point of the document
8. **Reset instructions** — how to return to clean state after destructive tests
9. **Cleanup section** — at the very end, how to restore any backed-up state
10. **Cross-shell commands** — every command that touches env vars, file viewing, file deletion, redirection, or shell utilities MUST be given in **cmd.exe**, **PowerShell**, AND **POSIX (bash/zsh)** forms. See "Cross-shell command forms" below.

## Cross-shell command forms

**Rule**: if the project runs on Windows (and most dazzlecmd-family projects do), checklist commands that are shell-specific MUST appear in all three forms. Do not write POSIX-only commands in a Windows-target project.

**Common pitfalls** (all these BREAK on Windows cmd.exe):

| POSIX form (BROKEN on cmd.exe) | Reason it fails |
|---|---|
| `export DAZZLECMD_CONFIG=/tmp/x.json` | `export` is bash-only |
| `$DAZZLECMD_CONFIG` | cmd.exe uses `%VAR%`; PowerShell uses `$env:VAR` |
| `cat file.txt` | No `cat` on cmd.exe; use `type` |
| `rm -f file.txt` | No `rm` on cmd.exe; use `del` |
| `grep pattern file` | No `grep` on cmd.exe; use `findstr` |
| `wc -l` | No `wc` on cmd.exe; count lines via PowerShell/findstr |
| `command > /tmp/file` | `/tmp` doesn't exist on Windows; use `%TEMP%` |
| `command | grep x` | No grep; use `| findstr x` (cmd) or `| Select-String x` (PowerShell) |

**Cross-shell equivalents table**:

| Operation | cmd.exe | PowerShell | POSIX |
|---|---|---|---|
| Set env var | `set VAR=value` | `$env:VAR = "value"` | `export VAR=value` |
| Read env var | `%VAR%` | `$env:VAR` | `$VAR` |
| Print env var | `echo %VAR%` | `Write-Host $env:VAR` | `echo $VAR` |
| Unset env var | `set VAR=` | `Remove-Item Env:\VAR` | `unset VAR` |
| View file | `type file` | `Get-Content file` | `cat file` |
| Delete file | `del file` | `Remove-Item file` | `rm -f file` |
| Delete if exists | `if exist file del file` | `if (Test-Path file) { Remove-Item file }` | `rm -f file` |
| Temp directory | `%TEMP%` | `$env:TEMP` | `/tmp` |
| Filter output | `\| findstr pattern` | `\| Select-String pattern` | `\| grep pattern` |
| Count lines | — | `\| Measure-Object -Line` | `\| wc -l` |
| Pipe to Python | `command \| python script.py` | `command \| python script.py` | `command \| python script.py` |

**Cross-platform escape hatches** (work in all shells if the language is installed):

- `python -m json.tool file.json` — pretty-print JSON
- `python -c "..."` — one-liner scripting in any shell
- `dz kit reset --yes` — dazzlecmd commands are shell-agnostic by construction; prefer them over raw file operations

**Template pattern for command blocks**:

```markdown
- [ ] **Steps** (pick your shell):

  **cmd.exe**:
  ```cmd
  set DAZZLECMD_CONFIG=%TEMP%\test.json
  dz kit enable wtf
  type %DAZZLECMD_CONFIG%
  ```

  **PowerShell**:
  ```powershell
  $env:DAZZLECMD_CONFIG = "$env:TEMP\test.json"
  dz kit enable wtf
  Get-Content $env:DAZZLECMD_CONFIG
  ```

  **POSIX**:
  ```bash
  export DAZZLECMD_CONFIG=/tmp/test.json
  dz kit enable wtf
  cat "$DAZZLECMD_CONFIG"
  ```
```

When all three forms do the same thing via a dz command only (no file or env var handling), you can use a single unlabeled code block — but be explicit that it's cross-shell safe:

```markdown
- [ ] **Steps** (same across all shells, uses `dz` commands only):

  ```
  dz kit reset --yes
  dz list
  ```
```

## Optional but recommended

- Screenshots or ASCII captures of expected output for visual verification
- Cross-references to related design docs, issue numbers, and user-facing docs
- Section grouping by concern (config, commands, edge cases, integration)
- Explicit Windows-vs-POSIX flags on tests that differ by platform
- "Skip this section if..." notes for destructive or environment-specific tests
- Time estimates per section ("~5 min to run Section 2")

## Durability and review

The checklist is a **durable artifact** and serves three long-term purposes:

1. **Release gating**: before shipping any Phase/feature, a human walks through its checklist and flags failures
2. **Regression evidence**: if a user reports a bug six months later, the checklist shows whether this scenario was supposed to work
3. **Onboarding**: new contributors reading the project history can see what each phase actually delivered and what quality bar it was held to

## Planning lineage guidance

The "Planning lineage" section is **the key differentiator** between public checklists and private design docs. Public checklists reference both, but label them clearly:

- **Public docs** (in the repo): link with relative path, e.g., `docs/guides/config.md`. External testers can click through.
- **Project-private docs**: list by filename only (no directory path) under a **"Project-private (not in public git history, for project maintainers)"** header. External testers know they exist but can't access them; project maintainers know exactly which file to look for in their local working tree. **Never mention the `private/claude/` path (or any other private directory layout) in public-facing checklists** — the public file should not hint at where project-internal docs are stored.
- **GitHub issues**: link by number (`#9`, `#18`). Public and discoverable.
- **Commit SHAs**: include when referencing specific prior commits so the lineage is time-anchored.

This way a public checklist is useful to external testers (without frustrating references to inaccessible files) AND serves as a navigation hub for project maintainers — without leaking directory layout.

## Example first-session introduction

> "I've written 75 automated tests for Phase 3. Before we commit, let's also create a human test checklist — it captures what a person should run to verify Phase 3 end-to-end, including shell rendering, real subprocess behavior, interactive prompts, and Windows-specific edge cases that the mocks can't cover. I'll save it to `tests/checklists/v0.7.11__Phase3__kit-management-and-config-write.md` as a public artifact (no sensitive content). Sound good?"

Then produce the document using the template above.
