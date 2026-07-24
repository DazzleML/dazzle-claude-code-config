# Platform support

The collection is markdown-first and platform-neutral by design; the executable edges have per-OS notes.

| Platform | Status | Notes |
|---|---|---|
| Windows 10/11 | **Tested** (primary dev) | Bash scripts (`dotclaude/scripts/*.sh`, hooks) run under Git Bash; use `python scripts/install-hooks.py` rather than the `.sh`; the tester-unbounded hook path needs an absolute home path in the agent frontmatter (`~` may not expand in the hook shell); mind the codepage rules the orchestrator CLAUDE.md documents |
| Linux | Expected | All POSIX paths native; `python3` vs `python` may need adjusting in hook frontmatter |
| macOS | Expected | As Linux |
| BSD | Expected | As Linux; the toolkit assumes only git + Python 3.10+ |

"Tested" = the maintainers use it daily. "Expected" = no known platform-specific code, not yet regularly exercised — reports welcome on the [Quick Notes issue](https://github.com/DazzleML/dazzle-claude-code-config/issues/2).

Deliberate cross-platform choices: ASCII-only in anything cmd/PowerShell-adjacent, `{{NODE}}`/`{{USER_CLAUDE}}` templating instead of hardcoded paths, `CLAUDE_CODE_ROOTS` instead of a fixed project layout, and Python for anything that must run identically everywhere.
