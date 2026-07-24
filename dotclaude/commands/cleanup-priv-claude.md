# Cleanup Private Claude Directory

Systematically review and archive completed design documents from `private/claude/`.

## Usage

```
/cleanup-priv-claude [options]
```

Options (passed as argument text):
- `--dry-run` — assess files but don't move anything (default first pass)
- `--execute` — perform the moves after assessment is approved

## Instructions

### Phase 1: Assessment

1. **List all markdown files** in `./private/claude/` (exclude `issues/`, `done/`, and `CHANGELOG.md`)

2. **For each file**, determine disposition by cross-referencing:
   - Git log: Is the described work committed?
   - GitHub issues: Are referenced issues closed?
   - File content: Are there remaining action items or open questions?
   - Recency: Files from the current day should generally be KEPT

3. **Decision criteria**:
   - **MOVE** if: All described work is shipped, all referenced issues are closed, no remaining action items
   - **KEEP** if: References open issues, contains future design specs, is actively being worked on, or is from the current session
   - When in doubt, KEEP

4. **Present the assessment** as a table:
   ```
   | File | Disposition | Reason |
   |------|-------------|--------|
   ```

5. **Wait for user approval** before proceeding to Phase 2

### Phase 2: Execution

1. **Use `scripts/safe_move.sh`** for each file to move:
   ```bash
   bash scripts/safe_move.sh "private/claude/<filename>" "private/claude/done" "<addendum>"
   ```

2. **Addendum format** for each moved file:
   ```markdown

   ---

   > **Addendum — Archived YYYY-MM-DD**
   >
   > **Status**: COMPLETE — Moved to `done/`
   > **Related Issues**: #N (closed), #M (closed)
   > **Shipped In**: vX.Y.Z
   > **Reason**: [Why this file's work is complete]
   ```

3. **Process in chronological order** (oldest first)

4. **Batch files** by date for efficiency (up to 3-4 per bash call)

### Phase 3: Post-cleanup

1. **Update `CHANGELOG.md`** in `private/claude/` — add a new cleanup section with date, counts, and file dispositions

2. **Update `strategy-docs-index.md`** — mark moved files with `done/` prefix, add any new active docs

3. **Verify counts**:
   ```bash
   ls private/claude/done/*.md | wc -l    # archived
   ls private/claude/*.md | wc -l          # remaining
   ```

4. **Report summary** to user:
   - Files moved (count and list)
   - Files kept (count)
   - Any files that need user decision

## Key Behaviors

- **NEVER modify files that are not being moved** — leave kept files exactly as-is
- **NEVER touch the `issues/` subfolder**
- **Preserve all file timestamps** (CreationTime, LastWriteTime, LastAccessTime) via safe_move.sh
- **Hash-verify all moves** via preserve tool (built into safe_move.sh)
- Use parallel agents to assess files when the count exceeds 20
- Start with `--dry-run` behavior by default; only execute after user confirms

## Prerequisites

- `scripts/safe_move.sh` must exist in the project
- `preserve` tool must be installed (`preserve`)
- PowerShell must be available (for Windows timestamp preservation)
- `private/claude/done/` directory must exist
