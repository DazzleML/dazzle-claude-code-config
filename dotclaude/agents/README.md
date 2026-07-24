# Agents

Where each agent sits in the [workflow](../../docs/workflow.md):

| Agent | Stage | Role |
|---|---|---|
| `oracle` | Design / Librarian | Traverses the knowledge vault (design docs, postmortems, issues) for traced answers; run it in a second session as the "librarian" |
| `brainstorm` | Design | Sparring partner that reads real code and project history; default consultant for `/collabN-local` |
| `senior-engineer` | Design / Build | Expert-level engineering analysis and hands-on fixes |
| `dwp-background` | Design | Runs a full dev-workflow-process analysis cold, in the background |
| `tester` | Verify | Cautious QA: runs checklists, writes tests, reports pass/fail |
| `tester-unbounded` | Verify | Autonomous testing inside safety zones — **requires** `hooks/tester-unbounded-guard.py` installed at `~/.claude/hooks/` (see the hook's docstring; on Windows use an absolute path in the agent frontmatter) |
| `investigate` | Orient/Design | Gathers context from files, issues, git history for new work |
| `help` | Any | Isolated-context research and Q&A (optionally via Zen MCP) |
| `code-finder` | Design | Fast code location across large trees |
| `project-manager-backlog` | Track | Backlog grooming and issue triage |
| `gpt-codex` | Design/Build | External-model code analysis via a Codex MCP server (bring your own) |

Agents are spawned by Claude Code's Task tool or referenced by the skills that use them.
