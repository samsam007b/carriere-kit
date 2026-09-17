#!/usr/bin/env python3
"""Create or check the private workspace/ folder.

  python3 tools/init.py            create workspace/ from templates/ (never overwrites a file)
  python3 tools/init.py --status   print the workspace state as JSON (used by the SessionStart hook)

workspace/ is ignored by git. It holds everything personal: profile, facts, tracker,
applications, config. Safe to run again at any time.
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WS = os.path.join(ROOT, "workspace")
TPL = os.path.join(ROOT, "templates")

FILES = ["profile.md", "facts.md", "tracker.md", "tracker-archive.md", "calendar.md",
         "vision.md", "positioning.md", "storytelling.md", "keywords.md"]

DEFAULT_CONFIG = {
    "language": None,
    "auto_contribute": True,
    "github_user": None,
    "private_terms": [],
    "onboarded_on": None,
}

PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")


def create():
    os.makedirs(os.path.join(WS, "applications"), exist_ok=True)
    os.makedirs(os.path.join(WS, ".logs"), exist_ok=True)
    made = []
    for name in FILES:
        src, dst = os.path.join(TPL, name), os.path.join(WS, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copyfile(src, dst)
            made.append(name)
    cfg = os.path.join(WS, "config.json")
    if not os.path.exists(cfg):
        with open(cfg, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        made.append("config.json")
    print(f"workspace ready at {os.path.relpath(WS, os.getcwd())}")
    for m in made:
        print(f"  created {m}")
    if not made:
        print("  nothing to create, all files already exist")
    return 0


def status():
    # tools may create workspace/.logs on their own: the workspace exists once init ran
    state = {"workspace": os.path.isfile(os.path.join(WS, "config.json")), "profile_filled": False, "placeholders_left": None,
             "config": None, "applications": 0}
    prof = os.path.join(WS, "profile.md")
    if os.path.exists(prof):
        text = open(prof, encoding="utf-8").read()
        left = len(PLACEHOLDER.findall(text))
        state["placeholders_left"] = left
        # a profile counts as filled once most placeholders are gone
        total = len(PLACEHOLDER.findall(open(os.path.join(TPL, "profile.md"), encoding="utf-8").read())) if os.path.exists(os.path.join(TPL, "profile.md")) else 0
        state["profile_filled"] = total == 0 and left == 0 or (total > 0 and left <= total * 0.3)
    cfg = os.path.join(WS, "config.json")
    if os.path.exists(cfg):
        try:
            state["config"] = json.load(open(cfg, encoding="utf-8"))
        except Exception:
            state["config"] = "invalid JSON"
    apps = os.path.join(WS, "applications")
    if os.path.isdir(apps):
        state["applications"] = len([d for d in os.listdir(apps) if os.path.isdir(os.path.join(apps, d))])
    print(json.dumps(state))
    return 0


if __name__ == "__main__":
    sys.exit(status() if "--status" in sys.argv else create())
