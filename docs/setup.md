# Full setup guide

The exhaustive version of the README's quickstart — every step from a bare machine to a fully configured Claude Code with this collection, the companion plugins, and multi-machine sync. Skip freely; each section says what it's for. The one-page value checklist ([customization.md](customization.md)) is the companion to this procedural guide.

## 0. Prerequisites

- **git** and **Python 3.10+** (for ccs and several tools)
- **Claude Code** itself — per the [official quickstart](https://code.claude.com/docs/en/quickstart):
  - macOS/Linux/WSL: `curl -fsSL https://claude.ai/install.sh | bash`
  - Windows PowerShell: `irm https://claude.ai/install.ps1 | iex`
  - Windows cmd: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- Optional but referenced by parts of the toolkit: **node** (Bash-guard hook + statusline), **gh** CLI (GitHub workflow commands), [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) (`dz safedel`, `dz private-init`, `dz git-snapshot`)

## 1. Decide: fork or consume

- **Fork this repo** (recommended) — your fork becomes *your* config payload: you'll collect your own skills into it and pull upstream waves when you want. Keep it private or public as you like.
- **Consume directly** — clone this repo as a read-only base; fine for trying things out.

## 2. Get the collection onto the machine

```bash
pip install dazzle-claude-config          # the ccs sync tool
git clone <your-fork-or-this-repo> ~/claude/dazzle-claude-code-config-public
ccs apply --checkout-dir ~/claude/dazzle-claude-code-config-public
```

What `apply` does: copies skills/commands/agents/hooks/scripts into `~/.claude/`, and **seeds** (only where absent — never overwriting) your global `CLAUDE.md`, the personal files it imports (`~/claude/claude-config/*.md`), and the session-logger plugin config. Re-running is idempotent. `ccs status` shows drift; `ccs collect` moves your local edits back into the checkout (with credential scanning).

**No ccs?** Copy by hand: `dotclaude/*` into `~/.claude/` and `userclaude/claude-config/` into `~/claude/claude-config/`.

## 3. Personalize

1. Edit the three seeded files in `~/claude/claude-config/` — your environment, project inventory, task rules. The orchestrating CLAUDE.md imports them at session load; you never edit the shared file.
2. Set `CLAUDE_CODE_ROOTS` (space-separated project roots; default `~/code`) in your shell profile — the cross-project skills use it.
3. Settings (optional, by hand until ccs `render` ships): follow the README's "Settings templates" section — substitute `{{NODE}}` and `{{USER_CLAUDE}}` in `settings-example/settings.base.json`, install the two `userclaude-example/scripts/` (or delete the `hooks`/`statusLine` blocks), seed `settings.local.json`.

## 4. Companion plugins (optional, recommended)

The wider DazzleML stack this collection pairs with:

```bash
# Session logging (records every session in real time)
claude plugin marketplace add "DazzleML/claude-session-logger"
claude plugin install session-logger@dazzle-claude-plugins

# Session backup (git-backed preservation of ~/.claude, with restore)
pip install claude-session-backup
claude plugin marketplace add "DazzleML/Claude-Session-Backup"
claude plugin install claude-session-backup@dazzle-claude-session-backup
csb setup        # guided git-store initialization + first backup
```

`rust-analyzer-lsp@claude-plugins-official` (in the settings template's enabledPlugins) needs no marketplace add.

## 5. Hooks

- **tester-unbounded guard** (required only if you use that agent): `ccs apply` already placed `tester-unbounded-guard.py` in `~/.claude/hooks/`. **Windows**: edit the agent frontmatter to use your absolute home path (`~` may not expand in the hook shell).
- **Repo guards** (if you forked): `python scripts/install-hooks.py` in your fork installs the credential-scanning pre-push and VERSION/CHANGELOG lockstep hooks. Your personal marker list (names, hostnames you'd never want pushed) goes in `~/claude/private/push-guard-markers.re` — untracked by design.

## 6. Verify

- Start a Claude Code session: the skills should appear (try `/familiarize`), and the CLAUDE.md orchestrator should reflect your imported personal sections.
- `ccs status --checkout-dir ~/claude/dazzle-claude-code-config-public` → `status: clean`.

## 7. More machines

Repeat steps 0.2 and 2 per box (Claude Code install → pip install → clone your fork → `ccs apply`). Your fork is the single source of truth; `ccs collect` + `git push` on one machine, `git pull` + `ccs apply` on another. Machine-local settings stay in each box's `settings.local.json`.

## Troubleshooting

- **Every Bash call fails after adopting settings**: you installed the settings but not the `userclaude-example/scripts/` pair (or vice versa) — see README "Settings templates".
- **`nul` file appears in repos on Windows**: DOS `>NUL` used in a bash context — see the orchestrator CLAUDE.md's null-device gotcha.
- **Skills reference things you don't have**: cross-references to not-yet-published components degrade gracefully (README "Notes for strangers").
