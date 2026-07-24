#!/usr/bin/env python3
"""stage-dotclaude-noise.py — Stage all transient/noise directories in ~/.claude

Usage: python ~/claude/scripts/stage-dotclaude-noise.py [--dry-run] [--commit]

Noise directories are Claude Code internal state that changes frequently
but has no functional significance. Committing them separately keeps
real edits clean in git history.

Options:
  --dry-run   Show what would be staged without doing it
  --commit    Stage AND commit with a standard noise message
  (default)   Stage only, no commit
"""

import os
import sys
import subprocess
import tempfile

# Noise directories — transient Claude Code state, no functional value
NOISE_DIRS = [
    "debug",
    "file-history",
    "session-states",
    "shell-snapshots",
    "shell-snapshots.bak",
    "paste-cache",
    "todos",
    "tasks",
    "sesslogs",
    "telemetry",
    "statsig",
    "plugins/cache",
]

def run_git(*args, cwd=None):
    """Run a git command and return (returncode, stdout)."""
    result = subprocess.run(
        ["git"] + list(args),
        capture_output=True, text=True, cwd=cwd
    )
    return result.returncode, result.stdout.strip()


def count_changes(target, cwd):
    """Count git status changes for a path."""
    rc, out = run_git("status", "--short", "--", target, cwd=cwd)
    if rc != 0 or not out:
        return 0
    return len([line for line in out.splitlines() if line.strip()])


def stage_dir(target, cwd):
    """Stage a directory, handling both existing and deleted paths."""
    # Try normal add with --ignore-errors for Windows path length issues
    rc, _ = run_git("add", "--ignore-errors", "--", target, cwd=cwd)
    if rc != 0:
        # Fallback: stage only tracked (deleted) files
        run_git("add", "--ignore-errors", "-u", "--", target, cwd=cwd)


def main():
    dry_run = "--dry-run" in sys.argv
    do_commit = "--commit" in sys.argv

    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    git_root = os.path.expanduser("~")
    claude_dir = os.path.join(git_root, ".claude")

    if not os.path.isdir(claude_dir):
        print(f"Error: {claude_dir} not found")
        return 1

    # Verify we're in a git repo
    rc, _ = run_git("rev-parse", "--git-dir", cwd=git_root)
    if rc != 0:
        print(f"Error: {git_root} is not a git repository")
        return 1

    total_files = 0
    staged_dirs = []

    for dirname in NOISE_DIRS:
        target = os.path.join(".claude", dirname)

        count = count_changes(target, cwd=git_root)
        if count > 0:
            if dry_run:
                print(f"  {target}/  ({count} files)")
            else:
                stage_dir(target, cwd=git_root)
            total_files += count
            staged_dirs.append(dirname)

    if total_files == 0:
        print("No noise changes to stage.")
        return 0

    if dry_run:
        print()
        print(f"Would stage {total_files} files across {len(staged_dirs)} directories.")
        print("Run without --dry-run to stage.")
        return 0

    print(f"Staged {total_files} files across {len(staged_dirs)} noise directories:")
    for d in staged_dirs:
        print(f"  .claude/{d}/")

    if do_commit:
        dir_list = ", ".join(staged_dirs)
        msg = (
            "~/.claude noise: sync transient state files\n"
            "\n"
            "Automated/transient data accumulated since last commit.\n"
            f"Directories: {dir_list}\n"
            "No functional changes — purely Claude Code internal state files."
        )

        # Write message to temp file for commit
        fd, msg_path = tempfile.mkstemp(suffix=".txt", prefix="commit-msg-")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(msg)
            rc, out = run_git("commit", "-F", msg_path, cwd=git_root)
            if rc != 0:
                print(f"Commit failed: {out}")
                return 1
            print()
            print("Committed.")
        finally:
            os.unlink(msg_path)
    else:
        print()
        print("Staged only. Review with: git diff --cached --stat")

    return 0


if __name__ == "__main__":
    sys.exit(main())
