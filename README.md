# dazzle-claude-code-config (public base)

[![Version](https://img.shields.io/github/v/release/DazzleML/dazzle-claude-code-config?include_prereleases&label=version&color=blue)](https://github.com/DazzleML/dazzle-claude-code-config/releases) [![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0--or--later-green)](LICENSE) [![Changelog](https://img.shields.io/badge/changelog-keep--a--changelog-orange)](CHANGELOG.md) [![Claude Code](https://img.shields.io/badge/for-Claude%20Code-blueviolet)](https://code.claude.com) [![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20BSD-lightgrey.svg)](docs/platforms.md)

A curated, working set of **Claude Code** skills, commands, and agents from the DazzleML toolchain usable directly as a [ccs](https://github.com/DazzleML/dazzle-claude-config) payload repo, or as a grab-bag you copy from by hand.

**The big idea**: configuration sets should be as easy to share, load in, and swap out as tools are in [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) — fork a set, point ccs at it, layer your own private overlay on top, swap sources at will. This repo is the first public set.

## Install (quickstart)

1. Have [Claude Code](https://code.claude.com/docs/en/quickstart), git, and Python 3.10+
2. `pip install dazzle-claude-config` (the [ccs](https://github.com/DazzleML/dazzle-claude-config) sync tool)
3. Fork this repo (or clone it directly), then:
   ```bash
   git clone <your-fork-or-this-repo> ~/claude/dazzle-claude-code-config-public
   ccs apply --checkout-dir ~/claude/dazzle-claude-code-config-public
   ```
4. Personalize: edit the seeded `~/claude/claude-config/*.md` (your environment/projects/rules -- the CLAUDE.md imports them) and set `CLAUDE_CODE_ROOTS`
5. Optional companions (session logging, git-backed backup) and settings templates: **[docs/setup.md](docs/setup.md)** is the exhaustive walk; **[docs/customization.md](docs/customization.md)** is the checklist

## What's here

| Set | Items |
|---|---|
| **The orchestrator** | `dotclaude/CLAUDE.md` — a curated global memory file that **imports your personal sections** (`@~/claude/claude-config/*.md`, seeded with templates) -- you never edit the shared file, so upstream updates merge easily; applied `seed-if-absent` |
| **Skills** (14) | Orient: `familiarize`, `wherearewe`; Design: `dev-workflow-process`, `collabN-local`, `oracle`, `investigate`; Restructure: `merge-3-way-split`, `move-code`; Verify: `test-checklist`, `double-check`; Reflect: `whereweare`; Project setup: `create-project`, `github-issues-setup`, `repokit-setup` |
| **Commands** (28) | Postmortem family (`postmortem`, `fullpostmortem`, `fullpostmortem-lean`, `minipostmortem`, `contextpostmortem`, `addendum`); git/release (`commit`, `prepcommit`, `version-bump`, `bump-merge-release`, `bump-merge-rel-submod`, `github-release`, `github-release-notes`, `repokit-post`); GitHub (`github-issue`, `github-acceptance-check`); consultation (`collaborate1/2/3`); research (`ask`, `askq`, `longask`, `quick-ask`, `analysis`); capture (`obsidian`, `docidea`); utilities (`check-deps`, `cleanup-priv-claude`) |
| **Agents** (11) | `oracle`, `brainstorm`, `senior-engineer`, `tester`, `tester-unbounded`, `dwp-background`, `investigate`, `help`, `code-finder`, `project-manager-backlog`, `gpt-codex` |
| **Hooks** (1) | `tester-unbounded-guard.py` — PreToolUse enforcement backing `tester-unbounded`; the agent **requires** it at `~/.claude/hooks/` (on Windows, put the absolute home path in the agent frontmatter, as `~` may not expand in the hook shell) |
| **Scripts** | `dotclaude/scripts/` — async research helpers the `/ask` family invokes (installed by the manifest) |
| **Settings templates** | `settings-example/` + `userclaude-example/` — including the **color-coded `ctx ##%` context statusline** (cyan → yellow at 85% → bold-red "wrap up or /compact" at 94%), arguably the best five-minute upgrade here — see below |

**Conventions these files assume**: durable notes live in `~/claude/` (user territory, safe from Claude Code cleanup) and per-project notes in `./private/claude/` (a gitignored project vault). One paragraph of setup gets you the whole system: create those two directories and the files just work.

**External integrations (optional)**: `collaborate1/2/3` require the open-source [PAL MCP (aka Zen MCP) server](https://github.com/BeehiveInnovations/zen-mcp-server) configured with a `GEMINI_API_KEY` and/or `OPENROUTER_API_KEY` (names only — bring your own); `collabN-local` is the no-external-API alternative and uses the included `brainstorm` agent as its default consultant. `github-acceptance-check` uses `gh_issue_full.py` from [git-repokit-common](https://github.com/DazzleTools/git-repokit-common) when present, with a plain `gh` fallback. The SPCR/PUVM frameworks referenced by the collaborate family are defined inline in `dev-workflow-process` and `analysis`. The `help` agent optionally uses Zen MCP; `gpt-codex` requires a Codex MCP server (`mcp__codex__*`/`mcp__gpt-codex__*` names only — bring your own setup).

## How everything fits together

The toolkit is a **workflow**, not a grab-bag: orient (`/familiarize`) → design (`/dev-workflow-process`, the collab family) → track/restructure → implement → verify (`/test-checklist` + tester agents) → gate (`/github-acceptance-check`, `/prepcommit`) → `/commit` → ship → reflect (the postmortem family), with `/double-check` guarding outward comms. **[docs/workflow.md](docs/workflow.md)** walks the full trajectory; each of [`skills/`](dotclaude/skills/), [`commands/`](dotclaude/commands/), and [`agents/`](dotclaude/agents/) has a README mapping its members to the stages.

## Use it

**Fork it — that's the intended path.** Your fork becomes *your* config payload: point [ccs](https://github.com/DazzleML/dazzle-claude-config) at it, `ccs collect` your own skills/commands/agents into it, keep it private or public as you like, and pull upstream waves from here when you want them. (Prefer a clean start with no fork link? Use it as a template instead.) The manifest, guards, and hook installer all travel with the fork — a forked copy is a fully working system on day one.

**With ccs** (`pip install dazzle-claude-config`):

```bash
git clone https://github.com/DazzleML/dazzle-claude-code-config ~/claude/dazzle-claude-code-config-public
ccs apply --checkout-dir ~/claude/dazzle-claude-code-config-public
```

**By hand**: copy what you want from `dotclaude/` into your `~/.claude/` (skills into `skills/`, commands into `commands/`, agents into `agents/`, hooks into `hooks/`, scripts into `scripts/`) — and `userclaude/claude-config/` into `~/claude/claude-config/` so the CLAUDE.md imports resolve.

**Then make it yours**: **[docs/customization.md](docs/customization.md)** is the one-page checklist of every directory, environment variable, placeholder, and imported personal file that expects your values — including `~/claude/claude-config/` (the files the orchestrating CLAUDE.md imports; seeded with templates, never overwritten).

## Notes for strangers

- **This is a curated subset** — now covering nearly the whole toolkit. Still held back: the `task-manager`-based `t-*` commands (their CLI isn't published yet) and a few personal-infrastructure agents. Occasional cross-references to those degrade gracefully.
- **Ecosystem prerequisites are optional.** Some commands mention `dz` ([dazzlecmd](https://github.com/DazzleTools/dazzlecmd)) and repokit scripts ([git-repokit-common](https://github.com/DazzleTools/git-repokit-common)) — public projects, not required for the core skills to work.
- These files encode one team's working conventions (e.g. a `private/claude/` project-notes directory). Adopt or adapt freely, that's what the license is for.

## Settings templates (`settings-example/`, `userclaude-example/`)

These are **examples, not applied by `ccs apply`** (ccs `render` support ships later). By hand:

1. Copy `settings-example/settings.base.json` → `~/.claude/settings.json`, substituting `{{NODE}}` (your node binary; defaults in `vars.windows.json` / `vars.posix.json`) and `{{USER_CLAUDE}}` (your `~/claude` directory).
2. Copy `userclaude-example/scripts/*` → `~/claude/scripts/` — the settings wire a Bash-guard hook and a context statusline to those two scripts. **Install both or delete the `hooks` and `statusLine` blocks**; otherwise every Bash call fails noisily.
3. `settings.local.seed.json` is the starting point for your machine-local `~/.claude/settings.local.json`; the `settings.windows/posix.json` files are OS-overlay stubs.
4. Plugins: the two DazzleML marketplaces in `plugins.json` need `claude plugin marketplace add` first; `rust-analyzer-lsp` needs no add (built-in official marketplace).

**Permissions philosophy**: the allow list trades prompts for speed and reflects one team's risk tolerance. Sharp edges to tune deliberately before adopting: `gh api:*`, `npx:*`, `gh issue edit/reopen`, and `sed` are allowed without prompting — each can mutate state or execute arbitrary code.

## Related projects

- [dazzle-claude-config](https://github.com/DazzleML/dazzle-claude-config) — `ccs`, the config sync CLI this repo is a payload for
- [claude-session-logger](https://github.com/DazzleML/claude-session-logger) — real-time session logging (Claude Code plugin)
- [Claude-Session-Backup](https://github.com/DazzleML/Claude-Session-Backup) — local session preservation (`csb`)

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for:
- Ground rules for a config collection (no personal content; cross-platform conventions; graceful degradation)
- The guard hooks (`python scripts/install-hooks.py`) and VERSION/CHANGELOG lockstep
- The PR workflow and folder-README updates for new payload entries

Like the project?

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/djdarcy)

## License

dazzle-claude-code-config, Copyright (C) 2026 Dustin Darcy

Licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) (GPL-3.0) -- see [LICENSE](LICENSE)
