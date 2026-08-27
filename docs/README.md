# Docs

| Doc | What it covers |
|---|---|
| [workflow.md](workflow.md) | How the toolkit flows together — the orient → design → track → implement → verify → gate → commit → ship → reflect lifecycle, its two stage drivers (`/first-mile`, `/last-mile`) and the whole-run driver (`/gauntlet`), the `/measure` · `/poc` · `/double-check` guards, and the two-session "librarian" pattern |
| [project-structure.md](project-structure.md) | The repeatable project shape the skills assume — the `private/` vault (`dz private-init`), the repokit-common subtree, the dazzlecmd-first graduation path, task tracking, and the creation process |
| [setup.md](setup.md) | The exhaustive install walk — Claude Code itself, ccs, personalization, companion plugins (session-logger, csb), hooks, verification, multi-machine rollout |
| [platforms.md](platforms.md) | Per-OS support status and the deliberate cross-platform design choices |
| [customization.md](customization.md) | The make-it-yours checklist — every directory, env var, placeholder, and imported personal file (`~/claude/claude-config/`) that expects your values, plus one-time installs |

Per-folder member guides live beside the assets themselves: [skills](../dotclaude/skills/README.md) · [commands](../dotclaude/commands/README.md) · [agents](../dotclaude/agents/README.md).

Planned: per-skill deep dives (worked examples of `/dev-workflow-process` and `/double-check` runs), and `ccs bootstrap` guided-onboarding docs once the renderer ships (tracked in [dazzle-claude-config#6](https://github.com/DazzleML/dazzle-claude-config/issues/6)); [customization.md](customization.md) covers settings adoption by hand until then.
