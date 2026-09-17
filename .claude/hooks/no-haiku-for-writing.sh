#!/usr/bin/env bash
# PreToolUse(Agent|Task): Haiku is for research and reading only.
# Blocks a Haiku subagent unless it is one of the read-only research agents.
input=$(cat)
HOOK_INPUT="$input" CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}" python3 - <<'PY'
import json, os, re, sys
ti = json.loads(os.environ.get("HOOK_INPUT") or "{}").get("tool_input", {})
agent = (ti.get("subagent_type") or "").strip()
READ_ONLY = {"researcher", "doc-reader", "Explore", "claude-code-guide"}
model = (ti.get("model") or "").lower()

if not model and agent:
    f = os.path.join(os.environ["CLAUDE_PROJECT_DIR"], ".claude", "agents", agent + ".md")
    if os.path.exists(f):
        m = re.search(r"^model:\s*(\S+)", open(f, encoding="utf-8").read(), re.M)
        model = (m.group(1) if m else "").lower()

if "haiku" in model and agent not in READ_ONLY:
    print("Blocked by carriere-kit guard: Haiku is reserved for research and reading "
          "(researcher, doc-reader). Use Sonnet for anything that writes code or documents.",
          file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
