---
description: Structured git commit workflow - status, diff, add, commit message, code review, sign-off, commit
allowed-tools: Bash, Read, Write, Glob, Grep
---

In essence: let's do a git diff, we'll do a code review, git add, then write a commit message, I'll do a code review & once I sign-off then AND ONLY THEN we can commit (we NEVER commit unless we get approval)

**Git Commit Workflow Process**

Following the structured approach: git status → git diff → git add → git status (loop: repeat git diff / git adds as appropriate) → analyze log conventions → write commit message → code review → sign-off → commit → user handles push

Arguments: "$ARGUMENTS" (optional - specific files to include, or leave empty for interactive selection)

---

## Process Steps:

### 1. **Git Status Check**
First, let's see what files have been modified: `!git status`

### 2. **Git Diff Review**
Show detailed diff of all changes to ensure nothing sensitive or problematic is being committed: `!git diff HEAD`

### 3. **Git Add (Selective)**
Add appropriate files to staging, being careful to exclude:
- Private configuration files (settings.py, .env, etc.)
- Sensitive data or credentials
- Temporary or backup files
- Files that shouldn't be version controlled

For tips of what to add and not add:{
**Context (auto-loaded):**
- **Ignore Rules:** `@.gitignore`
- **Git Hooks:** `!ls -la .git/hooks`
}
The status, diff, gitignore rules, and hook configuration are loaded above. Analyze what changed and flag anything sensitive (credentials, .env, settings files with passwords).

### 4. **Analyze Git Log Conventions**
Before writing the message, study recent commits to match the project's style:

**a) Format analysis** — Run `git log --format="----%n%s%n%n%b" -8` and identify:
- Subject line format: versioned (`v0.7.16: ...`), conventional commits, or plain
- Body structure: categories (Added/Changed/Fixed/Removed), bullet style, line length
- Any project-specific sections (design docs, test counts, technical notes, etc.)

If the project's git log uses or resembles **conventional commits**, follow the spec
(ref: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13):

```
<type>(<optional scope>): <description>

<optional body>

<optional footer>
```

Types: `feat` (new feature), `fix` (bug fix), `refactor`, `perf`, `style` (formatting),
`test`, `docs`, `build` (deps/versions), `ops` (infra/CI/CD), `chore` (maintenance).

Rules:
- Description uses imperative present tense ("change" not "changed"), no capitalization, no period
- Breaking changes: append an exclamation mark before the colon (e.g. feat!: remove endpoint) and/or BREAKING CHANGE: in footer
- Scope is optional contextual info (not issue numbers)
- Footer for issue refs: `Closes #123`, `Refs #456`

**b) GitHub issue references** — Determine which issues to mention:
- Search branch name, commit messages, and changed files for issue numbers
- Check open issues this work addresses: `gh issue list --state open --limit 20`
- Use the correct verb for each:
  - `Closes #N` — this commit fully resolves the issue
  - `Refs #N` — relates to but doesn't close (add context in parens, e.g. `Refs #44 (sub-issue resolved)`)
  - `Related: #N` — loose association
- Include parent/epic issues if the project references them

**c) Design documents** — Search for analysis docs related to this work:
- Look in `private/claude/` or equivalent project docs directory for matching files
- Include dev-workflow-process docs, collaboration final assessments, postmortems
- Reference by **filename only** — never include the directory path
- Skip intermediate artifacts (e.g. round 1 questions/responses) — prefer final assessments

### 5. **Write Commit Message to File**
Write the commit message to `./private/claude/commits/` so the user can review and edit it directly before approving. Use a descriptive filename (e.g., `commit_v0.7.16_issue52.txt` or `commit_fix-auth-bug.txt`). Create the `commits/` directory if it doesn't exist.

The message should mirror the conventions found in step 4:
- **Match the project's existing format exactly** — don't impose a different convention
- **NEVER include attribution or credit** (no "Generated with Claude Code" or "Co-Authored-By")
- **NEVER use terms like "comprehensive" unless genuinely warranted** (use descriptive, meaningful terms instead)
- Focus on WHAT was changed and WHY
- Use imperative mood ("Fix bug" not "Fixed bug")
- Keep first line under 72 characters (if possible)
- Issue references use the project's established syntax
- Design doc references listed by filename only under a "Design:" section (if project uses one)
- Test counts updated if the project tracks them in commits

### 5b. **Issue Acceptance Criteria & Comments**
For each issue referenced in the commit message (Closes/Refs), check:
- Read the issue using `gh_issue_full.py N --full` -- ALWAYS `--full` here. (`--compact` skips the body AND comments, which is exactly where acceptance criteria and discussion live; reserve it for timeline-only triage, never for AC checks.)
- Compare acceptance criteria against what was actually implemented
- Determine: should we `Closes` (fully done), `Refs` (progress), or just `Related`?
- **Write a progress comment** to each referenced issue documenting what was done in this commit
  - Save comment drafts to `private/claude/issues/issue_N_YYYY.MM.DD_NN.md`
  - Post via `gh issue comment N --body-file <path>`
  - Include: what was implemented, what remains, relevant design doc references
- This ensures issues always have up-to-date tracking of implementation progress

### 6. **Present for Code Review**
Show the full commit message in the conversation AND provide the file path so the user can edit it directly for precise revisions:
- Code review of all changes
- Commit message displayed inline for quick review
- File path provided for direct editing if the user wants precise wording changes
- Final sign-off approval

### 7. **Commit (After Sign-off)**
Only execute the actual `git commit` after explicit user approval. Use `git commit -F <path-to-commit-msg-file>` to commit with the (possibly user-edited) message file.

### 8. **Sync Private Repo**
If the project has a `private/` nested git repo (check for `private/.git/`), sync it after the parent commit:

```bash
if [ -d "private/.git" ]; then
  cd private && git add -A && git commit -m "sync: match parent commit $(cd .. && git rev-parse --short HEAD)" && cd ..
fi
```

This keeps the private workspace (design docs, postmortems, issue drafts, commit messages) in sync with the parent repo's version history.

**CRITICAL: NEVER push the `private/` nested repo.** It is local-only by design — design docs, issue drafts, commit messages, and other working notes are deliberately kept off the remote. Local commits are sufficient (they version the workspace on disk). Do not run `cd private && git push`, do not suggest it in summaries, and do not include push reminders for the private repo.

### 9. **Push Reminder** (OPTIONAL PUSH — PARENT REPO ONLY)
Remind user that they handle the git push for the **parent repo only** (requires authentication). Do NOT remind them to push the `private/` repo — it is intentionally local-only.

---

**CRITICAL SAFETY RULES:**

- Never commit sensitive configuration files
- Always show full diff before committing
- Wait for explicit user sign-off before final commit
- Never auto-push - user handles authentication
- Follow attribution rules: NO credits in commit messages
- Include version.py updates when version changes

**Example Usage:**
- `/commit` - Interactive commit of all changes
- `/commit file1.py file2.py` - Commit specific files
- `/commit docs/` - Commit all files in docs directory
