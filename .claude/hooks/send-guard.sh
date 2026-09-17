#!/usr/bin/env bash
# Final-send guard.
#   UserPromptSubmit : clears any previous approval, so an approval only lives inside the
#                      turn where the user said yes.
#   PreToolUse       : blocks browser actions that look like a final send (email, application
#                      portal, form, post) unless the approval flag was set in this turn with
#                      `python3 tools/approve_send.py "<what is being sent>"`.
input=$(cat)
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
HOOK_INPUT="$input" python3 - <<'PY'
import json, os, re, sys, time
data = json.loads(os.environ.get("HOOK_INPUT") or "{}")
flag = os.path.join("workspace", ".logs", "send-approved.json")

if data.get("hook_event_name") == "UserPromptSubmit":
    if os.path.exists(flag):
        os.remove(flag)
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input", {}) or {}
SEND = re.compile(
    r"\b(send|submit|apply|post|publish|confirm( and)? (send|submit|apply)|finish application|complete application|"
    r"envoyer|soumettre|postuler|publier|valider (et envoyer|ma candidature)|"
    r"verzenden|versturen|verstuur|indienen|solliciteer|solliciteren|"
    r"senden|absenden|bewerben|enviar|inviare|candidati)\b", re.I)

risky = False
if tool.endswith("browser_click"):
    risky = bool(SEND.search(str(ti.get("element", ""))))
elif tool.endswith("browser_press_key"):
    risky = str(ti.get("key", "")).lower() in ("control+enter", "meta+enter", "ctrl+enter", "cmd+enter")
elif tool.endswith("browser_fill_form"):
    risky = bool(ti.get("submit"))
elif tool.endswith(("browser_evaluate", "browser_run_code_unsafe", "browser_run_code")):
    code = str(ti.get("function", "")) + str(ti.get("code", ""))
    risky = bool(re.search(r"\.submit\(|requestSubmit\(", code)) or bool(SEND.search(code) and "click" in code)
elif tool.endswith("browser_type"):
    risky = bool(ti.get("submit")) and bool(SEND.search(str(ti.get("element", ""))))

NOT_SEND = re.compile(r"filter|search|sort|cookie|accept all|preferences|job post|see post|view post", re.I)
if risky and NOT_SEND.search(str(ti.get("element", ""))):
    risky = False
if not risky:
    sys.exit(0)

if os.path.exists(flag) and time.time() - os.path.getmtime(flag) < 900:
    sys.exit(0)

print("Blocked by carriere-kit send guard: this looks like a final send (email, application, form, post). "
      "Show the user exactly what will be sent (full text, recipient or portal, attachments) and ask "
      "for an explicit yes. Only after the user says yes in their new message, run "
      "`python3 tools/approve_send.py \"<what is sent>\"` and retry. Never set the approval without that yes.",
      file=sys.stderr)
sys.exit(2)
PY
