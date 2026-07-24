# Commands

Where each command sits in the [workflow](../../docs/workflow.md):

| Stage | Commands |
|---|---|
| Orient | `analysis` (estimative-language assessment), `ask`/`askq` (async background research), `longask`/`quick-ask` (blocking research) |
| Design | `collaborate1/2/3` (external-model consultation rounds via Zen MCP) |
| Track | `github-issue` (issue template + quality checklist) |
| Capture | `addendum` (append to active design doc), `obsidian` (vault note), `docidea` (idea capture) |
| Gate | `github-acceptance-check`, `prepcommit`, `version-bump`, `check-deps` |
| Ship | `github-release`, `github-release-notes`, `bump-merge-release`, `bump-merge-rel-submod` |
| Project setup | `repokit-post` (post-creation setup), `cleanup-priv-claude` (vault housekeeping) |
| Commit | `commit` (diff review → message → sign-off ceremony) |
| Reflect | `postmortem`, `fullpostmortem`, `fullpostmortem-lean`, `minipostmortem`, `contextpostmortem` |

Commands invoke as `/name`. The gate/commit family assumes the timestamped-docs and `private/claude/` conventions described in the workflow doc.
