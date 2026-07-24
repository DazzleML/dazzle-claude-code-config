#!/bin/sh
# Install this repo's git hooks (VERSION/CHANGELOG lockstep + the personal-marker
# and credential push guard). Run once per clone: sh scripts/install-hooks.sh
set -e
cd "$(git rev-parse --show-toplevel)"
for hook in pre-commit pre-push; do
    if [ -f "scripts/hooks/$hook" ]; then
        cp "scripts/hooks/$hook" ".git/hooks/$hook"
        chmod +x ".git/hooks/$hook"
        echo "installed: $hook"
    fi
done
