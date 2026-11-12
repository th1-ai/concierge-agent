#!/usr/bin/env python3
"""PreToolUse guard for the concierge agent.

Reads the hook input (JSON on stdin) and the one `Level: <value>` line in
AUTONOMY.md. The value is 0, 1, 2, 3 or PAUSED. A missing file, a missing
line, more than one line or an unknown value counts as PAUSED.

It blocks a Bash command (exit code 2, reason on stderr) in three cases:

1. PAUSED. Every Bash command is blocked, in every session.
2. Level 0 in a scheduled run (the scheduler sets CONCIERGE_SCHEDULED=1).
   Every Bash command is blocked.
3. Send guard. The command looks like an email send and the level is below 3.

Everything else exits 0 with no output, so the normal permission rules decide.

This is a backstop, not a security boundary: it matches the command text.
Edit SEND_PATTERNS so they match the send syntax of your own email tool.
"""
import json
import os
import re
import sys

# Regular expressions that mark a command as "sends an email".
# They are tested against the command with quoted text removed, so a draft
# whose body contains the word "send" is not blocked.
SEND_PATTERNS = [
    r"(?<![\w])send(?![\w])",   # send, --send, send-draft, drafts send, messages.send
    r"(?<![\w])sendmail(?![\w])",
    r"(?<![\w])deliver(?![\w])",
]


def block(reason):
    print("autonomy-guard: " + reason, file=sys.stderr)
    sys.exit(2)


def read_autonomy(project_dir):
    """Return (level, reason). level is 0-3 or "PAUSED"; reason explains a PAUSED."""
    path = os.path.join(project_dir, "AUTONOMY.md")
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return "PAUSED", "AUTONOMY.md is missing or cannot be read, which counts as PAUSED"
    values = [m.group(1).strip() for m in (re.match(r"\s*Level:(.*)$", l) for l in lines) if m]
    if len(values) != 1:
        return "PAUSED", "AUTONOMY.md has %d 'Level:' lines instead of one, which counts as PAUSED" % len(values)
    if values[0] in ("0", "1", "2", "3"):
        return int(values[0]), ""
    if values[0] == "PAUSED":
        return "PAUSED", "AUTONOMY.md says Level: PAUSED"
    return "PAUSED", "AUTONOMY.md has an unknown level value, which counts as PAUSED"


def strip_quoted(command):
    command = re.sub(r"'[^']*'", "''", command)
    command = re.sub(r'"(?:\\.|[^"\\])*"', '""', command)
    return command


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        block("could not read the hook input, so the command is blocked.")
    if not isinstance(data, dict) or data.get("tool_name") != "Bash":
        sys.exit(0)
    command = (data.get("tool_input") or {}).get("command") or ""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
    level, reason = read_autonomy(project_dir)

    if level == "PAUSED":
        block(reason + ". Nothing runs. Record the reason in runs/LOG.md and stop.")
    if level == 0 and os.environ.get("CONCIERGE_SCHEDULED") == "1":
        block("AUTONOMY.md says Level: 0. The agent runs only when the operator asks.")

    bare = strip_quoted(command)
    if level < 3 and any(re.search(p, bare, re.IGNORECASE) for p in SEND_PATTERNS):
        block("this looks like a send command and AUTONOMY.md says Level: %d. Sending needs Level 3. Create a draft instead." % level)
    sys.exit(0)


if __name__ == "__main__":
    main()
