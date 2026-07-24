# Skills

Where each skill sits in the [workflow](../../docs/workflow.md):

| Skill | Stage | Role |
|---|---|---|
| `familiarize` | Orient | Rebuild project context at session start (reads the docs the postmortems wrote) |
| `dev-workflow-process` | Design | Structured Story→Puzzle→Content→Result analysis, written to a durable doc |
| `collabN-local` | Design | N-round consultation with the repo-aware `brainstorm` agent (no external APIs) |
| `oracle` | Design / Librarian | Query the knowledge vault with traced, sourced answers |
| `merge-3-way-split` | Restructure | Read-only pre-merge review of dual-touched files |
| `test-checklist` | Verify | Human-runnable checklist covering what mocks can't |
| `double-check` | Cross-cutting | Claim-by-claim validation of outward communications |
| `wherearewe` | Orient | Inbound context recovery — "what's going on in this project?" |
| `investigate` | Orient/Design | Structured investigation: gather from files/issues/git, synthesize, plan |
| `move-code` | Restructure | Copy-don't-rewrite code migration |
| `whereweare` | Reflect | Forward-looking snapshot for resuming after time away |
| `create-project` | Project setup | Full GitHub repo creation workflow (template, subtree, issues, release) |
| `github-issues-setup` | Project setup | Standard evergreen issues (#Roadmap, #Quick Notes) + label set |
| `repokit-setup` | Project setup | Set up a project on the repokit template + common subtree |

Skills invoke as `/name` in Claude Code. Each SKILL.md is self-contained; cross-references to not-yet-published components degrade gracefully.
