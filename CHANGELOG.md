# Changelog

All notable changes to the public Claude Code config collection. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions are semantic (MAJOR: breaking layout/convention changes, MINOR: new assets or docs, PATCH: fixes/scrubs).

## [Unreleased]

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

[Unreleased]: https://github.com/DazzleML/dazzle-claude-code-config/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/DazzleML/dazzle-claude-code-config/releases/tag/v0.3.0
[0.2.0]: https://github.com/DazzleML/dazzle-claude-code-config/commits/861837b
[0.1.0]: https://github.com/DazzleML/dazzle-claude-code-config/commits/bdd9481
