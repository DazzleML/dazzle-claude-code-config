# Claude Code Session Instructions

> **About this file**: a curated public variant of a working global CLAUDE.md — the "orchestrator" that tells Claude Code how your tools, conventions, and territories fit together. Sections marked **[FILL IN]** are invitations: replace the examples with *your* machines, layouts, and integrations. Everything else works as-is alongside the skills/commands/agents in this collection.

## Cognitive Frameworks Used

| Primitive | Purpose | Mnemonic |
|-----------|-----------------------------------------------------------|-------------------------|
| **SPCR** | Structures analysis, planning, and docs: | [S]tory → [P]uzzle → [C]ontent → [R]esult |
| **PUVM** | Surfaces rationale, intention, and value: | [P]hilosophy → [U]tility → [V]alue → [M]arketing |
| **Grouping/Ungrouping** | Helps with managing, clarifying, or resolving complexity: | Collapse ↔ Expand |

> These frameworks are integrated directly into the workflow and postmortem templates (see `/dev-workflow-process` and the postmortem commands), and can be used anywhere deeper reasoning or clarity is beneficial.

When applying PUVM analysis, **always include 1-2 paragraphs about the intention** behind the code, system, or decision being analyzed: what belief drives this code? What did the author assume to be true or important? How does this intention differ from similar systems? Two systems that look redundant often have complementary intentions — understanding intention prevents forcing one system to serve another's purpose.

## Writing Precision Rules

- Avoid the word "comprehensive" unless you truly mean all-encompassing in scope; the same for "critical" — reserve it for things required for correct operation. Overuse diminishes clarity and makes logs and docs sound inflated. Say what it does, not how big it sounds.
- **Better than generic intensifiers**: instead of "complete", "detailed", or "full", name what actually matters — "real-time failure detection" (not "comprehensive monitoring"), "bidirectional data sync" (not "full integration").
- **Do NOT hard-wrap Markdown prose for rendered/web targets** (GitHub issues, PRs, READMEs, CHANGELOGs): write one line per paragraph and let the renderer reflow. Only hard-wrap where the consumer is fixed-width: git commit message bodies (~72 cols) and plain-text terminal files.

## Search & Shell Tooling: Match the Tool to the Search

**Default to the built-in tools** — Grep (text), Glob (files), Read (whole files). Escalate to a specialized CLI only when the built-in genuinely cannot do the job:

| Search intent | Tool | When |
|---|---|---|
| **CODE STRUCTURE** — AST patterns, codemods | `ast-grep` (`sg`) | No built-in equivalent — the main reason this table exists |
| Extract from large **JSON** | `jq` | Surgical field extraction without reading the whole file into context |
| Extract from large **YAML / XML** | `yq` | Same token-efficiency win |
| **FILES** by type / mtime / exec | `fd` | When the query needs `--type`, `--changed-within`, `--exec` |
| **TEXT / strings** | Grep tool | Raw `rg` only for flags it doesn't expose |

## Claude Code Specific Gotchas

### Unicode / Codepage Issues in Generated Scripts
**AVOID Unicode characters** (em dashes, smart quotes, arrows, checkmarks) in `.ps1`, `.cmd`, `.bat` files or any code executing in a Windows `cmd` shell — cmd.exe defaults to codepage 437, PowerShell 5.1 to 1252; neither handles UTF-8 by default. Use `--` not em-dash, `->` not arrows, `[OK]`/`[X]` not checkmarks. If Unicode output is needed, emit it from Python.

### Null Device Redirection (WSL/Git Bash on Windows)
`>nul` in bash creates a literal file named `nul`. Always use `>/dev/null`. If a `nul` file gets created, plain `del`/`rm` cannot remove it -- use Python `os.remove()` with the `\\\\.\\` device-path prefix.

### Windows Junctions/Symlinks
Always use PowerShell (`New-Item -ItemType Junction ...`) — `cmd.exe /c mklink` invoked from bash fails silently. Junctions don't require elevation; symlinks do (unless Developer Mode).

## Storage Territory: `~/.claude/` vs `~/claude/`

**`~/.claude/` is Claude Code's managed directory** — upgrades or cleanup sweeps may delete files it doesn't recognize. **Never store user-created private data there.**

| Location | Owner | What goes here |
|----------|-------|---------------|
| `~/.claude/` | Claude Code | Skills, agents, commands, settings — may be cleaned by upgrades |
| `~/claude/` | **You** | Private notes, scripts, recovered files, task data — never touched by Claude Code |
| `./private/claude/` | You (per-project) | Design docs, postmortems, notes — lives with the project (see the dazzle-claude-code-config repo's docs/project-structure.md) |

## Critical Safety Rules

### 1. NEVER DELETE ANYTHING WITHOUT A RECOVERY METHOD
Before any deletion: explicit user confirmation, a verified backup or recovery path, understanding of the full impact. This rule is absolute.

### 1a. Prefer a Recoverable Delete Tool
When available, use a trash-staging deleter (e.g. `dz safedel` from dazzlecmd — link-aware, metadata-preserving, 30-day recovery) over `rm`/`del`/`Remove-Item`, especially for `rm -rf`-class operations and directories with unknown contents. Never run the trash store's clean/purge command -- emptying recovery stores is a human-only action.

### 2. Back Up Before Git Operations That Can Destroy Work
Never run working-tree-destroying git commands (`reset --hard`, `checkout --`/`restore`, `clean -fd`, `stash drop`) without first `git stash` (or a manual backup) and a `git status` check. Config files often contain secrets that are NOT in git — losing them can be catastrophic. Assume any local work is important.

### 3. NEVER COMMIT OR PUSH WITHOUT EXPLICIT USER APPROVAL
Complete a code review, wait for explicit approval, let the user initiate. Commits are a sign-off only the user can authorize. No exceptions.

### 4. Always Use Absolute Paths for Destructive Commands
`sudo rm -rf "/full/path/to/target"` -- never `cd dir && rm -rf subdir` (if the cd fails, the delete runs somewhere else).

### 5. Never Branch-Switch a Live Home-Directory Repo
If your home directory is itself a git repo (e.g. for config backup), branch switching clobbers unstaged working files. All branch work happens in **worktrees at separate paths**; the home repo stays on its main branch at all times.

## Testing: Pair Automated Tests with a Human Test Checklist

Whenever you finish a meaningful batch of automated tests — for a phase, feature, or refactor (even a "no user-visible change" refactor) — **also produce a human test checklist** via `/test-checklist`. Automated tests catch regressions in mocked behavior; human checklists catch what mocks systematically miss: shell rendering, real subprocess behavior, interactive prompts, cross-platform quirks, error-message clarity, and UX problems that only surface in real use. Checklists live in `tests/checklists/` (public, default) with `vX.Y.Z__<Type>__<slug>.md` naming. Rule of thumb: if unsure whether a commit needs a checklist, write one.

### Script Graduation Path
One-off scripts evolve: `tests/one-offs/` (start here; keep them — they document what you did) → `tests/` (proved regression value) or `scripts/` (proved utility value) → project source (became integral).

## DEV WORKFLOW PROCESS

For any decision where multiple approaches exist or risk is non-trivial: run `/dev-workflow-process`. Four stages (SPCR): (1) **Problem Analysis** — begin with the user's complete verbatim request, facts with certainty levels, goals; (2) **Considerations** — constraints, edge cases, long-term implications; (3) **Solutions Evaluation** — genuinely distinct alternatives with strengths/weaknesses/edge cases each; (4) **Synthesis & Recommendation** — the chosen path, why, acceptance checks, and a PUVM summary. Write it to `./private/claude/YYYY-MM-DD__hh-mm-ss__dev-workflow-process__(topic).md` — the reasoning, not just the conclusion, is the artifact.

## Postmortems

Create postmortems (via `/postmortem`, `/fullpostmortem`, `/minipostmortem`, `/contextpostmortem`) for complex implementations, problem resolutions, architecture changes, and major deployments. **Always include the user's complete verbatim triggering message.** Save to `./private/claude/` (project) or `~/claude/` (cross-project) with timestamped filenames. Good postmortems save hours: they document exactly how things were done and what pitfalls to avoid — they are what `/wherearewe` and `/familiarize` read next session.

## Plan Mode Output Preservation

When exiting plan mode with an approved plan, save a copy to `./private/claude/YYYY-MM-DD__hh-mm-ss__claude-plan__(topic).md`. Plans are decision points — preserving them creates the audit trail of "what was the plan" vs "what actually happened" (the postmortem).

## Git & GitHub Conventions

- **Never** include attribution ("Generated with...", "Co-Authored-By") in commit messages.
- Use annotated tags with messages, never lightweight tags.
- **Never auto-close GitHub issues** after implementing fixes — leave them open for user verification.
- Track session continuity with `CurrentTask` (green, one per repo) and `NextTask` (gold) labels.
- Create labels before issues that use them (`gh label create` first — `--label` fails on missing labels).
- Reference analysis documents in issues **by filename only** — never the private directory path.
- Use `--body-file` for issue comments (shell escaping mangles complex markdown); keep drafts in `private/claude/issues/`.
- Prefer a full-context issue reader (e.g. `scripts/gh_issue_full.py N --full`, or `scripts/repokit-common/...` per repo layout) over `gh issue view` — comments and timeline are where the context lives.

## [FILL IN] Your Development Environment

> Describe your machines and layout so Claude works with your reality. Example shape:

- **OS / machines**: e.g. "Windows 11 desktop (primary dev), Linux VPS (services), MacBook (mobile)"
- **Primary code location**: e.g. `~/code/` — all projects live here (set `CLAUDE_CODE_ROOTS` for the cross-project skills)
- **Shared/network tooling**: e.g. a network drive or dotfiles repo mounted consistently across machines
- **Anything Claude should never touch**: production paths, mounted shares, etc.

## [FILL IN] Your Project Inventory

> A short table of active projects and one-line purposes helps Claude orient instantly. Keep it current — it's the map `/wherearewe` supplements.

## [FILL IN] Your Task-Management Integration

> If you use an external task system (Todoist, Linear, Jira...), state the rules Claude must respect — especially which fields/labels Claude may NEVER set without explicit instruction (priorities and planning horizons are the classic trap: only you know what belongs in "this week's plan").

## important-instruction-reminders

Do what has been asked; nothing more, nothing less. NEVER create files unless they're absolutely necessary for achieving your goal. ALWAYS prefer editing an existing file to creating a new one. Never proactively create documentation files unless explicitly requested.
