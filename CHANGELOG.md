# Changelog

All notable changes to the public Claude Code config collection. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions are semantic (MAJOR: breaking layout/convention changes; MINOR: new payload assets -- skills/commands/agents/templates a consumer applies; PATCH: docs, fixes, scrubs).

## [Unreleased]

### Changed
- `docs/workflow.md`: the lifecycle gains a re-entrant **Steer** layer (`/whatnext`, `/recap-wherearewe`), the `/measure` and `/rethink` guards inside Design, `/last-mile` as the driver of Gate → Commit → Ship, `/test-mutation` beside `/test-checklist`, and `/obsidian-init` / `/obsidian-update` for the vault. Several of these skills are not yet in this collection; they arrive with the next skill promotion, and until then the page describes the toolkit the collection is converging on.

### Fixed
- `scripts/repokit-common/generate-backlinks.py` skips any `_links/` directory in a vault, so navigation junctions to other vaults are neither indexed as local notes nor followed into a cycle. Matches the same fix upstream in git-repokit-common.

## [0.4.7] - 2026-07-25

### Changed
- `dotclaude/CLAUDE.md`: new "Shorthand codes: where they belong, and the `Key:` footer" section under Git & GitHub Conventions. Names the three families of private vocabulary a project accumulates (shorthand codes, acronyms and tool nicknames, repurposed jargon), gives one test for all of them, and splits by audience -- codes are fine in commits, design docs, and issues; checklists shipped to external testers need a legend table; CHANGELOG, README, release notes, and CLI output get plain language and no codes. Includes the `Key:` block format and why the defining-doc citation is mandatory even when a code is glossed inline

## [0.4.6] - 2026-07-24

### Changed
- README: the context-percentage statusline gets a visible callout in the inventory (was buried in the settings section)

## [0.4.5] - 2026-07-24

### Fixed
- README wording pass; Zen MCP renamed to PAL MCP (aka Zen MCP)

## [0.4.4] - 2026-07-24

### Added
- CONTRIBUTING.md (config-collection ground rules, guard hooks, PR workflow), docs/platforms.md + Platform badge, Contributing/support + copyright-license README footer (house format)

## [0.4.3] - 2026-07-24

### Added
- README Install quickstart (5 steps, above the inventory) and `docs/setup.md` — the exhaustive setup walk: Claude Code install, fork-vs-consume, ccs apply, personalization, companion plugins (session-logger + csb), hooks, verification, multi-machine rollout, troubleshooting

## [0.4.2] - 2026-07-24

### Fixed
- docs/README.md index: customization.md was missing; project-structure row and planned-docs note refreshed

## [0.4.1] - 2026-07-24

### Changed
- **The orchestrator now uses memory imports**: the [FILL IN] sections became `@~/claude/claude-config/*.md` imports -- your personal content lives in seeded, user-owned files, so the shared CLAUDE.md never needs editing and upstream updates always merge cleanly
- Cross-platform hook installer: `python scripts/install-hooks.py` (the `.sh` remains for POSIX shells)

### Added
- `userclaude/claude-config/` seed templates (environment, projects, task-rules) + manifest `userclaude` territory with seed-if-absent entries

## [0.4.0] - 2026-07-24

### Added
- **The orchestrator**: `dotclaude/CLAUDE.md` public variant with [FILL IN] invitation sections (applied `seed-if-absent`)
- Wave 3 (all remaining skills): `wherearewe` + `whereweare` (now with configurable `CLAUDE_CODE_ROOTS`), `investigate` (skill + agent), `move-code`, `create-project`, `github-issues-setup`, `repokit-setup`
- Batch 3 commands: `github-release`, `github-release-notes`, `ask`/`askq`/`longask`/`quick-ask` (+ async scripts), `bump-merge-release`, `bump-merge-rel-submod`, `repokit-post`, `fullpostmortem-lean`, `check-deps`, `cleanup-priv-claude`
- Batch 3 agents: `help`, `code-finder`, `project-manager-backlog`, `gpt-codex`
- `plugins-settings/session-logger.json` (seed-if-absent), `docs/customization.md` (the make-it-yours checklist), `docs/project-structure.md` additions (graduation path, task tracking)
- Manifest entries: `scripts`, `plugins-settings`, `CLAUDE.md`

### Changed
- Pre-push guard redesigned: generic patterns ship in-repo; personal marker lists load from an untracked local file (the mechanism travels with forks, the maintainer's list never does)
- README/workflow/folder docs updated to the full inventory (14 skills / 28 commands / 11 agents)

## [0.3.0] - 2026-07-24

### Added
- `tester-unbounded` agent with its required PreToolUse guard hook (`dotclaude/hooks/`, new manifest entry — the pair ships together)
- `obsidian` and `docidea` capture commands
- `settings-example/` — templated `settings.base.json` (battle-tested permission allow/ask lists), OS overlays, vars, local seed, `plugins.json`
- `userclaude-example/scripts/` — Bash-guard hook + context statusline the settings wire up
- `docs/workflow.md` — the toolkit lifecycle (orient → design → verify → gate → commit → ship → reflect, plus the librarian pattern); per-folder READMEs mapping members to stages
- Versioning: this VERSION file + changelog; `.gitignore`

## [0.2.0] - 2026-07-24

### Added
- Wave 2 batch 1: `collaborate1/2/3` + `collabN-local` consultation family, `dwp-background` agent, `analysis`, `github-issue`, `github-acceptance-check`, `merge-3-way-split`
- README: conventions paragraph, optional-integrations notes

## [0.1.0] - 2026-07-24

### Added
- First curated seed: 5 skills (`dev-workflow-process`, `double-check`, `test-checklist`, `familiarize`, `oracle`), 8 commands (postmortem family, `commit`, `prepcommit`, `version-bump`), 4 agents (`oracle`, `brainstorm`, `senior-engineer`, `tester`)
- Working `ccs-manifest.json`, README, GPL-3.0-or-later license

[Unreleased]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.6...HEAD
[0.4.6]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/DazzleML/dazzle-claude-code-config/releases/tag/v0.4.0
[0.3.0]: https://github.com/DazzleML/dazzle-claude-code-config/releases/tag/v0.3.0
[0.2.0]: https://github.com/DazzleML/dazzle-claude-code-config/commits/861837b
[0.1.0]: https://github.com/DazzleML/dazzle-claude-code-config/commits/bdd9481
