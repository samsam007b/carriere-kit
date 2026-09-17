#!/usr/bin/env python3
"""Resolve company names to verified ATS board slugs.

Takes a list of company names (one per line, comment lines starting with #
ignored), tries each name and a handful of spelling variants against all
seven ATS in ats.py, and reports which (provider, slug) pairs actually
answer -- and how many postings each one lists right now.

Why this exists: hand-guessing a slug from a company name is wrong often
enough to matter. An earlier audit of a hand-built board list found two
thirds of the entries dead, split between a wrong guessed slug and a company
that turned out to live on a different ATS entirely (a company is not on
Ashby just because it feels like an Ashby company). Guessing is not a
one-time cost either: companies migrate ATS providers over time, so a board
that resolved cleanly six months ago can quietly go dead.

The other half of that same lesson: a board that answers with zero postings
right now is not the same thing as a dead board, and must not be reported as
one. The original version of this script conflated the two ("if not result:
treat as not found"), which silently dropped every live-but-currently-empty
board from the result. Fixed here: only an exception from ats.py (board does
not exist / does not answer) counts as "not found".

Usage:
  python3 tools/resolve.py names.txt
  python3 tools/resolve.py names.txt --sector software-saas --country BE --write
  python3 tools/resolve.py --recheck-dead --write
  python3 tools/resolve.py names.txt --recheck-dead --sector software-saas --country BE --write
"""
import argparse
import concurrent.futures as cf
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ats
import db


def variants(name):
    """A handful of plausible slug spellings for a company name. Not
    exhaustive by design -- it only needs to catch the common cases
    (spaces vs dashes, punctuation, casing); anything more exotic is a
    manual entry, not a job for pattern-guessing.
    """
    n = name.strip().lower()
    candidates = [n, n.replace("-", ""), n.replace(" ", "-"), n.replace(" ", ""), n.replace("'", "")]
    out = []
    for x in candidates:
        x = x.strip("-")
        if x and x not in out:
            out.append(x)
    return out


def probe(job):
    """Try one (provider, slug) pair. Returns (provider, slug, count, status)
    on any answer (including a valid empty board), or None if the board does
    not exist / does not answer at all -- that distinction is the whole
    point of this function, see module docstring.
    """
    provider, slug = job
    try:
        postings = ats.FN[provider](slug)
    except ats.BoardError:
        return None
    except Exception:
        # Anything else (malformed response, etc.) is also "not this slug",
        # not a crash of the whole resolve run.
        return None
    status = "live" if postings else "empty"
    return (provider, slug, len(postings), status)


def resolve_names(names):
    """For each name, probe every variant against every provider and keep the
    single best match (most postings, live preferred over empty).
    Returns {name: (provider, slug, count, status) or None}.
    """
    jobs = []
    job_owner = {}
    for name in names:
        for v in variants(name):
            for provider in ats.FN:
                jobs.append((provider, v))
                job_owner.setdefault((provider, v), []).append(name)

    best = {name: None for name in names}
    with cf.ThreadPoolExecutor(16) as ex:
        for job, result in zip(jobs, ex.map(probe, jobs)):
            if not result:
                continue
            for name in job_owner[job]:
                current = best[name]
                if current is None or result[2] > current[2] or (result[2] == current[2] and result[3] == "live" and current[3] == "empty"):
                    best[name] = result
    return best


def recheck_dead():
    """Re-probe every company in db/ whose ats.status is "dead", using its
    stored provider+slug (not name guessing -- the slug was already
    verified once, we are only asking if the board came back).
    Returns {company_id: (provider, slug, count, status) or None}.
    """
    out = {}
    jobs, owners = [], {}
    for company_id, rec in db.company_index().items():
        entry = rec.get("ats")
        if entry and entry.get("status") == "dead":
            job = (entry["provider"], entry["slug"])
            jobs.append(job)
            owners.setdefault(job, []).append(company_id)
    with cf.ThreadPoolExecutor(16) as ex:
        for job, result in zip(jobs, ex.map(probe, jobs)):
            for company_id in owners[job]:
                out[company_id] = result
    return out


def main(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("names_file", nargs="?", help="file of company names, one per line ('-' for stdin)")
    p.add_argument("--sector", help="vocab.sectors id, required by --write to create a company that is not yet in db/")
    p.add_argument("--country", help="ISO country code (or EU/WW), required by --write to create a company that is not yet in db/")
    p.add_argument("--write", action="store_true", help="upsert results into db/ instead of only printing them")
    p.add_argument("--recheck-dead", action="store_true", help="also re-probe every company whose ats.status is dead")
    args = p.parse_args(argv[1:])

    if not args.names_file and not args.recheck_dead:
        p.error("give a names file, or pass --recheck-dead, or both")

    today = datetime.date.today().isoformat()
    exit_code = 0

    if args.recheck_dead:
        results = recheck_dead()
        if not results:
            print("# no dead boards in db/", file=sys.stderr)
        for company_id in sorted(results):
            result = results[company_id]
            if not result:
                print(f"dead {company_id}  (still no answer)")
                continue
            provider, slug, count, status = result
            flag = "  (empty)" if status == "empty" else ""
            print(f"{provider} {slug} {count}{flag}  [{company_id}]")
            if args.write:
                rec = {"id": company_id, "ats": {"provider": provider, "slug": slug, "status": status, "checked_on": today}}
                try:
                    action, rid, dest = db.upsert_record("company", rec)
                    print(f"  -> {action} {rid}", file=sys.stderr)
                except ValueError as e:
                    print(f"  -> ERROR: {e}", file=sys.stderr)
                    exit_code = 1

    if args.names_file:
        src = sys.stdin if args.names_file == "-" else open(args.names_file, encoding="utf-8")
        names = [l.strip() for l in src if l.strip() and not l.startswith("#")]
        results = resolve_names(names)

        found = 0
        for name in names:
            result = results[name]
            if not result:
                print(f"# not found: {name}", file=sys.stderr)
                continue
            found += 1
            provider, slug, count, status = result
            flag = "  (empty)" if status == "empty" else ""
            print(f"{provider} {slug} {count}{flag}")

            if args.write:
                company_id = db.slug(name)
                existing = db.company_index().get(company_id)
                rec = {"id": company_id, "ats": {"provider": provider, "slug": slug, "status": status, "checked_on": today}}
                if not existing:
                    if not (args.sector and args.country):
                        print(f"  -> ERROR: {name} is not yet in db/, need --sector and --country to create it", file=sys.stderr)
                        exit_code = 1
                        continue
                    rec.update({
                        "name": name,
                        "sector": args.sector,
                        "country": args.country,
                        "sources": [{"type": "ats-api", "ref": "resolve", "seen_on": today}],
                        "updated_on": today,
                    })
                try:
                    action, rid, dest = db.upsert_record("company", rec)
                    print(f"  -> {action} {rid}", file=sys.stderr)
                except ValueError as e:
                    print(f"  -> ERROR: {e}", file=sys.stderr)
                    exit_code = 1

        print(f"# {found}/{len(names)} names resolved to a live board", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
