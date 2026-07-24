"""Install this repo's git hooks (cross-platform; Windows-friendly).

Usage (any shell):  python scripts/install-hooks.py
Equivalent to scripts/install-hooks.sh for POSIX shells.
"""
import shutil
import stat
import subprocess
import sys
from pathlib import Path


def main() -> int:
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    if top.returncode != 0:
        print("not inside a git repository", file=sys.stderr)
        return 2
    root = Path(top.stdout.strip())
    hooks_src = root / "scripts" / "hooks"
    hooks_dst = root / ".git" / "hooks"
    installed = 0
    for hook in ("pre-commit", "pre-push"):
        src = hooks_src / hook
        if src.is_file():
            dst = hooks_dst / hook
            shutil.copy2(src, dst)
            dst.chmod(dst.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
            print(f"installed: {hook}")
            installed += 1
    if not installed:
        print("no hooks found under scripts/hooks/", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
