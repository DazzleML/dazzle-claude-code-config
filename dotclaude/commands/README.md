# Commands

Where each command sits in the [workflow](../../docs/workflow.md):

| Stage | Commands |
|---|---|
| Orient | `analysis` (estimative-language assessment for question series) |
| Design | `collaborate1/2/3` (external-model consultation rounds via Zen MCP) |
| Track | `github-issue` (issue template + quality checklist) |
| Capture | `addendum` (append to active design doc), `obsidian` (vault note), `docidea` (idea capture) |
| Gate | `github-acceptance-check`, `prepcommit`, `version-bump` |
| Commit | `commit` (diff review → message → sign-off ceremony) |
| Reflect | `postmortem`, `fullpostmortem`, `minipostmortem`, `contextpostmortem` |

Commands invoke as `/name`. The gate/commit family assumes the timestamped-docs and `private/claude/` conventions described in the workflow doc.
