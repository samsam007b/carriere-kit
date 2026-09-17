#!/usr/bin/env python3
"""Record the user's explicit "yes, send" for one final send in the current turn.

  python3 tools/approve_send.py "Application to <company> via its careers portal"

Run it ONLY right after the user approved in their latest message. The approval is erased
as soon as the user sends another message (UserPromptSubmit hook) and expires after
15 minutes. Every approval is appended to workspace/.logs/sends.log.
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(ROOT, "workspace", ".logs")

if len(sys.argv) < 2 or not sys.argv[1].strip():
    sys.exit("usage: approve_send.py \"<what is being sent, to whom>\"")
os.makedirs(LOGS, exist_ok=True)
now = datetime.datetime.now().isoformat(timespec="seconds")
json.dump({"approved_at": now, "what": sys.argv[1]}, open(os.path.join(LOGS, "send-approved.json"), "w"))
with open(os.path.join(LOGS, "sends.log"), "a", encoding="utf-8") as f:
    f.write(f"{now}\t{sys.argv[1]}\n")
print("send approved for this turn")
