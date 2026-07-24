---
description: Captures brainstorming ideas and exploration verbatim, creates a local document trail, and optionally mirrors to GitHub as a tracking issue. Use when exploring ideas worth preserving but not yet ready for formal issues.
allowed-tools: Bash, Write, Read, Glob, Grep, Edit, Task, AskUserQuestion
---

# Document Idea — Capture & Mirror

Capturing and documenting ideas from the current conversation...

## Context: "$ARGUMENTS"

## Process

### 1. Gather Context

```bash
TIMESTAMP=$(date +%Y-%m-%d__%H-%M-%S)
```

Determine the working context:
- **Project detection**: Check for `.git`, `CLAUDE.md`, `pyproject.toml`, `package.json`, etc. to identify the current project
- **GitHub repo detection**: Run `gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null` to get the repo if available
- **Existing ideas**: Check `./private/claude/` for prior idea documents to avoid duplication

### 2. Create Local Document

Write a structured document to the project's `private/claude/` directory (or `~/claude/` for cross-project/unclear context).

**Filename format**: `YYYY-MM-DD__HH-MM-SS__idea_(TOPIC).md`

**Document structure**:

```markdown
# Idea: (Short Descriptive Title)

**Date**: YYYY-MM-DD
**Project**: (project name)
**Repository**: (GitHub repo if applicable)
**Status**: Captured (not yet actioned)
**GitHub Mirror**: (link to tracking issue, if created)

---

## Trigger / Context

(What prompted this brainstorm — the situation, problem, or question that led here.
Include the user's COMPLETE VERBATIM words that initiated the discussion.)

## Discussion

(Preserve the conversation flow. What the user said, what Claude analyzed.
Keep the user's words verbatim in blockquotes. Claude's analysis can be
lightly organized but should retain the substance and reasoning.)

> **User**: (exact user message preserved)

**Analysis**: (Claude's response/analysis, organized but faithful to what was said)

## Ideas Catalog

For each idea:

### Idea N: (Title)
- **Category**: (security, feature, UX, performance, integration, infrastructure, etc.)
- **Effort estimate**: (small / medium / large / unknown)
- **Priority hint**: (high-value / nice-to-have / exploratory / deferred)
- **Description**: (what it is, why it matters)
- **Dependencies**: (what it needs, what it builds on)
- **Notes**: (edge cases, alternatives, related prior work)

## Potential Actions

- [ ] Ideas that could become GitHub issues (with draft titles)
- [ ] Ideas that are reference/FYI only
- [ ] Ideas that need more research before deciding
- [ ] Related existing issues to link to

## Summary

(Brief synthesis: how many ideas captured, which seem highest value,
what the natural next steps would be if any are pursued)
```

### 3. GitHub Mirror (Ask User)

After creating the local document, ask the user how (or whether) to mirror to GitHub:

**Options to present:**
- **Tracking issue** (recommended): Single umbrella issue with a checklist of all ideas. Lightweight, easy to manage, ideas can be broken out to individual issues later.
- **Individual issues**: Create separate GitHub issues for each idea. Better when ideas are concrete and actionable.
- **Skip GitHub**: Local document only. Good for early-stage or sensitive brainstorming.

**For tracking issues:**
- Title format: `Ideas: (topic area) — (date)`
- Label suggestions: `enhancement`, `ideas`, `discussion` (create labels if they don't exist)
- Body includes the ideas as a task checklist with descriptions
- Link back to the local document filename (not path) in the issue body
- Footer: `Captured from development session YYYY-MM-DD`

**For individual issues:**
- Create each as a separate issue
- Link them as related to each other
- Consider using a parent/umbrella issue if there are 4+ ideas
- Each issue references the local document filename

### 4. Cross-Reference

After GitHub creation:
- Update the local document with the GitHub issue URL(s)
- If the project tracks ideas elsewhere (wiki, discussions), note that too

## Key Principles

- **Verbatim preservation**: The user's words are captured exactly as written. Do not paraphrase, summarize, or clean up the user's language. Their phrasing carries intent.
- **Claude's analysis preserved too**: Organize lightly for readability but keep the substance and reasoning intact.
- **Ideas are tentative**: This is brainstorming, not commitment. The document and GitHub mirror should clearly convey "these are ideas being explored" not "these are planned features."
- **Low friction**: The default path should be quick — create local doc + single tracking issue. Don't over-engineer the capture step.
- **Forward reference**: Use filenames (not paths) when referencing local documents in GitHub issues, matching the convention in CLAUDE.md.

## File-Based GitHub Comments

When creating GitHub issues with complex markdown, always use `--body-file`:
1. Write the issue body to a temp file first
2. Use `gh issue create --title "..." --body-file /tmp/issue_body.md`
3. This avoids shell escaping issues with backticks, pipes, and special characters

## Usage Examples

```bash
# Document ideas from current conversation
/docidea Future features for wingather - security, window management, platform expansion

# Document a specific brainstorm
/docidea Authentication approaches for the API — OAuth2 vs JWT vs session tokens

# Quick capture of a tangential idea
/docidea Process ancestry tracking — show what launched suspicious windows

# Cross-project idea
/docidea Shared trust list format across wingather and process-delta
```
