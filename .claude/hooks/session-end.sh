#!/usr/bin/env bash
# SessionEnd: if db/ changed, open or update a pull request to the main repo.
# SessionEnd hooks have a very short budget, so the work runs detached in the background.
# Opt out: "auto_contribute": false in workspace/config.json.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f tools/contribute.py ] || exit 0
mkdir -p workspace/.logs
nohup python3 tools/contribute.py --auto >> workspace/.logs/contribute.log 2>&1 < /dev/null &
disown 2>/dev/null
exit 0
