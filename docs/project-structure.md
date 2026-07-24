# How projects are structured

The skills in this collection assume a specific, repeatable project shape. This page makes it explicit so the tools make sense — and so you can adopt the shape (or map the conventions onto your own).

## The skeleton

```
my-project/
├── src/<package>/          # or the content itself, for non-code repos
├── tests/
│   ├── checklists/         # human test checklists (see /test-checklist) + results/
│   └── one-offs/           # quick diagnostic scripts -- kept, not deleted (they graduate
│                           #   to tests/ or scripts/ if they prove valuable)
├── docs/
├── scripts/                # shared dev tooling, consumed as a git subtree of
│                           #   github.com/DazzleTools/git-repokit-common
│                           #   (hooks, version sync, gh_issue_full.py, ...)
├── private/                # the project vault -- see below
├── CHANGELOG.md            # keep-a-changelog; VERSION file or _version.py
└── README.md
```

## The `private/` vault

Every project carries a `private/` directory that is **gitignored by the parent repo** and initialized as its **own standalone git repository** (the `dz private-init` tool from [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) does this in one command — the nested repo is invisible to the parent, versioned independently, and deliberately local-only, never pushed).

```
private/claude/
├── YYYY-MM-DD__HH-MM-SS__dev-workflow-process__<topic>.md   # design analyses
├── YYYY-MM-DD__HH-MM-SS__full-postmortem_<topic>.md         # what actually happened
├── YYYY-MM-DD__HH-MM-SS__claude-plan__<topic>.md            # approved plan snapshots
├── issues/          # issue/comment drafts (posted via --body-file), kept for the record
├── commits/         # commit-message files reviewed before committing
└── notes/           # the Obsidian-style knowledge vault /obsidian writes into
```

Why this matters to the skills: `/dev-workflow-process` and the postmortem family **write** here; `/wherearewe`, `/familiarize`, and the `oracle` agent **read** here. The vault is the project's memory — the timestamped filenames mean a bare `ls` shows the project's decision history in order. Sync the nested repo after meaningful parent commits (`cd private && git add -A && git commit`).

## Where projects come from — the graduation path

Not everything deserves a repo on day one. Work graduates through stages as it proves value:

1. **One-off script** — starts life in some project's `tests/one-offs/` (a quick check, a diagnostic)
2. **Reusable script** — proves useful twice → moves to `scripts/`
3. **`dz` tool** — proves generally useful → becomes a tool inside [dazzlecmd](https://github.com/DazzleTools/dazzlecmd) (`dz new tool <name>` scaffolds the manifest + entry; the tool lives at `projects/<namespace>/<tool>/` and is invoked as `dz <tool>`). Most utilities live their whole lives here — one command surface, no repo overhead.
4. **Standalone project** — grows real scope (its own tests, docs, releases, users) → graduates to its own GitHub repo via the creation process below, and is optionally folded *back* into dazzlecmd as a git submodule so `dz` keeps serving it ("dz all the way down").

The rule of thumb: **dazzlecmd first; a repo only when the thing is bigger than a tool.**

## How work is tracked

- Every repo carries two **evergreen issues**, pinned for real: `#Roadmap` (the phased plan, checkboxes ticked as phases ship, progress comments per milestone) and `#Quick Notes` (a living scratchpad for bugs/ideas/follow-ups — never closed)
- Two labels manage session continuity: **`CurrentTask`** (the one issue actively being worked — at most one per repo) and **`NextTask`** (queued next — promoted to CurrentTask when work starts)
- Issues reference their design documents **by filename only** (e.g. `2026-07-24__12-13-13__dev-workflow-process__<topic>.md`) — the file lives in the maintainers' `private/` vault, so the reference tells a future session exactly what to look for without leaking the vault's layout
- Comments and issue bodies are drafted as files (`private/claude/issues/`) and posted via `--body-file` — shell-escaping never mangles a report, and the draft is kept for the record

## The repeatable creation process

New projects follow one process (encoded in the `/create-project` skill, publishing in a later wave):

1. Create the repo from a template ([git-repokit-template](https://github.com/DazzleTools/git-repokit-template)) — its init workflow substitutes project names and scaffolds the package
2. Add [git-repokit-common](https://github.com/DazzleTools/git-repokit-common) as the `scripts/` subtree; install its git hooks (version sync, private-content protection, pre-push checks)
3. Verify the version module; customize `pyproject.toml`, README, CHANGELOG
4. `dz private-init` the vault
5. Create the standard label set plus two **evergreen issues** — `#Roadmap` (pinned, phased checkboxes) and `#Quick Notes` (pinned scratchpad for bugs/ideas) — and pin them via the real GitHub pin (a GraphQL mutation, not just a label)
6. Optionally wire traffic/install tracking ([github-traffic-tracker](https://github.com/djdarcy/github-traffic-tracker))
7. First commit → annotated tag → GitHub release

A note on tooling honesty: this process is also mechanized by the standalone [repokit](https://github.com/DazzleTools/git-repokit) tool, and the two are **partially out of sync** — the skill encodes the current canonical process; the tool is being caught up to it. If you adopt one, adopt the skill's process.

## How it connects to the workflow

See [workflow.md](workflow.md): the vault documents written at Reflect are the inputs read at Orient. The issues from step 5 are the tracking surface for `/github-issue` and `/github-acceptance-check`; the checklists directory is where `/test-checklist` output lives; the `scripts/` subtree supplies the helpers several commands call.
