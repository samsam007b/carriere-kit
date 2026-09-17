#!/usr/bin/env bash
# PreToolUse(Write|Edit|MultiEdit): refuse to write secrets into files, and refuse
# personal data inside db/ (the shared, public database).
input=$(cat)
HOOK_INPUT="$input" CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}" python3 - <<'PY'
import json, os, re, sys
data = json.loads(os.environ.get("HOOK_INPUT") or "{}")
ti = data.get("tool_input", {})
path = ti.get("file_path", "") or ""
parts = [ti.get("content", ""), ti.get("new_string", "")]
for e in ti.get("edits", []) or []:
    parts.append(e.get("new_string", ""))
text = "\n".join(p for p in parts if isinstance(p, str))

base = os.path.basename(path)
# .env files in workspace/ are the intended place for credentials
if base.startswith(".env") and "/workspace/" in path.replace("\\", "/"):
    sys.exit(0)

SECRETS = [
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "Anthropic API key"),
    (r"sk-[A-Za-z0-9]{32,}", "API key"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{40,}", "GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"AIza[0-9A-Za-z_-]{35}", "Google API key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"(?i)(password|passwd|secret|api_key|apikey|token)\s*[:=]\s*['\"][^'\"\s{}]{8,}['\"]", "hardcoded credential"),
]
for rx, label in SECRETS:
    if re.search(rx, text):
        print(f"Blocked by carriere-kit guard: {label} in {path}. Store it in workspace/.env (ignored by git) and read it from there.", file=sys.stderr)
        sys.exit(2)

norm = path.replace("\\", "/")
if "/db/" in norm and (norm.endswith(".jsonl") or norm.endswith(".json")) and base != "vocab.json":
    print("Blocked by carriere-kit guard: db/ files are written only through `python3 tools/db.py upsert`, which validates and scans for personal data.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
