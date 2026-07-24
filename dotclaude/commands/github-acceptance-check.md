# GitHub Acceptance Criteria Check

Check acceptance criteria for a GitHub issue against the current staged/committed changes.

## Usage

```
/github-acceptance-check #N [#M ...]
```

Where N, M are issue numbers. If no numbers given, scan the staged commit message for issue references.

## Instructions

### 1. Identify Issues to Check

- Parse arguments for issue numbers (e.g., `#24`, `24`, `#3 #22`)
- If no arguments: read the commit message file in `private/claude/commits/` (most recent) and extract all `Refs #N`, `Closes #N`, `Related: #N` references
- If no commit message file: check `git diff --cached` for issue references in changed files

### 2. Fetch Each Issue

For each issue number, use the project's `gh_issue_full.py` if available:
```bash
python scripts/gh_issue_full.py N --full --repo OWNER/REPO
```

Fallback to:
```bash
gh issue view N --json body --jq '.body'
```

### 3. Extract Acceptance Criteria

Look for a section containing checkboxes:
- `### Acceptance Criteria` or `### Acceptance criteria`
- Lines matching `- [ ]` or `- [x]`
- If no checkboxes found, look for any bulleted list under "Acceptance" or "Criteria" headings

### 4. Compare Against Changes

For each criterion:
- Check staged changes (`git diff --cached`) and recent commits for evidence of implementation
- Search the codebase for relevant function names, settings, UI elements mentioned in the criterion
- Mark each as: **DONE**, **PARTIAL**, **NOT DONE**, or **N/A**

### 5. Determine Issue Verb

Based on the check results, recommend the appropriate reference verb:

| Result | Verb | When |
|--------|------|------|
| All criteria met | `Closes #N` | Every checkbox could be checked |
| Most criteria met, remainder tracked | `Refs #N` | Substantial progress, some items remain |
| Minor/tangential progress | `Related: #N` | Loose association, not the main work |
| No criteria addressed | Drop reference | Don't reference issues we didn't touch |

### 6. Report

Present a table:

```
## Issue #N: [Title]

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Keybinding map in storage | NOT DONE | No storage code for keybindings |
| 2 | Click-to-record UI | NOT DONE | No recording logic |
| ... | ... | ... | ... |

Recommendation: Related: #N (interim step, core feature not implemented)
```

### 7. Offer to Comment (Conditional)

Only offer to post a progress comment to the issue if:
- At least one criterion is DONE or PARTIAL
- The commit being prepared actually addresses the issue substantively (not just tangentially)
- There isn't already a recent progress comment (check last comment date)

If warranted, draft the comment to `private/claude/issues/issue_N_YYYY.MM.DD_NN.md` and offer to post.

If NOT warranted (e.g., `Related:` with no real progress), say:
> "No progress comment needed -- this commit is tangentially related, not a direct implementation."

## Notes

- This command is typically run after `/prepcommit` and before `/commit`
- It helps catch incorrect `Closes` verbs (claiming to close an issue that isn't fully done)
- It prevents commit message references to issues we didn't meaningfully touch
- The acceptance criteria check is about ACCURACY, not thoroughness -- better to under-claim than over-claim
- Never auto-post comments -- always ask the user first
