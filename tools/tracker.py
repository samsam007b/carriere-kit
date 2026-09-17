#!/usr/bin/env python3
"""Machine reading of the tracker: due follow-ups, dedup check, schema lint.

Operates on workspace/tracker.md and workspace/tracker-archive.md (override
the workspace root with --workspace <dir>). Standard library only.

Usage (from the repo root):
    python3 tools/tracker.py followups            due / overdue / missing follow-up date
    python3 tools/tracker.py check "<name>" ...    step 0 of any new research, see method/01
    python3 tools/tracker.py lint                  validate tracker.md and tracker-archive.md
    python3 tools/tracker.py --workspace <dir> ...  use a different workspace root (mainly for tests)

Same discipline as tools/db.py: what fails prints on stderr, never gets swallowed.
A row with a broken schema is reported, not silently skipped, because a tracker
that degrades quietly is worse than no tracker at all.
"""
import sys, os, re, json, datetime as dt, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db")

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")

HEADER = "| Lead | Type | Status | Submitted | Follow-up | Last action | Source |"


def load_vocab():
    path = os.path.join(DB, "vocab.json")
    if not os.path.exists(path):
        return {"pipeline_types": {}, "pipeline_status": {}}
    return json.load(open(path, encoding="utf-8"))


def norm(s):
    """Collapse case, accents, dashes and punctuation: 'Roland-Berger' == 'roland berger'."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return " ".join(s.split())


def parse_rows(path):
    """Return (rows, errors). Each row is a dict plus _file/_line for error messages."""
    rows, errors = [], []
    if not os.path.exists(path):
        return rows, errors
    name = os.path.basename(path)
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.startswith("|") or line.startswith("|---"):
            continue
        # a markdown cell may contain an escaped pipe (\|), as the template placeholders do
        cols = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if cols and cols[0] in ("Lead", "---"):
            continue
        if len(cols) != 7:
            errors.append(f"{name}:{n}: {len(cols)} columns instead of 7")
            continue
        row = dict(zip(("lead", "type", "status", "submitted", "followup", "action", "source"), cols))
        row["lead"] = row["lead"].replace("**", "").strip()
        row["_file"], row["_line"] = name, n
        rows.append(row)
    return rows, errors


def validate_rows(rows, vocab):
    errors = []
    types = set(vocab.get("pipeline_types", {}))
    statuses = set(vocab.get("pipeline_status", {}))
    for r in rows:
        where = f"{r['_file']}:{r['_line']}"
        if not r["lead"] or r["lead"].startswith("{{"):
            continue  # unfilled template row, ignore
        if types and r["type"] not in types:
            errors.append(f"{where}: type '{r['type']}' not in vocab.pipeline_types")
        if statuses and r["status"] not in statuses:
            errors.append(f"{where}: status '{r['status']}' not in vocab.pipeline_status")
        for field in ("submitted", "followup"):
            v = r[field]
            if v not in ("", "-", "—") and not ISO.match(v):
                errors.append(f"{where}: '{field}' is not YYYY-MM-DD -> {v!r}")
        if r["status"] == "waiting" and r["type"] in ("application", "outreach"):
            if r["followup"] in ("", "-", "—") or not ISO.match(r["followup"]):
                errors.append(f"{where}: status 'waiting' requires a Follow-up date")
    return errors


def workspace_paths(args):
    ws = ROOT_WORKSPACE
    if "--workspace" in args:
        i = args.index("--workspace")
        ws = args[i + 1]
        del args[i:i + 2]
    return os.path.join(ws, "tracker.md"), os.path.join(ws, "tracker-archive.md"), args


ROOT_WORKSPACE = os.path.join(ROOT, "workspace")


# ---------------------------------------------------------------- followups
def cmd_followups(active_path):
    rows, errors = parse_rows(active_path)
    today = dt.date.today()
    overdue, due, missing = [], [], []
    for r in rows:
        if not r["lead"] or r["lead"].startswith("{{"):
            continue
        if r["status"] != "waiting":
            continue
        v = r["followup"]
        if v in ("", "-", "—") or not ISO.match(v):
            missing.append(r)
            continue
        d = dt.date.fromisoformat(v)
        if d < today:
            overdue.append((d, (today - d).days, r))
        elif d == today:
            due.append(r)

    overdue.sort(key=lambda t: (t[0], t[2]["lead"]))

    print(f"# Follow-ups as of {today.isoformat()}\n")
    print(f"## Overdue ({len(overdue)})\n")
    for d, days, r in overdue:
        print(f"- {r['lead']}: due {d.isoformat()}, {days} day(s) overdue (submitted {r['submitted']})")
    print(f"\n## Due today ({len(due)})\n")
    for r in due:
        print(f"- {r['lead']} (submitted {r['submitted']})")
    print(f"\n## Missing a follow-up date ({len(missing)})\n")
    for r in missing:
        print(f"- {r['lead']}: status 'waiting', no Follow-up date set")
    if not overdue and not due and not missing:
        print("Nothing to follow up on.")

    if errors:
        print(f"\n{len(errors)} row(s) with an invalid schema:", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
    return 0


# ---------------------------------------------------------------- check
def company_ids_and_names():
    """(id, name) pairs from db/companies/*.jsonl, if the db exists."""
    out = []
    companies_dir = os.path.join(DB, "companies")
    if not os.path.isdir(companies_dir):
        return out
    for fname in os.listdir(companies_dir):
        if not fname.endswith(".jsonl"):
            continue
        for line in open(os.path.join(companies_dir, fname), encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "id" in rec or "name" in rec:
                out.append((rec.get("name") or rec.get("id"), f"db/companies/{fname}"))
    return out


def known_entries(active_path, archive_path):
    """(name, source_description) for every known lead: tracker, archive, applications/, db/companies."""
    entries = []
    for path, label in ((active_path, "tracker.md"), (archive_path, "tracker-archive.md")):
        rows, _ = parse_rows(path)
        for r in rows:
            if r["lead"] and not r["lead"].startswith("{{"):
                entries.append((r["lead"], label))
    ws = os.path.dirname(active_path)
    apps_dir = os.path.join(ws, "applications")
    if os.path.isdir(apps_dir):
        for d in sorted(os.listdir(apps_dir)):
            if os.path.isdir(os.path.join(apps_dir, d)):
                entries.append((d, "workspace/applications/"))
    entries.extend(company_ids_and_names())
    return entries


def cmd_check(terms, active_path, archive_path):
    entries = known_entries(active_path, archive_path)
    code = 0
    for term in terms:
        n = norm(term)
        hits = [(name, src) for name, src in entries if n and n in norm(name)]
        if hits:
            code = 1
            print(f"KNOWN     {term}")
            seen = set()
            for name, src in hits:
                key = (name, src)
                if key in seen:
                    continue
                seen.add(key)
                print(f"          {name}  ({src})")
        else:
            print(f"new       {term}")
    return code


# ---------------------------------------------------------------- lint
def check_header(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("| Lead"):
                if line.strip() != HEADER:
                    return [f"{os.path.basename(path)}: header does not match the expected schema\n"
                             f"  expected: {HEADER}\n"
                             f"  found:    {line.strip()}"]
                return []
    return [f"{os.path.basename(path)}: no header row found"]


def cmd_lint(active_path, archive_path):
    vocab = load_vocab()
    errors = []
    for path in (active_path, archive_path):
        errors += check_header(path)
        rows, parse_errors = parse_rows(path)
        errors += parse_errors
        errors += validate_rows(rows, vocab)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("OK", file=sys.stderr)
    return 0


# ---------------------------------------------------------------- main
def main(argv):
    argv = list(argv)
    if argv[:1] == ["--workspace"]:  # accept the option before the command too, as the usage shows
        argv = argv[2:3] + argv[:2] + argv[3:]
    if not argv or argv[0] not in ("followups", "check", "lint"):
        print(__doc__)
        return 2
    cmd, rest = argv[0], list(argv[1:])
    active_path, archive_path, rest = workspace_paths(rest)
    if cmd == "followups":
        return cmd_followups(active_path)
    if cmd == "lint":
        return cmd_lint(active_path, archive_path)
    if cmd == "check":
        if not rest:
            print("check requires at least one name", file=sys.stderr)
            return 2
        return cmd_check(rest, active_path, archive_path)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
