---
name: create-project
description: "Full GitHub project creation workflow: repo from template, subtree, hooks, versioning, private init, issues, topics, discussions, traffic tracker, PyPI setup, and first release."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, Agent
---

# Create Project — Full GitHub Repository Setup

End-to-end project creation using DazzleTools git-repokit-template. Covers everything from `gh repo create` through first release.

## User Input

- $ARGUMENTS: `<org/name> "<description>" [--type python|cpp|other] [--topics "t1,t2,..."]`
- Org: `djdarcy` (personal), `DazzleTools` (dev tools), `DazzleNodes` (ComfyUI), `DazzleML` (ML tools)
- If args are missing, prompt for: org, name, description, project type, topics

## Pre-Flight Checks

```bash
# Verify tools are available
gh auth status
ghtraf --version 2>/dev/null || echo "WARN: ghtraf not installed (pip install github-traffic-tracker)"
dz private-init --help 2>/dev/null || echo "WARN: dz private-init not available"
```

---

## Phase 1: Create GitHub Repo from Template

```bash
gh repo create <ORG>/<PROJECT_NAME> \
  --template DazzleTools/git-repokit-template \
  --public \
  --description "<description>"
```

The template's GHA workflow (`setup-from-template.yml`) fires on first push and:
- Derives `$PROJECT_NAME`, `$PACKAGE_NAME`, `$CLI_COMMAND`, `$GITHUB_ORG` from repo metadata
- Runs `find`+`sed` to replace placeholders in all text files
- Creates the Python package directory with `__init__.py` and `__main__.py`
- Self-destructs after running

**Wait ~30 seconds for GHA to complete before proceeding:**
```bash
gh run list --repo <ORG>/<PROJECT_NAME> --limit 3
# Look for "Initialize from template" with status "completed success"
```

## Phase 2: Clone Locally

**If target directory already has code:**
```bash
git clone https://github.com/<ORG>/<PROJECT_NAME>.git /tmp/<project>-template
cp -r /tmp/<project>-template/.git <CODE_ROOT>/<PROJECT_NAME>/
cp -r /tmp/<project>-template/.github <CODE_ROOT>/<PROJECT_NAME>/
cp /tmp/<project>-template/.gitignore <CODE_ROOT>/<PROJECT_NAME>/
cp /tmp/<project>-template/LICENSE <CODE_ROOT>/<PROJECT_NAME>/
cp /tmp/<project>-template/CONTRIBUTING.md <CODE_ROOT>/<PROJECT_NAME>/
cp /tmp/<project>-template/README.md <CODE_ROOT>/<PROJECT_NAME>/
cp /tmp/<project>-template/pyproject.toml <CODE_ROOT>/<PROJECT_NAME>/
cp -r /tmp/<project>-template/tests <CODE_ROOT>/<PROJECT_NAME>/
cp -r /tmp/<project>-template/docs <CODE_ROOT>/<PROJECT_NAME>/
test -f /tmp/<project>-template/.repokit.json && cp /tmp/<project>-template/.repokit.json <CODE_ROOT>/<PROJECT_NAME>/
```

**If starting fresh:**
```bash
git clone https://github.com/<ORG>/<PROJECT_NAME>.git <CODE_ROOT>/<PROJECT_NAME>
```

**Alternative -- init-and-pull (avoids temp dir):**
```bash
cd <CODE_ROOT>/<PROJECT_NAME>
git init
git remote add origin https://github.com/<ORG>/<PROJECT_NAME>.git
git pull origin main
git branch -M main
git branch --set-upstream-to=origin/main main
```

## Phase 3: Add git-repokit-common as Subtree

**IMPORTANT:** Working tree must be clean. Stash or commit changes first.

```bash
cd <CODE_ROOT>/<PROJECT_NAME>
git subtree add --prefix=scripts https://github.com/DazzleTools/git-repokit-common.git main --squash
git remote add repokit-common https://github.com/DazzleTools/git-repokit-common.git
```

## Phase 4: Install Git Hooks

```bash
bash scripts/install-hooks.sh
```

Hooks installed:
- **pre-commit**: Version sync (`sync-versions.py --auto`), private content protection, large file blocking
- **post-commit**: Updates version hash after commit
- **pre-push**: Python syntax check, pytest, debug statement detection

## Phase 5: Fix _version.py

**NOTE:** This was fixed in git-repokit-template v0.1.6, which generates the full `_version.py`. If the template workflow ran successfully, verify with `python -m pytest tests/test_version.py -v`. If tests fail, the fallback fix is to replace with the proper version manually:

Use `src/dazzlecmd/_version.py` in [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) as the reference template. The file must include:
- `MAJOR`, `MINOR`, `PATCH` (int components)
- `PHASE` (str: `""` for stable, `"alpha"`, `"beta"`, `"rc1"`)
- `PROJECT_PHASE` (str: `""`, `"prealpha"`, `"alpha"`, `"beta"`, `"stable"`)
- `__version__` (auto-updated by hooks)
- `__app_name__` (project name)
- `get_version()`, `get_base_version()`, `get_display_version()`, `get_pip_version()` functions
- `VERSION`, `BASE_VERSION`, `PIP_VERSION`, `DISPLAY_VERSION` convenience constants

**Verify:** `python scripts/sync-versions.py --check` and `python -m pytest tests/test_version.py -v`

## Phase 6: Customize Project Files

### pyproject.toml
- Update `description`, `keywords`, `classifiers`
- Set `authors` with real name
- Set `[project.scripts]` entry point (e.g., `my-tool = "my_package.cli:main"`)
- Verify `[tool.repokit-common]` section matches package

### .gitignore
- Add project-specific patterns under `# Project Specific`
- Add `**/bak/` and `**/baks/` if needed

### README.md
- Write proper content with badges, usage, docs
- Platform badge should link to `docs/platform-support.md`
- Create `docs/platform-support.md` with tested/expected platform status table

### CHANGELOG.md
- Create with initial version entry following Keep a Changelog format
- Include `[Unreleased]` and `[0.1.0]` compare links at bottom

### ROADMAP.md
- Create with link to Issue #1
- Summary table of phases and status

## Phase 7: Initialize Private Folder

```bash
# Fresh project (no existing private/ content):
dz private-init <CODE_ROOT>/<PROJECT_NAME>

# Existing content to adopt:
dz private-init --adopt <CODE_ROOT>/<PROJECT_NAME>

# Verify:
dz private-init --status <CODE_ROOT>/<PROJECT_NAME>
```

Creates a nested git repo at `private/` that's invisible to the parent repo. Used for design docs, postmortems, issue drafts, commit message files.

## Phase 8: Configure GitHub Repository

### Enable discussions, sponsorship, and set topics
```bash
gh repo edit <ORG>/<PROJECT_NAME> --enable-discussions
gh repo edit <ORG>/<PROJECT_NAME> --add-topic topic1 --add-topic topic2
```

**Enable Sponsorships (manual):** No API exists for this yet ([GitHub community #179964](https://github.com/orgs/community/discussions/179964)). Remind the user:
> Go to **Settings > General > Features > check "Sponsorships"** to show the Sponsor button.
> FUNDING.yml is already populated by the template workflow, but the feature toggle must be enabled manually.

### Create PyPI environment (if publishing to PyPI)
```bash
echo '{}' | gh api repos/<ORG>/<PROJECT_NAME>/environments/pypi -X PUT --input -
```

Then tell the user to configure PyPI trusted publisher at https://pypi.org/manage/account/publishing/ with:
- **PyPI Project Name:** `<project-name>`
- **Owner:** `<ORG>`
- **Repository name:** `<PROJECT_NAME>`
- **Workflow name:** `release.yml`
- **Environment name:** `pypi`

### Create standard labels
Check existing labels first (`gh label list`), then create missing ones:

```bash
gh label create "pinned" --color "d4c5f9" --description "Permanently open issue" --repo <ORG>/<PROJECT_NAME>
gh label create "evergreen" --color "2ea44f" --description "Never close -- living document updated over time" --repo <ORG>/<PROJECT_NAME>
gh label create "roadmap" --color "0075ca" --description "Project roadmap" --repo <ORG>/<PROJECT_NAME>
gh label create "scratchpad" --color "f9d0c4" --description "Quick notes and scratch space" --repo <ORG>/<PROJECT_NAME>
gh label create "architecture" --color "bfd4f2" --description "Structural decisions" --repo <ORG>/<PROJECT_NAME>
gh label create "epic" --color "5319e7" --description "Large multi-phase initiative" --repo <ORG>/<PROJECT_NAME>
gh label create "ideas" --color "c5def5" --description "Exploratory ideas" --repo <ORG>/<PROJECT_NAME>
gh label create "CurrentTask" --color "0e8a16" --description "Currently being worked on" --repo <ORG>/<PROJECT_NAME>
gh label create "NextTask" --color "e6b800" --description "Next item to pick up" --repo <ORG>/<PROJECT_NAME>
```

**Evergreen issues** are living documents that should never be closed. They're continuously updated as the project evolves. The Roadmap and Quick Notes issues are both evergreen -- they accumulate information over the project's lifetime rather than tracking a task to completion.

### Create Issues #1 and #2

**IMPORTANT:** Check for existing issues first. Create in order to get correct numbering.

Save issue bodies to `private/claude/issues/` and post via `--body-file`:

**Issue #1 -- Roadmap** (labels: `pinned`, `roadmap`, `evergreen`):

- Title: "Roadmap"
- Body: Vision statement, phased roadmap with checkboxes, versions table
- Reference: `djdarcy/github-traffic-tracker#1` for format example

**Issue #2 -- Quick Notes** (labels: `pinned`, `scratchpad`, `evergreen`):

- Title: "Quick Notes -- Bugs, Features, Ideas"
- Body: Sections for Bugs, Features, Ideas/Research, Architecture Notes, Recently Completed
- Reference: `djdarcy/github-traffic-tracker#2` for format example

```bash
gh issue create --title "Roadmap" --label "pinned,roadmap" \
  --body-file private/claude/issues/issue_roadmap.md --repo <ORG>/<PROJECT_NAME>
gh issue create --title "Quick Notes -- Bugs, Features, Ideas" --label "pinned,scratchpad" \
  --body-file private/claude/issues/issue_notes_ideas.md --repo <ORG>/<PROJECT_NAME>
```

### Actually pin the evergreen issues (not just the label)

**The `pinned` LABEL is cosmetic.** GitHub's real "pin" feature (up to 3 issues
shown at the top of the Issues tab) is a separate GraphQL mutation -- there is
NO `gh issue pin` command, so it is easy to forget. Pin both evergreen issues
after creating them. **Resolve numbers by title, not by assuming #1/#2** -- a
Dependabot PR often takes #1, shifting the issues to #2/#3.

```bash
for TITLE in "Roadmap" "Quick Notes"; do
  NUM=$(gh issue list --repo <ORG>/<PROJECT_NAME> --state open --search "$TITLE in:title" \
        --json number,title --jq "map(select(.title|startswith(\"$TITLE\")))[0].number")
  ID=$(gh issue view "$NUM" --repo <ORG>/<PROJECT_NAME> --json id --jq '.id')
  gh api graphql -f query="mutation { pinIssue(input: {issueId: \"$ID\"}) { issue { number } } }"
done
```

Verify both are pinned:
```bash
gh api graphql -f query='{ repository(owner: "<ORG>", name: "<PROJECT_NAME>") { pinnedIssues(first: 5) { nodes { issue { number title } } } } }'
```

## Phase 9: GitHub Traffic Tracker (ghtraf)

**Prerequisites:** `pip install github-traffic-tracker`, `gh` CLI with `gist` scope

### Check for existing gists first (avoid duplicates!)
```bash
gh gist list --limit 30 | grep -i '<PROJECT_NAME>'
```

### Run setup
```bash
cd <CODE_ROOT>/<PROJECT_NAME>
ghtraf create --owner <ORG> --repo <PROJECT_NAME> --repo-dir . \
  --configure --display-name "<Display Name>" --created <YYYY-MM-DD> \
  --ci-workflows --non-interactive
```

**KNOWN BUG:** `--non-interactive` with `--configure` creates gists and sets variables correctly, but if template files don't exist on disk yet, the `--configure` substitution fails silently. Fix:

```bash
# Step 1: Cloud setup (gists + variables)
ghtraf create --owner <ORG> --repo <PROJECT_NAME> --repo-dir . \
  --configure --display-name "<Display Name>" --created <YYYY-MM-DD> \
  --ci-workflows --non-interactive

# Step 2: Copy template files
ghtraf create --owner <ORG> --repo <PROJECT_NAME> --repo-dir . \
  --files-only --force --non-interactive

# Step 3: Manually verify no placeholders remain
grep -c 'PLACEHOLDER\|OWNER/REPO\|USER/GISTID' docs/stats/index.html
# If > 0, manually substitute from .ghtraf.json values
```

### Copy ghtraf dashboard images
```bash
cp <path-to-your-ghtraf-clone>/docs/images/ghtraf-banner.png docs/images/
cp <path-to-your-ghtraf-clone>/docs/images/ghtraf-logo.png docs/images/
cp <path-to-your-ghtraf-clone>/docs/images/ghtraf-icon.png docs/images/
```

### Set PAT secret (user must do interactively)
Tell the user to run:
```bash
gh secret set TRAFFIC_GIST_TOKEN -R <ORG>/<PROJECT_NAME>
```
They can reuse an existing PAT with `gist` scope or create a new one at https://github.com/settings/tokens/new

### Seed history baseline
```bash
python <path-to-your-ghtraf-clone>/scripts/seed_history.py --write
```

### Add Installs badge to README
```markdown
[![Installs](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<USER>/<BADGE_GIST_ID>/raw/installs.json)](https://<USER>.github.io/<PROJECT_NAME>/stats/#installs)
```

## Phase 10: First Commit, Push, and Release

### Commit
**GOTCHA:** The pre-commit hook blocks deletion of `private/` template gitkeep files on public branches. Use `--no-verify` for the first commit only.

```bash
git add <files>  # Stage everything except .vscode/, private/
git rm private/claude/.gitkeep private/claude/commits/commit_v0.1.0_initial-template.txt
git commit --no-verify -m "feat: initial project setup with <description>"
```

### Sync private repo
```bash
cd private && git add -A && git commit -m "sync: initial setup" && cd ..
```

### Push
```bash
git push
```

### Enable GitHub Pages
Tell the user: Settings > Pages > Deploy from branch > `main`, folder `/docs`

### Tag and Release (if ready)
```bash
git tag -a v0.1.0 -m "v0.1.0: <brief description>"
git push origin v0.1.0
gh release create v0.1.0 --title "v0.1.0 - Initial Release" \
  --notes-file private/claude/issues/release_v0.1.0.md
```

The `release.yml` workflow keys off the **GitHub Release published** event
(`on: release: types: [published]`), NOT tag push -- so PyPI publishing fires
on the `gh release create` step above, after the release notes exist, never
ahead of them. **Verify** the instantiated repo's `.github/workflows/release.yml`
actually has the `release: published` trigger before the first ship: older
projects (and any created before git-repokit-template was fixed) carry the
legacy `on: push: tags: ['v*']` trigger, which publishes on tag push and races
the release notes / double-fires on a re-pushed tag. If you see the legacy
trigger, swap it (one-block change; mirror csb's `117eb86`). The root fix lives
in `DazzleTools/git-repokit-template` so new projects inherit it.

**NOTE:** FUNDING.yml sponsor button may not appear until after the first release or GitHub cache refresh. This is normal.

---

## Gotchas & Lessons Learned

1. **_version.py template is incomplete** -- GHA generates minimal version; must replace with full module including all helper functions
2. **pre-commit blocks private/ deletions** -- use `--no-verify` on first commit that removes template gitkeeps
3. **ghtraf --configure fails silently** -- if template files don't exist when cloud setup runs, placeholders aren't substituted
4. **CHANGELOG compare link warning** -- `sync-versions.py --check` warns about missing tag before first release; this is expected
5. **Version bumps** -- every commit should bump at least patch version; don't batch multiple commits at the same version
6. **Private repo sync** -- after every commit to parent, also commit to `private/` nested repo to keep them in sync
7. **Platform badge** -- should link to `docs/platform-support.md`, not the repo root
8. **Issue bodies** -- always write to file first, post via `--body-file` to avoid shell escaping issues
9. **gist scope** -- `gh` CLI needs gist scope for setup; PAT for workflow is separate
10. **GitHub Pages** -- must be enabled manually in repo settings after first push of `docs/`
11. **release.yml trigger** -- must key off `on: release: types: [published]`, NOT `on: push: tags: ['v*']`. Tag-push publishes to PyPI ahead of (or independent of) the GitHub Release notes and double-fires when a tag is re-pushed (spurious "400 File already exists"). The release-published event checks out the release's tag, so the right version still builds. Fixed at root in `DazzleTools/git-repokit-template`; verify the instantiated repo before the first ship and swap if it carries the legacy trigger (mirror csb `117eb86`).

## Reference

- Template: https://github.com/DazzleTools/git-repokit-template
- Common scripts: https://github.com/DazzleTools/git-repokit-common
- Traffic tracker: https://github.com/djdarcy/github-traffic-tracker
- Version file reference: `src/dazzlecmd/_version.py` in [dazzlecmd](https://github.com/DazzleTools/dazzlecmd)
- First project using this skill: `djdarcy/spacehaven-cheat-engine` (2026-04-04)
