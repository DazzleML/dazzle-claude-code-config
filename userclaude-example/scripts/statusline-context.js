#!/usr/bin/env node
/*
 * statusline-context.js -- custom Claude Code status line with an EARLY
 * context-usage warning.
 *
 * Why this exists: Claude Code's built-in "X% context used" element only
 * appears within a fixed ~33k-token buffer of the limit. On a 1M-token
 * window that is ~97% used, which feels too late. This status line shows
 * the context percentage at all times and escalates to a loud warning at
 * WARN_AT so you get a heads-up at ~94-95%.
 *
 * Claude Code pipes a JSON blob to this script on stdin (see
 * tools/AgentTool/built-in/statuslineSetup.ts). The field we care about is
 * context_window.used_percentage (pre-calculated, 0-100, or null before the
 * first API response).
 *
 * Wired up via ~/.claude/settings.json:
 *   "statusLine": { "type": "command",
 *     "command": "\"C:\\Program Files\\nodejs\\node.exe\" \"%USERPROFILE%\\claude\\scripts\\statusline-context.js\"" }
 *
 * ASCII-only output by design (no em dashes / smart quotes / arrows) to stay
 * safe across Windows codepages. ANSI color escapes are fine -- they are
 * control sequences, not codepage-dependent characters.
 */

'use strict';

// ---- Tunable thresholds (percent of context window used) -------------------
const CAUTION_AT = 85; // yellow: getting full
const WARN_AT = 94; // bold red: wrap up / compact soon  <-- the "popup" the user wanted
// ----------------------------------------------------------------------------

// ANSI styling. Claude Code renders the status line already dimmed; these add color on top.
const RESET = '\x1b[0m';
const DIM = '\x1b[2m';
const CYAN = '\x1b[36m';
const YELLOW = '\x1b[33m';
const RED_BOLD = '\x1b[1;31m';

function readStdin() {
  return new Promise((resolve) => {
    let buf = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (c) => (buf += c));
    process.stdin.on('end', () => resolve(buf));
    // If nothing is piped, do not hang.
    process.stdin.on('error', () => resolve(buf));
  });
}

function shortenCwd(p) {
  if (!p) return '';
  let s = String(p).replace(/\\/g, '/');
  const home = (process.env.USERPROFILE || process.env.HOME || '').replace(/\\/g, '/');
  if (home && s.toLowerCase().startsWith(home.toLowerCase())) {
    s = '~' + s.slice(home.length);
  }
  // Keep it short: show at most the last 3 path segments.
  const parts = s.split('/').filter(Boolean);
  if (parts.length > 3) {
    const tail = parts.slice(-3).join('/');
    return (s.startsWith('~') ? '~/.../' : '.../') + tail;
  }
  return s;
}

function ctxSegment(usedPct) {
  if (usedPct === null || usedPct === undefined || Number.isNaN(usedPct)) {
    return `${DIM}ctx --%${RESET}`;
  }
  const n = Math.round(usedPct);
  if (n >= WARN_AT) {
    return `${RED_BOLD}[!] CTX ${n}% LOW -- wrap up or /compact${RESET}`;
  }
  if (n >= CAUTION_AT) {
    return `${YELLOW}ctx ${n}%${RESET}`;
  }
  return `${CYAN}ctx ${n}%${RESET}`;
}

(async () => {
  const raw = await readStdin();
  let data = {};
  try {
    data = JSON.parse(raw);
  } catch (_) {
    // Never break the UI: emit a minimal line and exit cleanly.
    process.stdout.write('ctx --%');
    return;
  }

  const model =
    (data.model && (data.model.display_name || data.model.id)) || 'claude';
  const cwd = shortenCwd(
    (data.workspace && data.workspace.current_dir) || data.cwd
  );
  const cw = data.context_window || {};
  const usedPct =
    cw.used_percentage !== undefined && cw.used_percentage !== null
      ? Number(cw.used_percentage)
      : null;

  const segments = [`${DIM}${model}${RESET}`];
  if (cwd) segments.push(`${DIM}${cwd}${RESET}`);
  segments.push(ctxSegment(usedPct));

  process.stdout.write(segments.join(`${DIM} | ${RESET}`));
})();
