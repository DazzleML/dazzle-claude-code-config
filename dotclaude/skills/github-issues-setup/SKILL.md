---
name: github-issues-setup
description: "Initialize standard GitHub issues (#1 Roadmap, #2 Quick Notes) with the canonical label set for a new project."
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch
---

# GitHub Issues Setup -- Standard Project Initialization

Sets up the standard evergreen issues + labels for a DazzleTools/djdarcy project.

**Canonical convention:** this skill is the single source of truth for standalone
issue setup and mirrors `create-project` Phase 8 -- keep the two in sync. It
supersedes the retired `setup-github-project` command (consolidated 2026-06-19).

## What This Does

1. Creates the standard label set (`pinned`, `evergreen`, `roadmap`, `scratchpad`,
   `architecture`, `epic`, `ideas`, `CurrentTask`, `NextTask`)
2. Creates Issue #1: **Roadmap** (evergreen, never closes)
3. Creates Issue #2: **Quick Notes -- Bugs, Features, Ideas** (evergreen, never closes)
4. Stores issue body files in `private/claude/issues/` for future reference

## Prerequisites

- `gh` CLI authenticated
- A GitHub repo already exists for the project
- Working directory is the project root (with `.git/`)

## Process

### Step 1: Create Labels

Check existing labels first (`gh label list`) to avoid duplicates, then:

```bash
gh label create "pinned"       --color "d4c5f9" --description "Permanently open issue"
gh label create "evergreen"    --color "2ea44f" --description "Never close -- living document updated over time"
gh label create "roadmap"      --color "0075ca" --description "Project roadmap"
gh label create "scratchpad"   --color "f9d0c4" --description "Quick notes and scratch space"
gh label create "architecture" --color "bfd4f2" --description "Structural decisions"
gh label create "epic"         --color "5319e7" --description "Large multi-phase initiative"
gh label create "ideas"        --color "c5def5" --description "Exploratory ideas"
gh label create "CurrentTask"  --color "0e8a16" --description "Currently being worked on"
gh label create "NextTask"     --color "e6b800" --description "Next item to pick up"
```

### Step 2: Draft Issue Bodies

**Do NOT hard-wrap the body prose.** Issue bodies render on GitHub and reflow on
their own — write one line per paragraph. Hard-wrapping at ~80 cols makes the issue
painful to edit and can mis-render in lists. (Fix after the fact with `dz md-unwrap -i`.)

Create `private/claude/issues/` directory. Draft two files:

**`issue_roadmap.md`** structure:
```markdown
## Roadmap

Evergreen tracking issue for [ProjectName] development priorities.

### Phase 1: Foundation
- [x] Completed items
- [ ] Pending items (#N)

### Phase 2: Core Features
- [ ] Items...

### Phase 3: Refactor / Modernization
- [ ] Items...

### Phase 4: Advanced / Future
- [ ] Items...
```

**`issue_notes_ideas.md`** structure:
```markdown
## Quick Notes -- Bugs, Features, Ideas

Evergreen scratch space for [ProjectName]: small bugs, feature seeds, and ideas
that don't warrant their own issue yet. Items get promoted to proper issues when
they mature.

### Bugs
- (none yet)

### Features
- Bullet feature seeds...

### Ideas / Research
- Exploratory ideas...

### Architecture Notes
- Decisions, gotchas, observations...

### Recently Completed
- (rolling log)
```

Customize the content for the specific project. The phase structure and section
headings are flexible -- adapt to the project's actual scope.

### Step 3: Create Issues

**CRITICAL**: Issues must be #1 and #2. If the repo already has issues, coordinate
first (`gh issue list --state all --limit 5`).

```bash
gh issue create --title "Roadmap" --label "pinned,roadmap,evergreen" \
  --body-file private/claude/issues/issue_roadmap.md

gh issue create --title "Quick Notes -- Bugs, Features, Ideas" --label "pinned,scratchpad,evergreen" \
  --body-file private/claude/issues/issue_notes_ideas.md
```

### Step 4: Actually pin the issues (not just the label)

**The `pinned` LABEL is cosmetic** -- GitHub's real "pin" feature (up to 3 issues
at the top of the Issues tab) is a separate GraphQL mutation with no `gh issue
pin` command, so it is easy to forget. Pin both evergreen issues. **Resolve
numbers by title, not by assuming #1/#2** -- a Dependabot PR often takes #1,
shifting the issues to #2/#3.

```bash
for TITLE in "Roadmap" "Quick Notes"; do
  NUM=$(gh issue list --state open --search "$TITLE in:title" \
        --json number,title --jq "map(select(.title|startswith(\"$TITLE\")))[0].number")
  ID=$(gh issue view "$NUM" --json id --jq '.id')
  gh api graphql -f query="mutation { pinIssue(input: {issueId: \"$ID\"}) { issue { number } } }"
done
```

### Step 5: Verify

```bash
gh issue list --label pinned
gh api graphql -f query='{ repository(owner: "OWNER", name: "REPO") { pinnedIssues(first: 5) { nodes { issue { number title } } } } }'
```

Both issues should show as OPEN with the `pinned` label AND appear in
`pinnedIssues` (actually pinned on the repo).

## User Input Required

- $ARGUMENTS: Optional project description or context to customize the roadmap
  phases and notes content. If empty, ask the user what the project is about and
  what work has been done / is planned.

## Reference

- **Canonical convention:** mirrors `create-project` Phase 8; keep them in sync.
- Format examples: `djdarcy/github-traffic-tracker#1` (Roadmap), `#2` (Quick Notes)
- The `pinned` (#d4c5f9) + `evergreen` (#2ea44f) labels mark living issues that never close
- Issue body files stored at `private/claude/issues/` (gitignored via repokit)
- Supersedes the retired `setup-github-project` command (consolidated 2026-06-19)
