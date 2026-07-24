# dazzle-claude-code-config (public base)

[![Version](https://img.shields.io/github/v/release/DazzleML/dazzle-claude-code-config?include_prereleases&label=version&color=blue)](https://github.com/DazzleML/dazzle-claude-code-config/releases) [![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0--or--later-green)](LICENSE) [![Changelog](https://img.shields.io/badge/changelog-keep--a--changelog-orange)](CHANGELOG.md) [![Claude Code](https://img.shields.io/badge/for-Claude%20Code-blueviolet)](https://code.claude.com)

A curated, working set of **Claude Code** skills, commands, and agents from the DazzleML toolchain — usable directly as a [ccs](https://github.com/DazzleML/dazzle-claude-config) payload repo, or as a grab-bag you copy from by hand.

**The big idea**: configuration sets should be as easy to share, load in, and swap out as tools are in [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) — fork a set, point ccs at it, layer your own private overlay on top, swap sources at will. This repo is the first public set.

## What's here (waves 1-2)

| Set | Items |
|---|---|
| **Skills** (7) | `dev-workflow-process` (structured problem analysis), `double-check` (claim/number verification with estimative language), `test-checklist` (human test checklists alongside automated tests), `familiarize` (session-start context rebuild), `oracle` (knowledge-vault querying), `collabN-local` (N-round consultation with a repo-aware local agent), `merge-3-way-split` (pre-merge semantic-collision review) |
| **Commands** (14) | The postmortem family (`postmortem`, `fullpostmortem`, `minipostmortem`, `contextpostmortem`, `addendum`), git workflow (`commit`, `prepcommit`, `version-bump`), `analysis` (CIA estimative-language assessment), `github-issue` (issue-writing template), `github-acceptance-check` (AC-vs-implementation verifier), `collaborate1/2/3` (1/2/3-round external-model consultation), `obsidian` (knowledge-vault capture; example topic layout — adapt to your projects), `docidea` (lightweight idea capture) |
| **Agents** (6) | `oracle`, `brainstorm`, `senior-engineer`, `tester`, `dwp-background` (background dev-workflow-process runner), `tester-unbounded` (autonomous testing with safety zones) |
| **Hooks** (1) | `tester-unbounded-guard.py` — PreToolUse enforcement backing `tester-unbounded` (blocks unapproved deletions/mutations); the agent **requires** it at `~/.claude/hooks/` (on Windows, put the absolute home path in the agent frontmatter — `~` may not expand in the hook shell) |
| **Settings templates** | `settings-example/` + `userclaude-example/` — see below |

**Conventions these files assume**: durable notes live in `~/claude/` (user territory, safe from Claude Code cleanup) and per-project notes in `./private/claude/` (a gitignored project vault). One paragraph of setup gets you the whole system: create those two directories and the files just work.

**External integrations (optional)**: `collaborate1/2/3` require the open-source [Zen MCP server](https://github.com/BeehiveInnovations/zen-mcp-server) configured with a `GEMINI_API_KEY` and/or `OPENROUTER_API_KEY` (names only — bring your own); `collabN-local` is the no-external-API alternative and uses the included `brainstorm` agent as its default consultant. `github-acceptance-check` uses `gh_issue_full.py` from [git-repokit-common](https://github.com/DazzleTools/git-repokit-common) when present, with a plain `gh` fallback. The SPCR/PUVM frameworks referenced by the collaborate family are defined inline in `dev-workflow-process` and `analysis`.

## How these fit together

The toolkit is a **workflow**, not a grab-bag: orient (`/familiarize`) → design (`/dev-workflow-process`, the collab family) → track/restructure → verify (`/test-checklist` + tester agents) → gate (`/github-acceptance-check`, `/prepcommit`) → `/commit` → ship → reflect (the postmortem family), with `/double-check` guarding outward comms. **[docs/workflow.md](docs/workflow.md)** walks the full trajectory; each of [`skills/`](dotclaude/skills/), [`commands/`](dotclaude/commands/), and [`agents/`](dotclaude/agents/) has a README mapping its members to the stages.

## Use it

**Fork it — that's the intended path.** Your fork becomes *your* config payload: point [ccs](https://github.com/DazzleML/dazzle-claude-config) at it, `ccs collect` your own skills/commands/agents into it, keep it private or public as you like, and pull upstream waves from here when you want them. (Prefer a clean start with no fork link? Use it as a template instead.) The manifest, guards, and hook installer all travel with the fork — a forked copy is a fully working system on day one.

**With ccs** (`pip install dazzle-claude-config`):

```bash
git clone https://github.com/DazzleML/dazzle-claude-code-config ~/claude/dazzle-claude-code-config-public
ccs apply --checkout-dir ~/claude/dazzle-claude-code-config-public
```

**By hand**: copy what you want from `dotclaude/` into your `~/.claude/` (skills into `skills/`, commands into `commands/`, agents into `agents/`).

## Notes for strangers

- **This is a curated subset.** Some files cross-reference components not (yet) published here — e.g. the `whereweare`/`wherearewe` skills, the `/obsidian` and `/ask` families, session-log conventions, and the `task-manager`-based `t-*` commands. Those references degrade gracefully; more waves are planned.
- **Ecosystem prerequisites are optional.** Some commands mention `dz` ([dazzlecmd](https://github.com/DazzleTools/dazzlecmd)) and repokit scripts ([git-repokit-common](https://github.com/DazzleTools/git-repokit-common)) — public projects, not required for the core skills to work.
- These files encode one team's working conventions (e.g. a `private/claude/` project-notes directory). Adopt or adapt freely — that's what the license is for.

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

## License

[GPL-3.0-or-later](LICENSE).
