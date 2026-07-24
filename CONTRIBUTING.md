# Contributing

Contributions welcome — new skills/commands/agents, scrub improvements, docs, platform reports.

## Ground rules (this is a config collection, not a code package)

1. **No personal content.** Nothing identifying you or anyone else: no absolute personal paths, hostnames, employer/project internals, or credentials. The pre-push guard (`python scripts/install-hooks.py` to install) scans for credential shapes; add your own marker list at `~/claude/private/push-guard-markers.re` (untracked by design).
2. **Cross-platform or clearly labeled.** Follow the conventions in [docs/platforms.md](docs/platforms.md) and the orchestrator CLAUDE.md's gotchas (ASCII in cmd-adjacent scripts, no hardcoded layouts — use `CLAUDE_CODE_ROOTS`/`{{VARS}}`).
3. **Self-contained files.** A skill/command should degrade gracefully when it references something a stranger doesn't have — say so inline.
4. **Versioning is enforced**: bumping `VERSION` requires a matching `CHANGELOG.md` entry (the pre-commit hook checks). MINOR = new payload assets; PATCH = docs/fixes/scrubs.

## Workflow

Open an issue first for anything substantial (the pinned [Roadmap](https://github.com/DazzleML/dazzle-claude-code-config/issues/1) shows direction). Fork → branch → PR. For new payload entries, update the relevant folder README table and, if applicable, `ccs-manifest.json`.

## Like the project?

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/djdarcy)
