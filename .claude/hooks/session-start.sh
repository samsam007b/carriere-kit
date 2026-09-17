#!/usr/bin/env bash
# SessionStart: pull the shared database, then brief Claude on the workspace state.
# Everything printed here lands in Claude's context. Keep it short.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

echo "## carriere-kit session briefing"

# sync.py enforces its own network timeout (macOS has no `timeout` binary by default)
sync_out=$(python3 tools/sync.py --quiet 2>&1)
[ -n "$sync_out" ] && echo "$sync_out"

state=$(python3 tools/init.py --status 2>/dev/null)
echo "workspace state: $state"

case "$state" in
  *'"workspace": false'*)
    echo "FIRST RUN: no workspace/ yet. Run the \`start\` skill: explain the kit in at most 8 lines, offer the menu, then create the workspace with \`python3 tools/init.py\` once the user agrees."
    ;;
  *'"profile_filled": false'*)
    echo "PROFILE NOT FILLED: run the \`start\` skill, then propose the \`profile\` interview."
    ;;
  *)
    if [ -f tools/tracker.py ] && [ -f workspace/tracker.md ]; then
      fu=$(python3 tools/tracker.py followups --summary 2>/dev/null || python3 tools/tracker.py followups 2>/dev/null | head -15)
      [ -n "$fu" ] && { echo "follow-ups:"; echo "$fu"; }
    fi
    ;;
esac

if [ -f db/vocab.json ]; then
  python3 tools/db.py stats 2>/dev/null | head -6
fi
exit 0
