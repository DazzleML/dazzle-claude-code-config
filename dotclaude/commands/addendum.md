# Addendum Command

Append a verbatim user note to the most recent dev-workflow-process document or postmortem.

## Usage

```
/addendum <text to append>
```

## Instructions

1. **Find the most recent design doc or postmortem** in one of these locations (check in order):
   - Current project's `./private/claude/` folder
   - `~/claude/`
   - User's `~/.claude/` directory

2. **Identify the file** by:
   - Most recent file matching pattern: `YYYY-MM-DD__HH-MM-SS__*.md`
   - Or most recent file containing "postmortem" or "dev-workflow" in the name
   - Prefer files modified in the current session

3. **Append the addendum** to the end of the file:

```markdown

---

## Addendum: User Note (YYYY-MM-DD HH:MM)

> [User's verbatim text here, preserved exactly as written]

### Implications

[If appropriate, add brief analysis of what this note means for the design/implementation]
```

4. **Confirm to the user**:
   - Which file was updated
   - Preview of what was added

## Example

User: `/addendum We should also consider rate limiting on the API calls`

Result appended to `2026-01-29__14-46-10__api-design.md`:

```markdown

---

## Addendum: User Note (2026-01-29 15:30)

> We should also consider rate limiting on the API calls

### Implications

- Add rate limiting consideration to API design
- May need configuration options for rate limits
```

## Notes

- Always preserve the user's text **verbatim** in a blockquote
- The "Implications" section is optional - only add if there are clear follow-up considerations
- If no recent design doc is found, ask the user which file to append to
- If the addendum relates to a GitHub issue, offer to add it as a comment there too
