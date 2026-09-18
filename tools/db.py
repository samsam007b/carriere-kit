#!/usr/bin/env python3
"""Shared database of carriere-kit: validate, write, search, scan for personal data.

Every agent and every tool writes to db/ THROUGH this script, never by hand,
so all clones of the kit keep the same format and the same vocabulary.

Usage (from anywhere):
  python3 tools/db.py validate                 check every file against db/vocab.json and the schemas below
  python3 tools/db.py fmt                      rewrite every file in canonical form (sorted keys, sorted by id)
  python3 tools/db.py stats                    counts per dataset and per sector
  python3 tools/db.py find <text>              search companies, postings, job titles
  python3 tools/db.py stale [days]             postings to re-confirm at the source (default 60 days)
  python3 tools/db.py upsert <dataset> '<json>' insert or merge a record by id (dataset: company, posting,
                                               job-title, market-note, source, sweep-run, filter)
  python3 tools/db.py upsert <dataset> -       same, one JSON object per line on stdin
  python3 tools/db.py pii-scan [files...]      look for personal data (emails, phones, profile URLs, first person)
  python3 tools/db.py id company "Name"        print the canonical id for a name

Python 3.9+, standard library only. Exit code 1 on any error.
"""
import datetime, hashlib, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db")
VOCAB = json.load(open(os.path.join(DB, "vocab.json"), encoding="utf-8"))

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
COUNTRY = re.compile(r"^([A-Z]{2}|EU|WW)$")
LANG = re.compile(r"^[a-z]{2}$")
SIZES = ["1-10", "11-50", "51-200", "201-1000", "1001-5000", "5000+"]
NOTE_MAX = 500


def slug(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"&", " and ", t)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def posting_id(url):
    return "p-" + hashlib.sha1(url.strip().encode()).hexdigest()[:12]


# ---------------------------------------------------------------- schemas
# field: (type, required, extra check or vocab key)
def v(key):
    return ("vocab", key)


SCHEMAS = {
    "company": {
        "id": (str, True, ID), "name": (str, True, None), "sector": (str, True, v("sectors")),
        "sectors_secondary": (list, False, v("sectors")), "country": (str, True, COUNTRY),
        "city": (str, False, None), "website": (str, False, "url"), "careers_url": (str, False, "url"),
        "ats": (dict, False, "ats"), "size": (str, False, SIZES), "tags": (list, False, ID),
        "sources": (list, True, "sources"), "notes": (str, False, "note"), "updated_on": (str, True, DATE),
    },
    "posting": {
        "id": (str, True, None), "company_id": (str, True, ID), "title": (str, True, None),
        "family": (str, True, v("job_families")), "seniority": (str, True, v("seniority")),
        "location": (str, False, None), "country": (str, False, COUNTRY), "remote": (bool, False, None),
        "url": (str, True, "url"), "status": (str, True, v("posting_status")),
        "evidence": (dict, True, "evidence"), "first_seen": (str, True, DATE), "last_seen": (str, True, DATE),
        "requirements": (dict, False, "requirements"), "salary": (dict, False, "salary"),
        "deadline": (str, False, DATE), "found_by": (str, False, ID), "notes": (str, False, "note"),
    },
    "job-title": {
        "id": (str, True, ID), "title": (str, True, None), "lang": (str, True, LANG),
        "family": (str, True, v("job_families")), "seniority_typical": (list, True, v("seniority")),
        "markets": (list, False, COUNTRY), "aliases": (list, False, None), "notes": (str, False, "note"),
    },
    "market-note": {
        "id": (str, True, ID), "scope": (str, True, re.compile(r"^([A-Z]{2}|EU|WW)(-[A-Za-z-]+)?$")),
        "topic": (str, True, v("note_topics")), "note": (str, True, "note"),
        "source_url": (str, False, "url"), "verified_on": (str, True, DATE),
    },
    "source": {
        "id": (str, True, ID), "name": (str, True, None), "type": (str, True, v("evidence_source")),
        "url": (str, False, "url"), "country": (str, False, COUNTRY), "sectors": (list, True, v("sectors")),
        "coverage": (dict, False, None), "method": (str, True, None), "last_run": (str, False, DATE),
    },
    "sweep-run": {
        "id": (str, True, None), "date": (str, True, DATE), "filter": (str, True, ID),
        "boards_total": (int, True, None), "boards_dead": (int, True, None),
        "postings_scanned": (int, True, None), "matches": (int, True, None), "new_matches": (int, False, None),
    },
    "filter": {
        "id": (str, True, ID), "description": (str, True, None), "title_regex": (str, True, "regex"),
        "exclude_title_regex": (str, False, "regex"), "location_regex": (str, True, "regex"),
        "keep_empty_location": (bool, False, None), "families": (list, False, v("job_families")),
        "seniority": (list, False, v("seniority")), "updated_on": (str, True, DATE),
    },
}

# where each dataset lives
def files_of(dataset):
    if dataset == "company":
        return sorted(os.path.join(DB, "companies", f) for f in os.listdir(os.path.join(DB, "companies")) if f.endswith(".jsonl"))
    if dataset == "posting":
        return sorted(os.path.join(DB, "postings", f) for f in os.listdir(os.path.join(DB, "postings")) if f.endswith(".jsonl"))
    if dataset == "filter":
        return sorted(os.path.join(DB, "search-filters", f) for f in os.listdir(os.path.join(DB, "search-filters")) if f.endswith(".json"))
    return [os.path.join(DB, {"job-title": "job-titles.jsonl", "market-note": "market-notes.jsonl",
                              "source": "sources.jsonl", "sweep-run": "sweep-runs.jsonl"}[dataset])]


def target_file(dataset, rec):
    if dataset == "company":
        return os.path.join(DB, "companies", rec["sector"] + ".jsonl")
    if dataset == "posting":
        comp = company_index().get(rec.get("company_id"))
        sector = comp["sector"] if comp else "other"
        return os.path.join(DB, "postings", sector + ".jsonl")
    if dataset == "filter":
        return os.path.join(DB, "search-filters", rec["id"] + ".json")
    return files_of(dataset)[0]


def read(path):
    if not os.path.exists(path):
        return []
    if path.endswith(".json"):
        return [json.load(open(path, encoding="utf-8"))]
    out = []
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{rel(path)}:{n}: invalid JSON ({e})")
    return out


def write(path, records):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        if path.endswith(".json"):
            f.write(json.dumps(records[0], ensure_ascii=False, sort_keys=True, indent=2) + "\n")
        else:
            for r in sorted(records, key=lambda r: r["id"]):
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def rel(p):
    return os.path.relpath(p, ROOT)


_company_cache = None
def company_index():
    global _company_cache
    if _company_cache is None:
        _company_cache = {r["id"]: r for p in files_of("company") for r in read(p)}
    return _company_cache


# ---------------------------------------------------------------- validation
def check_value(dataset, field, val, rule, errs, where):
    typ, _, extra = rule
    if typ is int and isinstance(val, bool) or not isinstance(val, typ):
        errs.append(f"{where}: '{field}' must be {typ.__name__}")
        return
    items = val if isinstance(val, list) else [val]
    for it in items:
        if extra is None:
            continue
        if isinstance(extra, tuple) and extra[0] == "vocab":
            if it not in VOCAB[extra[1]]:
                errs.append(f"{where}: '{field}' value '{it}' is not in vocab.{extra[1]}")
        elif isinstance(extra, re.Pattern):
            if not isinstance(it, str) or not extra.match(it):
                errs.append(f"{where}: '{field}' value '{it}' has the wrong format")
        elif isinstance(extra, list):
            if it not in extra:
                errs.append(f"{where}: '{field}' must be one of {extra}")
        elif extra == "url":
            if not re.match(r"^https?://", it):
                errs.append(f"{where}: '{field}' must be an http(s) URL")
        elif extra == "note":
            if len(it) > NOTE_MAX:
                errs.append(f"{where}: '{field}' longer than {NOTE_MAX} chars, move detail elsewhere")
        elif extra == "regex":
            try:
                re.compile(it)
            except re.error as e:
                errs.append(f"{where}: '{field}' invalid regex ({e})")
        elif extra == "ats":
            if set(it) - {"provider", "slug", "status", "checked_on"} or not {"provider", "slug"} <= set(it):
                errs.append(f"{where}: 'ats' needs provider+slug, optional status+checked_on")
            elif it["provider"] not in VOCAB["ats"]:
                errs.append(f"{where}: ats.provider '{it['provider']}' not in vocab.ats")
            elif "status" in it and it["status"] not in VOCAB["board_status"]:
                errs.append(f"{where}: ats.status '{it['status']}' not in vocab.board_status")
            elif "checked_on" in it and not DATE.match(it["checked_on"]):
                errs.append(f"{where}: ats.checked_on must be YYYY-MM-DD")
        elif extra == "sources":
            for s in it if isinstance(it, list) else [it]:
                if not isinstance(s, dict) or set(s) - {"type", "ref", "seen_on"} or "type" not in s:
                    errs.append(f"{where}: each source is {{type, ref, seen_on}}")
                elif s["type"] not in VOCAB["evidence_source"]:
                    errs.append(f"{where}: source type '{s['type']}' not in vocab.evidence_source")
        elif extra == "evidence":
            if set(it) - {"source", "verified_on", "ref"} or not {"source", "verified_on"} <= set(it):
                errs.append(f"{where}: evidence is {{source, verified_on, ref?}}")
            elif it["source"] not in VOCAB["evidence_source"] or not DATE.match(it["verified_on"]):
                errs.append(f"{where}: evidence.source must be in vocab, verified_on YYYY-MM-DD")
        elif extra == "requirements":
            allowed = {"experience_years_min", "languages", "degree", "other"}
            if set(it) - allowed:
                errs.append(f"{where}: requirements keys limited to {sorted(allowed)}")
            for l in it.get("languages", []):
                if not (isinstance(l, dict) and LANG.match(l.get("lang", "")) and l.get("level") in VOCAB["language_levels"]):
                    errs.append(f"{where}: requirements.languages items are {{lang: 'nl', level: 'B2'}}")
        elif extra == "salary":
            if set(it) - {"min", "max", "currency", "period"} or it.get("period") not in (None, "year", "month", "hour"):
                errs.append(f"{where}: salary is {{min, max, currency, period: year|month|hour}}")


def validate_record(dataset, rec, where):
    errs = []
    schema = SCHEMAS[dataset]
    if not isinstance(rec, dict):
        return [f"{where}: record must be a JSON object"]
    for k in rec:
        if k not in schema:
            errs.append(f"{where}: unknown field '{k}' (allowed: {', '.join(schema)})")
    for field, rule in schema.items():
        if field not in rec:
            if rule[1]:
                errs.append(f"{where}: missing required field '{field}'")
            continue
        check_value(dataset, field, rec[field], rule, errs, where)
    if dataset == "posting" and rec.get("url") and rec.get("id") != posting_id(rec["url"]):
        errs.append(f"{where}: posting id must be {posting_id(rec['url'])} (derived from url)")
    return errs


def cmd_validate():
    errs, seen = [], {}
    for ds in SCHEMAS:
        for path in files_of(ds):
            recs = read(path)
            for i, r in enumerate(recs, 1):
                where = f"{rel(path)}:{i}"
                errs += validate_record(ds, r, where)
                key = (ds, r.get("id"))
                if key in seen:
                    errs.append(f"{where}: duplicate id '{r.get('id')}' (also in {seen[key]})")
                seen[key] = where
                if ds == "company" and os.path.basename(path) != f"{r.get('sector')}.jsonl":
                    errs.append(f"{where}: company with sector '{r.get('sector')}' must live in companies/{r.get('sector')}.jsonl")
                if ds == "filter" and os.path.basename(path) != f"{r.get('id')}.json":
                    errs.append(f"{where}: filter file name must be <id>.json")
    companies = company_index()
    for path in files_of("posting"):
        for i, r in enumerate(read(path), 1):
            if r.get("company_id") not in companies:
                errs.append(f"{rel(path)}:{i}: company_id '{r.get('company_id')}' does not exist in db/companies")
    errs += pii_scan(all_db_files())
    for e in errs:
        print(e)
    n = sum(len(read(p)) for ds in SCHEMAS for p in files_of(ds))
    print(f"{'FAIL' if errs else 'OK'}: {n} records, {len(errs)} errors", file=sys.stderr)
    return 1 if errs else 0


def all_db_files():
    return [p for ds in SCHEMAS for p in files_of(ds)]


# ---------------------------------------------------------------- personal data scan
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]*[A-Za-z]{2,}")
PHONE = re.compile(r"\+\d[\d .()/-]{7,}\d|\b0\d{2,3}[ ./]\d{2,3}[ ./]\d{2,3}[ ./]?\d{0,3}\b")
PROFILE_URL = re.compile(r"linkedin\.com/in/|facebook\.com/|instagram\.com/", re.I)
# first person and profile judgements only matter in free text fields
FREE_TEXT = ("notes", "note", "method", "description")
FIRST_PERSON = re.compile(r"\b(I|I'm|I've|my|mine|je|j'ai|mon|mes|moi|ik|mijn|ich|mein|yo|mi)\b")
FIT_JUDGEMENT = re.compile(r"(my|his|her|their|mon|son|sa) profil|fit for (me|him|her)|pour moi|voor mij|dream job|priority for", re.I)
URL_FIELDS = ("url", "website", "careers_url", "source_url", "ref")


def _strings(obj, key=""):
    if isinstance(obj, dict):
        for k, val in obj.items():
            yield from _strings(val, k)
    elif isinstance(obj, list):
        for val in obj:
            yield from _strings(val, key)
    elif isinstance(obj, str):
        yield key, obj


def pii_scan(paths, extra_terms=()):
    hits = []
    terms = [t for t in extra_terms if isinstance(t, str) and len(t) >= 3]
    for path in paths:
        for n, rec in enumerate(read(path), 1):
            hits += pii_record(rec, f"{rel(path)}:{n}", terms)
    return hits


def pii_record(rec, label, terms=()):
    hits = []
    for key, text in _strings(rec):
                where = f"{label} [{key}]"
                if key not in URL_FIELDS and key not in ("title_regex", "location_regex", "exclude_title_regex"):
                    if EMAIL.search(text):
                        hits.append(f"{where}: email address '{EMAIL.search(text).group(0)}'")
                    if PHONE.search(text):
                        hits.append(f"{where}: phone-like number '{PHONE.search(text).group(0)}'")
                if PROFILE_URL.search(text):
                    hits.append(f"{where}: link to a personal profile")
                if key in FREE_TEXT:
                    if FIRST_PERSON.search(text):
                        hits.append(f"{where}: first person wording '{FIRST_PERSON.search(text).group(0)}' (db/ is impersonal)")
                    if FIT_JUDGEMENT.search(text):
                        hits.append(f"{where}: personal fit judgement (keep it in workspace/)")
                for t in terms:
                    if re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", text, re.I):
                        hits.append(f"{where}: contains a private term from workspace/config.json")
    return hits


# ---------------------------------------------------------------- freshness
# A posting record says what was true the day it was last confirmed at the source, and
# nothing about today. Nothing in db/ expires on its own (an expiry date written into the
# data would be a guess, and would go stale in its own right), so freshness is computed
# at read time from the last date the record was actually confirmed.
STALE_DAYS = 60


def confirmed_on(rec):
    """The day this record was last confirmed at the source, or None."""
    for k in ("last_seen", "checked_on", "verified_on", "last_run", "updated_on", "date"):
        val = rec.get(k)
        if isinstance(val, str) and DATE.match(val):
            return val
    ats = rec.get("ats")
    if isinstance(ats, dict) and isinstance(ats.get("checked_on"), str) and DATE.match(ats["checked_on"]):
        return ats["checked_on"]
    return None


def age_days(rec, today=None):
    """Days since this record was last confirmed. None when it was never confirmed."""
    day = confirmed_on(rec)
    if not day:
        return None
    today = today or datetime.date.today()
    try:
        return (today - datetime.date.fromisoformat(day)).days
    except ValueError:
        return None


def is_stale(rec, today=None, days=STALE_DAYS):
    age = age_days(rec, today)
    return age is None or age >= days


def cmd_stale(days=STALE_DAYS):
    """Records that must be re-confirmed at the source before anyone acts on them."""
    n = 0
    for r in (x for p in files_of("posting") for x in read(p)):
        if r.get("status") == "closed":
            continue
        age = age_days(r)
        if r.get("status") == "unverified" or is_stale(r, days=days):
            n += 1
            why = "never confirmed" if age is None else f"{age} days old"
            print(f"[posting] {r['id']}  {r.get('title', '')[:60]}  {r.get('status')}, {why}")
            print(f"           {r.get('url', '')}")
    boards = 0
    for r in (x for p in files_of("company") for x in read(p)):
        ats = r.get("ats") or {}
        if ats and ats.get("status") != "dead" and is_stale(r, days=days):
            boards += 1
    print(f"\n{n} posting(s) to re-confirm, {boards} job board(s) not scanned for {days}+ days", file=sys.stderr)
    if boards:
        print("re-scan with: python3 tools/sweep.py --filter <id>", file=sys.stderr)
    return 0


# ---------------------------------------------------------------- other commands
def cmd_fmt():
    for ds in SCHEMAS:
        for path in files_of(ds):
            recs = read(path)
            if recs:
                write(path, recs)
    print("formatted", file=sys.stderr)
    return 0


def cmd_stats():
    for ds in SCHEMAS:
        paths = files_of(ds)
        total = sum(len(read(p)) for p in paths)
        print(f"{ds:12} {total:6}")
        if ds in ("company", "posting"):
            for p in paths:
                print(f"  {os.path.basename(p)[:-6]:32} {len(read(p)):5}")
    post = [r for p in files_of("posting") for r in read(p)]
    live = [r for r in post if r.get("status") != "closed"]
    stale = [r for r in live if is_stale(r)]
    if stale:
        print(f"\n{len(stale)} of {len(live)} open posting(s) not confirmed for {STALE_DAYS}+ days: "
              f"run `python3 tools/db.py stale` before trusting them")
    return 0


def cmd_find(q):
    qn = slug(q)
    for ds in ("company", "posting", "job-title"):
        for p in files_of(ds):
            for r in read(p):
                blob = slug(" ".join(str(x) for x in (r.get("name"), r.get("title"), r.get("id"), r.get("company_id"), " ".join(r.get("aliases", [])))))
                if qn and qn in blob:
                    age = age_days(r)
                    # a hit nobody re-confirmed recently must not read like a live fact
                    flag = ""
                    if ds == "posting" and r.get("status") != "closed" and is_stale(r):
                        flag = "  STALE: re-confirm at the source" + (f" ({age} days old)" if age is not None else " (never confirmed)")
                    print(f"[{ds}] {rel(p)}  {json.dumps(r, ensure_ascii=False)[:300]}{flag}")
    return 0


def merge(old, new):
    out = dict(old)
    for k, val in new.items():
        if k == "sources" and isinstance(val, list):
            known = {json.dumps(s, sort_keys=True) for s in out.get("sources", [])}
            out["sources"] = out.get("sources", []) + [s for s in val if json.dumps(s, sort_keys=True) not in known]
        elif k == "first_seen" and "first_seen" in out:
            out[k] = min(out[k], val)
        elif k == "last_seen" and "last_seen" in out:
            out[k] = max(out[k], val)
        else:
            out[k] = val
    return out


def upsert_record(dataset, rec):
    """Insert or merge a single record dict by id, the programmatic twin of
    `cmd_upsert` used by tools that write to db/ in-process (resolve.py, sweep.py)
    instead of shelling back out to `db.py upsert`.

    Returns (action, id, dest_path) where action is "added" or "updated".
    Raises ValueError (message = newline-joined validation/pii errors) on failure;
    nothing is written to disk in that case.
    """
    if dataset not in SCHEMAS:
        raise ValueError(f"unknown dataset '{dataset}', use one of {list(SCHEMAS)}")
    if dataset == "posting" and "url" in rec:
        rec.setdefault("id", posting_id(rec["url"]))
    if dataset == "company" and "id" not in rec and "name" in rec:
        rec["id"] = slug(rec["name"])
    # find existing record anywhere in the dataset (a company may change sector)
    existing, where = None, None
    for p in files_of(dataset) if dataset != "filter" else []:
        for r in read(p):
            if r["id"] == rec.get("id"):
                existing, where = r, p
    merged = merge(existing, rec) if existing else rec
    errs = validate_record(dataset, merged, f"{dataset} '{merged.get('id')}'")
    errs += pii_record(merged, f"{dataset} '{merged.get('id')}'", private_terms())
    if errs:
        raise ValueError("\n".join(errs))
    dest = target_file(dataset, merged)
    if where and where != dest:
        write(where, [r for r in read(where) if r["id"] != merged["id"]])
    recs = [r for r in read(dest) if r["id"] != merged["id"]] + [merged]
    write(dest, recs)
    if dataset == "company":
        company_index()[merged["id"]] = merged
    return ("updated" if existing else "added", merged["id"], dest)


def cmd_upsert(dataset, payload):
    if dataset not in SCHEMAS:
        raise SystemExit(f"unknown dataset '{dataset}', use one of {list(SCHEMAS)}")
    lines = sys.stdin.read().splitlines() if payload == "-" else [payload]
    errs, n = [], 0
    for line in lines:
        if not line.strip():
            continue
        rec = json.loads(line)
        try:
            action, rid, dest = upsert_record(dataset, rec)
        except ValueError as e:
            errs += str(e).split("\n")
            continue
        n += 1
        print(f"{action} {dataset} {rid} -> {rel(dest)}")
    for e in errs:
        print(e, file=sys.stderr)
    return 1 if errs else 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    c = argv[1]
    if c == "validate":
        return cmd_validate()
    if c == "fmt":
        return cmd_fmt()
    if c == "stats":
        return cmd_stats()
    if c == "stale":
        return cmd_stale(int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else STALE_DAYS)
    if c == "find" and len(argv) > 2:
        return cmd_find(" ".join(argv[2:]))
    if c == "upsert" and len(argv) > 3:
        return cmd_upsert(argv[2], argv[3])
    if c == "id" and len(argv) > 3:
        print(slug(argv[3]) if argv[2] == "company" else posting_id(argv[3]))
        return 0
    if c == "pii-scan":
        paths = argv[2:] or all_db_files()
        hits = pii_scan([os.path.abspath(p) for p in paths if os.path.abspath(p).startswith(DB) and p.endswith((".json", ".jsonl")) and not p.endswith("vocab.json")], private_terms())
        for h in hits:
            print(h)
        print(f"{len(hits)} possible personal data hits", file=sys.stderr)
        return 1 if hits else 0
    print(__doc__)
    return 1


def private_terms():
    """Words from the local private profile that must never reach db/ (name, email, city...)."""
    cfg = os.path.join(ROOT, "workspace", "config.json")
    if not os.path.exists(cfg):
        return []
    try:
        return [t for t in json.load(open(cfg, encoding="utf-8")).get("private_terms", []) if isinstance(t, str)]
    except Exception:
        return []


if __name__ == "__main__":
    sys.exit(main(sys.argv))
