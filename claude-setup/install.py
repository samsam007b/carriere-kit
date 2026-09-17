#!/usr/bin/env python3
"""Optional machine-wide Claude Code setup. Everything the kit needs already works inside
the repo; this only makes the same habits apply in every folder.

  python3 claude-setup/install.py                 show the plan, change nothing
  python3 claude-setup/install.py --apply all     apply every item
  python3 claude-setup/install.py --apply models,rules

Items:
  models   ~/.claude/settings.json: "model": "opusplan", env CLAUDE_CODE_SUBAGENT_MODEL=sonnet
  bypass   ~/.claude/settings.json: permissions.defaultMode = "bypassPermissions"
           (needed on some setups for the repo's bypass mode to take effect everywhere;
           the repo hooks still block dangerous actions, other folders have no such hooks)
  rules    append claude-setup/rules.md to ~/.claude/CLAUDE.md (idempotent, marked block)

A timestamped backup of every file is written before any change.
"""
import datetime, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.join(os.path.expanduser("~"), ".claude")
SETTINGS = os.path.join(HOME, "settings.json")
CLAUDE_MD = os.path.join(HOME, "CLAUDE.md")
ITEMS = ["models", "bypass", "rules"]


def backup(path):
    if os.path.exists(path):
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copyfile(path, f"{path}.bak-{stamp}")


def load_settings():
    try:
        return json.load(open(SETTINGS, encoding="utf-8"))
    except FileNotFoundError:
        return {}


def plan(settings):
    out = []
    if settings.get("model") != "opusplan" or settings.get("env", {}).get("CLAUDE_CODE_SUBAGENT_MODEL") != "sonnet":
        out.append(("models", f"model: {settings.get('model')} -> opusplan, subagent model -> sonnet"))
    if settings.get("permissions", {}).get("defaultMode") != "bypassPermissions":
        out.append(("bypass", f"defaultMode: {settings.get('permissions', {}).get('defaultMode')} -> bypassPermissions"))
    text = open(CLAUDE_MD, encoding="utf-8").read() if os.path.exists(CLAUDE_MD) else ""
    if "carriere-kit:rules:start" not in text:
        out.append(("rules", f"append working rules to {CLAUDE_MD}"))
    return out


def main():
    settings = load_settings()
    todo = plan(settings)
    if "--apply" not in sys.argv:
        if not todo:
            print("Everything is already set up.")
        for item, desc in todo:
            print(f"  {item:7} {desc}")
        print("\nNothing changed. Apply with: python3 claude-setup/install.py --apply all  (or a list: models,rules)")
        return 0

    arg = sys.argv[sys.argv.index("--apply") + 1] if len(sys.argv) > sys.argv.index("--apply") + 1 else ""
    chosen = ITEMS if arg == "all" else [a for a in arg.split(",") if a in ITEMS]
    if not chosen:
        sys.exit(f"--apply needs 'all' or a comma list of {ITEMS}")
    os.makedirs(HOME, exist_ok=True)

    if {"models", "bypass"} & set(chosen):
        backup(SETTINGS)
        if "models" in chosen:
            settings["model"] = "opusplan"
            settings.setdefault("env", {})["CLAUDE_CODE_SUBAGENT_MODEL"] = "sonnet"
        if "bypass" in chosen:
            settings.setdefault("permissions", {})["defaultMode"] = "bypassPermissions"
        json.dump(settings, open(SETTINGS, "w", encoding="utf-8"), indent=2)
        print(f"updated {SETTINGS}")
    if "rules" in chosen:
        text = open(CLAUDE_MD, encoding="utf-8").read() if os.path.exists(CLAUDE_MD) else ""
        if "carriere-kit:rules:start" not in text:
            backup(CLAUDE_MD)
            with open(CLAUDE_MD, "a", encoding="utf-8") as f:
                f.write(("\n\n" if text else "") + open(os.path.join(HERE, "rules.md"), encoding="utf-8").read())
            print(f"updated {CLAUDE_MD}")
    print("Restart Claude Code to load the changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
