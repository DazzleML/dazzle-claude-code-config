#!/bin/bash
# stage-dotclaude-noise.sh — Stage all transient/noise directories in ~/.claude
#
# Usage: bash ~/claude/scripts/stage-dotclaude-noise.sh [--dry-run] [--commit]
#
# Noise directories are Claude Code internal state that changes frequently
# but has no functional significance. Committing them separately keeps
# real edits clean in git history.
#
# Options:
#   --dry-run   Show what would be staged without doing it
#   --commit    Stage AND commit with a standard noise message
#   (default)   Stage only, no commit

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
GIT_ROOT="$HOME"

# Noise directories — transient Claude Code state, no functional value
NOISE_DIRS=(
    debug
    file-history
    session-states
    shell-snapshots
    shell-snapshots.bak
    paste-cache
    todos
    tasks
    sesslogs
    telemetry
    statsig
    plugins/cache
)

DRY_RUN=false
DO_COMMIT=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --commit)  DO_COMMIT=true ;;
        --help|-h)
            echo "Usage: $0 [--dry-run] [--commit]"
            echo "  --dry-run   Show what would be staged"
            echo "  --commit    Stage and commit with standard message"
            echo "  (default)   Stage only"
            exit 0
            ;;
        *) echo "Unknown option: $arg"; exit 1 ;;
    esac
done

cd "$GIT_ROOT"

total_files=0
staged_dirs=()

for dir in "${NOISE_DIRS[@]}"; do
    target=".claude/$dir"

    # Count changes (staged + unstaged + deleted)
    count=$(git status --short -- "$target" 2>/dev/null | wc -l)
    count=$((count))  # trim whitespace

    if [ "$count" -gt 0 ]; then
        if $DRY_RUN; then
            echo "  $target/  ($count files)"
        else
            # Use --ignore-errors to skip files with paths too long for Windows
            git add --ignore-errors "$target" 2>/dev/null || \
                git add --ignore-errors -u "$target" 2>/dev/null || true
        fi
        total_files=$((total_files + count))
        staged_dirs+=("$dir")
    fi
done

if [ "$total_files" -eq 0 ]; then
    echo "No noise changes to stage."
    exit 0
fi

if $DRY_RUN; then
    echo ""
    echo "Would stage $total_files files across ${#staged_dirs[@]} directories."
    echo "Run without --dry-run to stage."
    exit 0
fi

echo "Staged $total_files files across ${#staged_dirs[@]} noise directories:"
for d in "${staged_dirs[@]}"; do
    echo "  .claude/$d/"
done

if $DO_COMMIT; then
    MSG_FILE=$(mktemp)
    dir_list=$(printf ', %s' "${staged_dirs[@]}")
    dir_list=${dir_list:2}  # trim leading ", "

    cat > "$MSG_FILE" <<MSGEOF
~/.claude noise: sync transient state files

Automated/transient data accumulated since last commit.
Directories: $dir_list
No functional changes — purely Claude Code internal state files.
MSGEOF

    git commit -F "$MSG_FILE"
    rm -f "$MSG_FILE"
    echo ""
    echo "Committed."
else
    echo ""
    echo "Staged only. Review with: git diff --cached --stat"
fi
