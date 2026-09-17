#!/usr/bin/env python3
"""Send your database discoveries to the main repository as a pull request.

  python3 tools/contribute.py             contribute now, verbose
  python3 tools/contribute.py --dry-run   show what would be sent, send nothing
  python3 tools/contribute.py --auto      used by the SessionEnd hook: silent, respects
                                          "auto_contribute" in workspace/config.json

What it does:
1. Fetches the main repository and compares your db/ with it, record by record.
2. Keeps only records that are new or changed. Nothing outside db/ is ever read or sent.
3. Validates them and scans them for personal data (including your `private_terms`).
4. Rebuilds a branch `db-contrib/<github-login>` on top of the latest main repo, in a
   temporary worktree, and runs `db.py validate` there.
5. Pushes it to your fork (created if needed) and opens a pull request, or updates the
   one already open. Commits use your GitHub noreply address, never your git email.

Sending needs a free GitHub account and the GitHub CLI logged in (`gh auth login`). Without
them, the records wait in workspace/outbox/ and leave at the first run after connecting.
Receiving everyone else's records (tools/sync.py) needs no account.
"""
import datetime, json, os, shutil, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import db  # noqa: E402
from sync import dataset_of, parse, freshness  # noqa: E402

KIT = json.load(open(os.path.join(ROOT, "kit.json"), encoding="utf-8"))
UPSTREAM, BRANCH = KIT["upstream"], KIT["upstream_branch"]
REF = "refs/remotes/kit-upstream/" + BRANCH
AUTO, DRY = "--auto" in sys.argv, "--dry-run" in sys.argv
LOGS = os.path.join(ROOT, "workspace", ".logs")


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] {msg}" if AUTO else msg)


def run(cmd, cwd=ROOT, timeout=120, check=False, stdin=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, input=stdin)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:4])}: {(r.stderr or r.stdout).strip()[:300]}")
    return r


def config():
    p = os.path.join(ROOT, "workspace", "config.json")
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def upstream_index():
    names = run(["git", "ls-tree", "-r", "--name-only", REF, "db/"], check=True).stdout.split()
    idx = {}
    for path in names:
        ds = dataset_of(path)
        if not ds:
            continue
        for rec in parse(run(["git", "show", f"{REF}:{path}"], check=True).stdout, path):
            idx[(ds, rec["id"])] = rec
    return idx


def local_records():
    out = []
    for ds in db.SCHEMAS:
        for p in db.files_of(ds):
            for rec in db.read(p):
                out.append((ds, rec))
    return out


def contribution():
    idx = upstream_index()
    terms = db.private_terms()
    send, rejected = [], []
    for ds, rec in local_records():
        up = idx.get((ds, rec.get("id")))
        if up == rec:
            continue
        if up:
            payload = db.merge(up, rec) if freshness(rec) >= freshness(up) else db.merge(rec, up)
            if payload == up:
                continue
        else:
            payload = rec
        where = f"{ds} '{rec.get('id')}'"
        errs = db.validate_record(ds, payload, where) + db.pii_record(payload, where, terms)
        (rejected if errs else send).append((ds, payload, "updated" if up else "added", errs))
    return send, rejected


def github_ready():
    return bool(shutil.which("gh")) and run(["gh", "auth", "status"]).returncode == 0


def summary(send):
    counts = {}
    for ds, _, action, _ in send:
        counts.setdefault(ds, {"added": 0, "updated": 0})[action] += 1
    return counts


def title_of(counts):
    parts = []
    for ds, c in sorted(counts.items()):
        if c["added"]:
            parts.append(f"+{c['added']} {ds}")
        if c["updated"]:
            parts.append(f"~{c['updated']} {ds}")
    return "db: " + ", ".join(parts)


def main():
    cfg = config()
    if AUTO and (not cfg or cfg.get("auto_contribute") is False):
        return 0
    os.makedirs(LOGS, exist_ok=True)
    lock = os.path.join(LOGS, "contribute.lock")
    if os.path.exists(lock) and time.time() - os.path.getmtime(lock) < 600:
        log("contribute: another run is in progress, skipped")
        return 0
    open(lock, "w").write(str(os.getpid()))
    try:
        return _main()
    finally:
        if os.path.exists(lock):
            os.remove(lock)


def _main():
    url = f"https://github.com/{UPSTREAM}.git"
    if run(["git", "fetch", "--quiet", "--no-tags", url, f"+{BRANCH}:{REF}"], timeout=60).returncode != 0:
        log("contribute: main repository not reachable, will retry at the next session end")
        return 0

    send, rejected = contribution()
    for ds, rec, _, errs in rejected:
        log(f"contribute: NOT sent {ds} {rec.get('id')}: " + "; ".join(errs)[:300])
    if not send:
        if not AUTO or rejected:
            log("contribute: nothing new to send, the main repository already has your database records")
        return 0

    counts = summary(send)
    title = title_of(counts)
    if DRY:
        log(f"contribute (dry run): would open a pull request '{title}'")
        for ds, rec, action, _ in send:
            log(f"  {action:7} {ds:11} {rec['id']}")
        return 0

    if not github_ready():
        # No GitHub account or CLI yet: keep the contribution in a local outbox. It is rebuilt
        # from db/ at every run, so nothing is lost and it goes out once GitHub is connected.
        outbox = os.path.join(ROOT, "workspace", "outbox")
        os.makedirs(outbox, exist_ok=True)
        with open(os.path.join(outbox, "db-contribution.jsonl"), "w", encoding="utf-8") as fh:
            for ds, rec, action, _ in send:
                fh.write(json.dumps({"dataset": ds, "action": action, "record": rec}, ensure_ascii=False, sort_keys=True) + "\n")
        log(f"contribute: GitHub not connected, {len(send)} record(s) kept in workspace/outbox/ ({title}). "
            "They will be sent automatically once GitHub is connected (skill `connect-github`).")
        return 0

    login = run(["gh", "api", "user", "-q", ".login"], check=True).stdout.strip()
    uid = run(["gh", "api", "user", "-q", ".id"], check=True).stdout.strip()
    owner, name = UPSTREAM.split("/")
    is_owner = login.lower() == owner.lower()
    if not is_owner:
        run(["gh", "repo", "fork", UPSTREAM, "--clone=false", "--remote=false"], timeout=120)
    target = UPSTREAM if is_owner else f"{login}/{name}"
    branch = f"{KIT['contribution_branch_prefix']}{login}"

    tmp = tempfile.mkdtemp(prefix="kit-contrib-")
    wt = os.path.join(tmp, "wt")
    try:
        run(["git", "worktree", "add", "--detach", wt, REF], check=True)
        by_ds = {}
        for ds, rec, _, _ in send:
            by_ds.setdefault(ds, []).append(rec)
        # companies first: postings are filed under their company's sector
        order = ["company"] + [d for d in by_ds if d != "company"]
        for ds in order:
            if ds not in by_ds:
                continue
            body = "\n".join(json.dumps(r, ensure_ascii=False) for r in by_ds[ds])
            r = run([sys.executable, "tools/db.py", "upsert", ds, "-"], cwd=wt, stdin=body)
            if r.returncode != 0:
                raise RuntimeError(f"upsert {ds} failed in clean tree: {r.stderr.strip()[:300]}")
        v = run([sys.executable, "tools/db.py", "validate"], cwd=wt)
        if v.returncode != 0:
            raise RuntimeError(f"validation failed on top of the main repo: {(v.stdout + v.stderr).strip()[:400]}")
        # only db/ may change
        stray = [l for l in run(["git", "status", "--porcelain"], cwd=wt).stdout.splitlines() if not l[3:].startswith("db/")]
        if stray:
            raise RuntimeError("files outside db/ changed, aborting: " + ", ".join(stray[:5]))

        ident = ["-c", f"user.name={login}", "-c", f"user.email={uid}+{login}@users.noreply.github.com"]
        run(["git", "add", "db"], cwd=wt, check=True)
        run(["git", *ident, "commit", "--quiet", "-m", title,
             "-m", "Automatic database contribution from carriere-kit tools/contribute.py."], cwd=wt, check=True)
        cred = ["-c", "credential.helper=", "-c", "credential.helper=!gh auth git-credential"]
        run(["git", *cred, "push", "--quiet", "--force", f"https://github.com/{target}.git",
             f"HEAD:refs/heads/{branch}"], cwd=wt, timeout=120, check=True)

        head = branch if is_owner else f"{login}:{branch}"
        existing = run(["gh", "pr", "list", "--repo", UPSTREAM, "--head", branch, "--state", "open",
                        "--json", "number,url,headRepositoryOwner"]).stdout
        prs = [p for p in json.loads(existing or "[]") if (p.get("headRepositoryOwner") or {}).get("login", "").lower() == login.lower()]
        lines = [f"| {ds} | {c['added']} | {c['updated']} |" for ds, c in sorted(counts.items())]
        body = ("Database contribution, generated by `tools/contribute.py`.\n\n"
                "| Dataset | Added | Updated |\n|---|---|---|\n" + "\n".join(lines) +
                "\n\nValidated with `tools/db.py validate` and the personal-data scan before pushing. "
                "CI runs both again.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n")
        if prs:
            run(["gh", "pr", "edit", str(prs[0]["number"]), "--repo", UPSTREAM, "--title", title, "--body", body])
            pr_url = prs[0]["url"]
            log(f"contribute: updated pull request {pr_url} ({title})")
        else:
            r = run(["gh", "pr", "create", "--repo", UPSTREAM, "--base", BRANCH, "--head", head,
                     "--title", title, "--body", body], timeout=120, check=True)
            pr_url = r.stdout.strip().splitlines()[-1]
            log(f"contribute: opened pull request {pr_url} ({title})")
        json.dump({"date": datetime.date.today().isoformat(), "pr": pr_url, "title": title},
                  open(os.path.join(LOGS, "last-contribution.json"), "w"), indent=2)
        return 0
    finally:
        run(["git", "worktree", "remove", "--force", wt])
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log(f"contribute: failed ({e})")
        sys.exit(0 if AUTO else 1)
