#!/usr/bin/env bash
# PreToolUse(Bash): block destructive or risky shell commands.
# The project runs in bypass-permissions mode; this hook is part of the safety net.
# Exit 2 = block, the reason on stderr is shown to Claude.
input=$(cat)
cmd=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)
[ -z "$cmd" ] && exit 0

block() { echo "Blocked by carriere-kit guard: $1. Explain to the user instead of working around it." >&2; exit 2; }

# Normalise whitespace for matching
c=$(printf '%s' "$cmd" | tr '\n' ' ' | tr -s ' ')

case "$c" in
  *"sudo "*) block "sudo is not allowed" ;;
esac

echo "$c" | grep -Eq '(^|[;&|] *)rm +(-[a-zA-Z]*[rR][a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*[rR])[a-zA-Z]* +(/|~|\$HOME|\.|\*|\.\.)( |$|/ *$)' \
  && block "recursive forced delete of a root, home or whole-folder path"
echo "$c" | grep -Eq 'rm +-[a-zA-Z]*[rR][a-zA-Z]* .*(workspace|db)(/)?( |$)' \
  && block "deleting workspace/ or db/ wholesale"
echo "$c" | grep -Eq 'git +push .*(--force|-f( |$)|--force-with-lease)' \
  && block "force push"
echo "$c" | grep -Eq 'git +push .*(origin|upstream) +(main|master)( |$)' \
  && block "direct push to main: database changes go through tools/contribute.py pull requests"
echo "$c" | grep -Eq 'git +(reset +--hard|clean +-[a-zA-Z]*f|checkout +-- +\.|restore +\.)' \
  && block "command that discards local work"
echo "$c" | grep -Eq 'git +add .*(workspace|\.env)' \
  && block "staging private files (workspace/ or .env)"
echo "$c" | grep -Eq '(curl|wget)[^|]*\| *(ba|z)?sh' \
  && block "piping a download into a shell"
echo "$c" | grep -Eq '(mkfs|dd +if=|:\(\)\{|chmod +-R +777 +/)' \
  && block "system-level destructive command"
echo "$c" | grep -Eq '(cat|less|head|tail|cp|scp|curl).*(\.env|id_rsa|id_ed25519|\.aws/credentials)' \
  && block "reading or moving credentials"
echo "$c" | grep -Eq 'gh +repo +(delete|edit .*--visibility)' \
  && block "deleting a repository or changing its visibility"

exit 0
