# Customization checklist — make it yours

Everything in this collection that expects *your* values, in one place. Work top to bottom; most items are one-time. (`ccs bootstrap` will eventually walk you through this interactively — tracked in [dazzle-claude-config](https://github.com/DazzleML/dazzle-claude-config/issues).)

## Directories to create

| Path | Purpose | Used by |
|---|---|---|
| `~/claude/` | Your durable territory — notes, scripts, backups; safe from Claude Code cleanup | postmortems, `/analysis`, backups |
| `~/claude/scripts/` | Home of the guard + statusline scripts | `settings-example` wiring |
| `./private/claude/` (per project) | The project vault — design docs, postmortems, notes | `/dev-workflow-process`, postmortem family, `/wherearewe`, `/obsidian` |

## Environment variables

| Variable | What it does | Needed by | Default |
|---|---|---|---|
| `CLAUDE_CODE_ROOTS` | Space-separated list of your project root dirs for cross-project scans | `wherearewe`, `whereweare` | `~/code` |
| `GEMINI_API_KEY` / `OPENROUTER_API_KEY` | External-model keys (bring your own) | `collaborate1/2/3` (optional — `collabN-local` needs neither) | — |

## Placeholders to substitute

| Placeholder | Where | Replace with |
|---|---|---|
| `{{NODE}}` | `settings-example/settings.base.json` | Your node binary (defaults in `vars.windows.json` / `vars.posix.json`) |
| `{{USER_CLAUDE}}` | same | Your `~/claude` directory, absolute path |
| `<CODE_ROOT>` | `create-project`, `repokit-setup`, `bump-merge*` docs | Your projects root (e.g. `~/code`) |

## Files to personalize

- **`~/claude/claude-config/*.md`** — your environment, project inventory, and task rules. The orchestrating `dotclaude/CLAUDE.md` **imports** these via `@~/claude/claude-config/...` memory imports, so you edit YOUR files and never the shared one — upstream updates always merge cleanly. Templates are seeded on first apply (never overwritten). The CLAUDE.md itself is applied `seed-if-absent` too.
- **`~/.claude/settings.local.json`** — machine-local settings, seeded from `settings-example/settings.local.seed.json`, never synced.
- **`dotclaude/commands/obsidian.md`** — the example topic folders/tags are one project's; adapt to your subjects.

## Installs (one-time per machine)

1. Hooks for this repo's own guards (if you fork): `python scripts/install-hooks.py` (any OS; `sh scripts/install-hooks.sh` on POSIX)
2. The tester-unbounded guard: copy `dotclaude/hooks/tester-unbounded-guard.py` to `~/.claude/hooks/` — **Windows**: put the absolute path in the agent frontmatter (`~` may not expand in the hook shell)
3. Plugin marketplaces (optional): `claude plugin marketplace add` for the entries in `settings-example/plugins.json`
4. Ecosystem tools the docs reference (all optional): [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) (`dz safedel`, `dz private-init`), [git-repokit-common](https://github.com/DazzleTools/git-repokit-common) (ships as `scripts/repokit-common/` in this repo)
