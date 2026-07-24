// search-tool-readonly-guard.js
// PreToolUse(Bash) guard: blocks file-rewriting invocations of ast-grep/sg and yq,
// while letting their read-only (search / extract) usage run with no prompt.
//
// Rationale: Claude Code permission globs match a command PREFIX, so they cannot
// fence a write flag that appears as a suffix arg (e.g. `ast-grep -p X -U`). This
// hook parses the full command instead and hard-blocks (exit 2) only the write modes.
//
// Fails OPEN (exit 0) on any internal error so a bug here never blocks all Bash calls.
// ASCII-only output (Windows codepage safety).

let raw = "";
process.stdin.on("data", c => (raw += c));
process.stdin.on("end", () => {
  try {
    const data = JSON.parse(raw || "{}");
    if ((data.tool_name || "") !== "Bash") process.exit(0);
    const cmd = (data.tool_input || {}).command || "";
    if (!cmd) process.exit(0);

    // Drop quoted spans so flags inside a pattern / yq expression don't false-trigger.
    const stripped = cmd.replace(/'[^']*'/g, " ").replace(/"[^"]*"/g, " ");

    // Inspect each command segment (pipes / chains) independently, so another tool's
    // flag (e.g. `grep -i`) in the same line can't be mis-attributed to ast-grep/yq.
    const segments = stripped.split(/\|\||\||&&|;|&/);
    for (const seg of segments) {
      const toks = seg.trim().split(/\s+/).filter(Boolean);
      if (!toks.length) continue;

      // Skip leading `VAR=value` env assignments to find the real command token.
      let i = 0;
      while (i < toks.length && /^[A-Za-z_][A-Za-z0-9_]*=/.test(toks[i])) i++;
      if (i >= toks.length) continue;

      const base = toks[i].replace(/.*[\/\\]/, "").toLowerCase();
      const rest = toks.slice(i + 1);

      if (base === "ast-grep" || base === "ast-grep.exe" || base === "sg" || base === "sg.exe") {
        const write =
          rest[0] === "new" ||                                  // scaffolds rule/config files
          rest.some(t =>
            t === "--update-all" || t === "--interactive" ||
            /^-[A-Za-z]*[Ui][A-Za-z]*$/.test(t));               // short cluster with -U or -i
        if (write) block("ast-grep/sg", seg.trim(), "-U/--update-all, -i/--interactive, or 'new'");
      }

      if (base === "yq" || base === "yq.exe") {
        const write = rest.some(t =>
          t === "--inplace" || /^-[A-Za-z]*i[A-Za-z]*$/.test(t)); // short cluster with lowercase -i
        if (write) block("yq", seg.trim(), "-i/--inplace");
      }
    }
    process.exit(0); // read-only: allow
  } catch (e) {
    process.exit(0); // fail open
  }
});

function block(tool, seg, flags) {
  process.stderr.write(
    "[readonly-guard] Blocked a file-rewriting " + tool + " command (" + flags + ").\n" +
    "Segment: " + seg + "\n" +
    "Per CLAUDE.md, confirm with the user before mutating files. If the rewrite is intended\n" +
    "and the user has approved it, proceed only after that explicit sign-off.\n");
  process.exit(2);
}
