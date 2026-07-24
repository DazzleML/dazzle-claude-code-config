# dazzle-claude-code-config (public base)

A curated, working set of **Claude Code** skills, commands, and agents from the DazzleML toolchain — usable directly as a [ccs](https://github.com/DazzleML/dazzle-claude-config) payload repo, or as a grab-bag you copy from by hand.

## What's here (waves 1-2)

| Set | Items |
|---|---|
| **Skills** (7) | `dev-workflow-process` (structured problem analysis), `double-check` (claim/number verification with estimative language), `test-checklist` (human test checklists alongside automated tests), `familiarize` (session-start context rebuild), `oracle` (knowledge-vault querying), `collabN-local` (N-round consultation with a repo-aware local agent), `merge-3-way-split` (pre-merge semantic-collision review) |
| **Commands** (12) | The postmortem family (`postmortem`, `fullpostmortem`, `minipostmortem`, `contextpostmortem`, `addendum`), git workflow (`commit`, `prepcommit`, `version-bump`), `analysis` (CIA estimative-language assessment), `github-issue` (issue-writing template), `github-acceptance-check` (AC-vs-implementation verifier), `collaborate1/2/3` (1/2/3-round external-model consultation) |
| **Agents** (5) | `oracle`, `brainstorm`, `senior-engineer`, `tester`, `dwp-background` (background dev-workflow-process runner) |

**Conventions these files assume**: durable notes live in `~/claude/` (user territory, safe from Claude Code cleanup) and per-project notes in `./private/claude/` (a gitignored project vault). One paragraph of setup gets you the whole system: create those two directories and the files just work.

**External integrations (optional)**: `collaborate1/2/3` require the open-source [Zen MCP server](https://github.com/BeehiveInnovations/zen-mcp-server) configured with a `GEMINI_API_KEY` and/or `OPENROUTER_API_KEY` (names only — bring your own); `collabN-local` is the no-external-API alternative and uses the included `brainstorm` agent as its default consultant. `github-acceptance-check` uses `gh_issue_full.py` from [git-repokit-common](https://github.com/DazzleTools/git-repokit-common) when present, with a plain `gh` fallback. The SPCR/PUVM frameworks referenced by the collaborate family are defined inline in `dev-workflow-process` and `analysis`.

## Use it

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

## Related projects

- [dazzle-claude-config](https://github.com/DazzleML/dazzle-claude-config) — `ccs`, the config sync CLI this repo is a payload for
- [claude-session-logger](https://github.com/DazzleML/claude-session-logger) — real-time session logging (Claude Code plugin)
- [Claude-Session-Backup](https://github.com/DazzleML/Claude-Session-Backup) — local session preservation (`csb`)

## License

[GPL-3.0-or-later](LICENSE).
