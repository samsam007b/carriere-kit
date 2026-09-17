#!/usr/bin/env python3
"""Pull the latest kit and shared database from the main repository.

  python3 tools/sync.py            update, report what changed
  python3 tools/sync.py --quiet    print only when something happened (SessionStart hook)
  python3 tools/sync.py --check    report how far behind, change nothing

Safe by design:
- workspace/ is never touched (ignored by git).
- Your uncommitted db/ records are saved, the update is applied fast-forward only, then
  your records are merged back record by record with `db.py` rules. No text conflicts.
- If you edited other kit files, or have local commits, nothing is changed and the
  report says why.
"""
import datetime, importlib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = json.load(open(os.path.join(ROOT, "kit.json"), encoding="utf-8"))
REF = "refs/remotes/kit-upstream/" + KIT["upstream_branch"]
QUIET = "--quiet" in sys.argv


def say(msg, always=False):
    if always or not QUIET:
        print(msg)


def git(*args, timeout=30, check=False):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def dataset_of(path):
    p = path.replace("\\", "/")
    if p.startswith("db/companies/") and p.endswith(".jsonl"):
        return "company"
    if p.startswith("db/postings/") and p.endswith(".jsonl"):
        return "posting"
    if p.startswith("db/search-filters/") and p.endswith(".json"):
        return "filter"
    return {"db/job-titles.jsonl": "job-title", "db/market-notes.jsonl": "market-note",
            "db/sources.jsonl": "source", "db/sweep-runs.jsonl": "sweep-run"}.get(p)


def parse(text, path):
    if path.endswith(".json"):
        return [json.loads(text)] if text.strip() else []
    return [json.loads(l) for l in text.splitlines() if l.strip()]


def freshness(rec):
    ev = rec.get("evidence") or {}
    return max(str(x) for x in (rec.get("updated_on"), rec.get("last_seen"), ev.get("verified_on"),
                                rec.get("verified_on"), rec.get("last_run"), rec.get("date"), "") if x is not None)


def main():
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        return 0
    url = f"https://github.com/{KIT['upstream']}.git"
    try:
        f = git("fetch", "--quiet", "--no-tags", url, f"+{KIT['upstream_branch']}:{REF}", timeout=20)
    except subprocess.TimeoutExpired:
        say("sync: main repository not reachable (timeout), working offline")
        return 0
    if f.returncode != 0:
        say("sync: main repository not reachable, working offline")
        return 0

    behind = int(git("rev-list", "--count", f"HEAD..{REF}").stdout.strip() or 0)
    if behind == 0:
        say("sync: kit and database are up to date")
        return 0
    if "--check" in sys.argv:
        say(f"sync: {behind} update(s) available from {KIT['upstream']}", always=True)
        return 0

    if git("symbolic-ref", "-q", "HEAD").returncode != 0:
        say(f"sync: {behind} update(s) available but HEAD is detached, skipped", always=True)
        return 0
    if git("merge-base", "--is-ancestor", "HEAD", REF).returncode != 0:
        say(f"sync: {behind} update(s) available but this clone has its own commits. "
            f"Run `git pull --rebase {url} {KIT['upstream_branch']}` when ready.", always=True)
        return 0

    status = git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    other = [l for l in status if not l[3:].startswith("db/")]
    if other:
        say(f"sync: {behind} update(s) available, not applied because kit files were edited locally: "
            + ", ".join(l[3:] for l in other[:5]), always=True)
        return 0

    # 1. save local db records that differ from HEAD
    changed = [l[3:].strip() for l in status]
    saved, backup = [], []
    for path in changed:
        ds = dataset_of(path)
        full = os.path.join(ROOT, path)
        if not ds or not os.path.isfile(full):
            continue
        head = git("show", f"HEAD:{path}")
        before = {r["id"]: r for r in parse(head.stdout, path)} if head.returncode == 0 else {}
        for rec in parse(open(full, encoding="utf-8").read(), path):
            if before.get(rec.get("id")) != rec:
                saved.append((ds, rec))
    if saved:
        logdir = os.path.join(ROOT, "workspace", ".logs")
        os.makedirs(logdir, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        with open(os.path.join(logdir, f"sync-backup-{stamp}.jsonl"), "w", encoding="utf-8") as fh:
            for ds, rec in saved:
                fh.write(json.dumps({"dataset": ds, "record": rec}, ensure_ascii=False) + "\n")

    # 2. reset db/ to HEAD and fast-forward
    tracked = [p for p in changed if git("ls-files", "--error-unmatch", p).returncode == 0]
    untracked = [p for p in changed if p not in tracked]
    if tracked:
        git("checkout", "HEAD", "--", *tracked, check=True)
    for p in untracked:
        full = os.path.join(ROOT, p)
        if os.path.isfile(full):
            os.remove(full)
    old_head = git("rev-parse", "HEAD").stdout.strip()
    git("merge", "--ff-only", "--quiet", REF, check=True)
    files = git("diff", "--name-only", old_head, "HEAD").stdout.split()
    db_files = [p for p in files if p.startswith("db/")]

    # 3. merge local records back with the fresh db.py (vocab or schemas may have changed)
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import db  # noqa: E402
    db = importlib.reload(db)
    reapplied, rejected = 0, []
    for ds, rec in saved:
        upstream = None
        for p in db.files_of(ds) if ds != "filter" else [os.path.join(db.DB, "search-filters", rec["id"] + ".json")]:
            for r in db.read(p):
                if r.get("id") == rec.get("id"):
                    upstream = r
        if upstream and freshness(upstream) > freshness(rec):
            rec = db.merge(rec, upstream)
        try:
            db.upsert_record(ds, rec)
            reapplied += 1
        except ValueError as e:
            rejected.append(f"{ds} {rec.get('id')}: {str(e).splitlines()[0]}")

    say(f"sync: pulled {behind} update(s) from {KIT['upstream']} "
        f"({len(db_files)} database file(s), {len(files) - len(db_files)} kit file(s) changed)", always=True)
    if saved:
        say(f"sync: your {reapplied} local database record(s) were merged back", always=True)
    for r in rejected:
        say(f"sync: could not re-apply {r} (kept in workspace/.logs/sync-backup-*.jsonl)", always=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # never break a session start
        print(f"sync: skipped ({e})")
        sys.exit(0)
