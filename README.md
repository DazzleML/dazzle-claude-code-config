# dazzle-claude-code-config (public base)

A curated, working set of **Claude Code** skills, commands, and agents from the DazzleML toolchain — usable directly as a [ccs](https://github.com/DazzleML/dazzle-claude-config) payload repo, or as a grab-bag you copy from by hand.

## What's here (first minimal wave)

| Set | Items |
|---|---|
| **Skills** (5) | `dev-workflow-process` (structured problem analysis), `double-check` (claim/number verification with estimative language), `test-checklist` (human test checklists alongside automated tests), `familiarize` (session-start context rebuild), `oracle` (knowledge-vault querying) |
| **Commands** (8) | The postmortem family (`postmortem`, `fullpostmortem`, `minipostmortem`, `contextpostmortem`, `addendum`) + git workflow (`commit`, `prepcommit`, `version-bump`) |
| **Agents** (4) | `oracle`, `brainstorm`, `senior-engineer`, `tester` |

## Use it

**With ccs** (`pip install dazzle-claude-config`):

```bash
git clone https://github.com/DazzleML/dazzle-claude-code-config ~/claude/dazzle-claude-code-config-public
ccs apply --checkout-dir ~/claude/dazzle-claude-code-config-public
```

**By hand**: copy what you want from `dotclaude/` into your `~/.claude/` (skills into `skills/`, commands into `commands/`, agents into `agents/`).

## Notes for strangers

- **This is a curated subset.** Some files cross-reference components not (yet) published here — e.g. `/analysis`, `/collabN-local`, the `whereweare` skills, session-log conventions. Those references degrade gracefully; more waves are planned.
- **Ecosystem prerequisites are optional.** Some commands mention `dz` ([dazzlecmd](https://github.com/DazzleTools/dazzlecmd)) and repokit scripts ([git-repokit-common](https://github.com/DazzleTools/git-repokit-common)) — public projects, not required for the core skills to work.
- These files encode one team's working conventions (e.g. a `private/claude/` project-notes directory). Adopt or adapt freely — that's what the license is for.

## Related projects

- [dazzle-claude-config](https://github.com/DazzleML/dazzle-claude-config) — `ccs`, the config sync CLI this repo is a payload for
- [claude-session-logger](https://github.com/DazzleML/claude-session-logger) — real-time session logging (Claude Code plugin)
- [Claude-Session-Backup](https://github.com/DazzleML/Claude-Session-Backup) — local session preservation (`csb`)

## License

[GPL-3.0-or-later](LICENSE).
