#!/usr/bin/env python3
"""
tester-unbounded-guard.py

PreToolUse hook for the tester-unbounded subagent.

Reads Bash command from stdin JSON; exits 0 (allow) or 2 (block).
Blocks dangerous mutation commands while allowing test/inspection commands.

Why this exists: Claude Code's `permissions.allow` and `permissions.deny`
rules in settings.json are NOT reliably enforced for Bash commands as of
2026-04-29 (open issues #18846, #13340 in anthropics/claude-code). The
PreToolUse hook is the reliable enforcement mechanism.

Scope: this hook fires ONLY while the tester-unbounded subagent is active
(per the agent's frontmatter `hooks` block). It does not affect the main
session or other subagents.

Allow rules (read-only inspection, test execution, autonomous operations):
  - pytest, python -m pytest, dz, python -m dazzlecmd
  - powershell / pwsh / cmd / bash invocations of test scripts
  - git status, git log, git diff, git show (read-only git)
  - gh issue view, gh pr view, gh sub_issues list (read-only gh)
  - dz safedel (recoverable deletion -- the supported path)
  - Standard read-only utilities (these are also auto-allowed by Claude
    Code's built-in list, but listed here for completeness)

Deny rules (state-mutating operations that should never run autonomously):
  - gh issue create/comment/close/edit/delete
  - gh pr create/close/merge
  - gh release create
  - git push, git commit --amend, git reset --hard, git clean -f,
    git filter-branch
  - Native deletes: rm -rf, rm -f, rmdir, del /s/q/f, Remove-Item, rd /s
    (force the agent to use `dz safedel` for any deletion)
  - Bash writes to protected paths (`src/`, `packages/*/src/`) via
    redirect / cat / tee / cp / mv

Default: ALLOW. The agent's system prompt and warm-up phase already
constrain behavior; the hook catches the explicitly-dangerous patterns.
"""
import json
import re
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If we can't parse the input, fail open (allow) but log to stderr.
        print(
            "[tester-unbounded-guard] WARN: could not parse stdin JSON; allowing",
            file=sys.stderr,
        )
        return 0

    if data.get("tool_name") != "Bash":
        # Only gate Bash; Edit/Write/Read pass through (frontmatter
        # permissionMode acceptEdits + agent system prompt govern those).
        return 0

    cmd = data.get("tool_input", {}).get("command", "")
    if not cmd:
        return 0

    # ---- DENY list: block these unconditionally ----
    deny_patterns = [
        # GitHub state-mutating operations
        (r"\bgh\s+issue\s+create\b", "gh issue create"),
        (r"\bgh\s+issue\s+comment\b", "gh issue comment"),
        (r"\bgh\s+issue\s+close\b", "gh issue close"),
        (r"\bgh\s+issue\s+delete\b", "gh issue delete"),
        (r"\bgh\s+issue\s+edit\b", "gh issue edit"),
        (r"\bgh\s+issue\s+reopen\b", "gh issue reopen"),
        (r"\bgh\s+issue\s+lock\b", "gh issue lock"),
        (r"\bgh\s+pr\s+create\b", "gh pr create"),
        (r"\bgh\s+pr\s+close\b", "gh pr close"),
        (r"\bgh\s+pr\s+merge\b", "gh pr merge"),
        (r"\bgh\s+pr\s+edit\b", "gh pr edit"),
        (r"\bgh\s+pr\s+review\b", "gh pr review"),
        (r"\bgh\s+release\s+create\b", "gh release create"),
        (r"\bgh\s+release\s+delete\b", "gh release delete"),
        (r"\bgh\s+release\s+edit\b", "gh release edit"),
        (r"\bgh\s+repo\s+(create|delete|edit|fork|rename|archive|sync)\b",
         "gh repo state-mutation"),
        (r"\bgh\s+label\s+(create|delete|edit)\b", "gh label state-mutation"),
        (r"\bgh\s+api\s+.*\s-X\s+(POST|PUT|PATCH|DELETE)\b",
         "gh api state-mutation"),

        # Dangerous git operations
        (r"\bgit\s+push\b", "git push"),
        (r"\bgit\s+commit\s+--amend\b", "git commit --amend"),
        (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
        (r"\bgit\s+clean\s+-[a-z]*f\b", "git clean -f"),
        (r"\bgit\s+filter-branch\b", "git filter-branch"),
        (r"\bgit\s+filter-repo\b", "git filter-repo"),
        (r"\bgit\s+rebase\s+--interactive\b", "git rebase --interactive"),
        (r"\bgit\s+rebase\s+-i\b", "git rebase -i"),
        (r"\bgit\s+branch\s+-D\b", "git branch -D"),
        (r"\bgit\s+tag\s+-d\b", "git tag -d"),
        (r"\bgit\s+remote\s+(add|remove|set-url)\b", "git remote modification"),
        (r"\bgit\s+update-ref\b", "git update-ref"),
        (r"\bgit\s+(submodule|worktree)\s+(add|remove)\b",
         "git submodule/worktree state-mutation"),

        # Native destructive deletions (`dz safedel` is the supported path)
        (r"\brm\s+-[a-z]*r[a-z]*f[a-z]*\b", "rm -rf (use dz safedel)"),
        (r"\brm\s+-[a-z]*f[a-z]*r[a-z]*\b", "rm -fr (use dz safedel)"),
        (r"\brm\s+-[a-z]*f\b", "rm -f (use dz safedel)"),
        (r"\brm\s+-[a-z]*r\b", "rm -r (use dz safedel)"),
        (r"\brmdir\b", "rmdir (use dz safedel)"),
        (r"\bdel\s+/[sqfa]", "del /s|/q|/f|/a (use dz safedel)"),
        (r"\bRemove-Item\b", "Remove-Item (use dz safedel)"),
        (r"\brd\s+/s\b", "rd /s (use dz safedel)"),

        # Process killing
        (r"\bkill\s+-9\b", "kill -9"),
        (r"\bkillall\b", "killall"),
        (r"\btaskkill\s+/F\b", "taskkill /F"),
        (r"\bStop-Process\s+-Force\b", "Stop-Process -Force"),
    ]

    for pattern, label in deny_patterns:
        if re.search(pattern, cmd, re.IGNORECASE):
            print(
                f"[tester-unbounded-guard] BLOCKED ({label}): {cmd!r}",
                file=sys.stderr,
            )
            print(
                f"This operation is denied for tester-unbounded. "
                f"For state-mutating operations, return findings to the "
                f"caller and let the main session execute. For deletions, "
                f"use `dz safedel <path>` (recoverable for ~30 days).",
                file=sys.stderr,
            )
            return 2

    # ---- Bash writes to protected source paths via redirect / cat / tee / cp / mv ----
    # Edit/Write tool deny rules don't block Bash file writes to the same
    # paths, so the hook checks Bash patterns that write to source.
    protected_path_patterns = [
        r"(?:^|[\s'\"])src/",
        r"(?:^|[\s'\"])packages/[^/\s'\"]+/src/",
    ]
    write_verb_patterns = [
        # Output redirects to a path: > foo or >> foo
        r">\s*[^&]",
        # tee writing to a path
        r"\btee\s+",
        # Cat / printf / echo writing through redirect (covered by `>` above)
        # cp / mv with destination
        r"\b(?:cp|mv|move|copy)\s+",
        # PowerShell Set-Content / Out-File / Add-Content
        r"\b(?:Set-Content|Out-File|Add-Content)\s+",
    ]

    for write_pattern in write_verb_patterns:
        if re.search(write_pattern, cmd):
            for path_pattern in protected_path_patterns:
                if re.search(path_pattern, cmd):
                    print(
                        f"[tester-unbounded-guard] BLOCKED (Bash write to "
                        f"protected source path): {cmd!r}",
                        file=sys.stderr,
                    )
                    print(
                        f"Real-file edits should go through the Edit/Write "
                        f"tool (which gates inline) or the cautious `tester` "
                        f"agent. If this is intentional, redispatch with the "
                        f"`modify freely` directive.",
                        file=sys.stderr,
                    )
                    return 2

    # ---- Default: allow ----
    return 0


if __name__ == "__main__":
    sys.exit(main())
