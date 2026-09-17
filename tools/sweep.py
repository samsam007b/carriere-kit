#!/usr/bin/env python3
"""Sweep the ATS boards already in db/ against a named search filter.

Boards come from db/companies (any company with an `ats` entry, optionally
narrowed by --sector/--country), the filter from db/search-filters/<id>.json.
Fetches all boards concurrently, applies the filter's regexes, and unless
--dry-run writes the result back into db/: each company's ats.status and
checked_on, each matching posting (upserted, so first_seen/last_seen widen
instead of reset), a sweep-run record, and closes postings this filter had
previously found on a board that answered this run but no longer lists them.

Two lessons carried over from an earlier version of this tool, because both
were paid for the hard way:

- A dead board must never be swallowed silently. A board can go quiet for
  months without anyone noticing if the tool just skips it and moves on --
  that happened once already (rate-limiting mistaken for 12 boards going
  dead at once, see ats.py). Dead boards are collected and always printed
  on stderr at the end, never dropped.
- --diff must compare by posting URL/id, not by "title | location" text.
  Both of those fields can themselves contain the pipe character (a title
  like "Marketing Ops Manager | GTM Engineer", a multi-office location
  list), which makes naive text diffing silently wrong.

Usage:
  python3 tools/sweep.py --filter junior-strategy-policy-eu
  python3 tools/sweep.py --filter junior-strategy-policy-eu --sector software-saas ai-data --dry-run
  python3 tools/sweep.py --filter junior-strategy-policy-eu --diff --report sweep-report.md
"""
import argparse
import concurrent.futures as cf
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ats
import classify
import db

THREADS = 16


def load_filter(filter_id):
    path = os.path.join(db.DB, "search-filters", f"{filter_id}.json")
    recs = db.read(path)
    if not recs:
        raise SystemExit(f"no such filter: db/search-filters/{filter_id}.json")
    return recs[0]


def boards(sectors, countries):
    """Companies with an ats entry, optionally narrowed by sector/country.
    Returns [(company_id, provider, slug)].
    """
    out = []
    for company_id, rec in db.company_index().items():
        entry = rec.get("ats")
        if not entry:
            continue
        if sectors and rec.get("sector") not in sectors:
            continue
        if countries and rec.get("country") not in countries:
            continue
        out.append((company_id, entry["provider"], entry["slug"]))
    return sorted(out)


def fetch_all(board_list):
    """Fetch every board concurrently. Returns (results, dead) where results
    is {company_id: [posting dict, ...]} for boards that answered (live or
    empty) and dead is [(company_id, provider, slug, error message)].
    """
    results, dead = {}, []

    def fetch(job):
        company_id, provider, slug = job
        try:
            return company_id, ats.FN[provider](slug), None
        except Exception as e:
            return company_id, None, f"{type(e).__name__}: {str(e)[:80]}"

    with cf.ThreadPoolExecutor(THREADS) as ex:
        for company_id, postings, err in ex.map(fetch, board_list):
            if err is not None:
                provider, slug = next((p, s) for c, p, s in board_list if c == company_id)
                dead.append((company_id, provider, slug, err))
            else:
                results[company_id] = postings
    return results, dead


def matches_filter(posting, filt):
    title, location = posting["title"], posting.get("location") or ""
    if not re.search(filt["title_regex"], title, re.I):
        return False
    if filt.get("exclude_title_regex") and re.search(filt["exclude_title_regex"], title, re.I):
        return False
    if location:
        return bool(re.search(filt["location_regex"], location, re.I))
    return bool(filt.get("keep_empty_location"))


def existing_posting_ids():
    """Every posting id currently on disk, read once up front so --diff has a
    stable "before this run" reference regardless of what this run writes.
    """
    return {r["id"] for p in db.files_of("posting") for r in db.read(p)}


def main(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--filter", required=True, help="filter id, matches db/search-filters/<id>.json")
    p.add_argument("--sector", nargs="+", help="limit to these vocab.sectors ids")
    p.add_argument("--country", nargs="+", help="limit to these country codes")
    p.add_argument("--diff", action="store_true", help="only print matches whose posting id was not already in db/")
    p.add_argument("--dry-run", action="store_true", help="fetch and match, but write nothing to db/")
    p.add_argument("--report", help="also write the markdown output to this path")
    args = p.parse_args(argv[1:])

    filt = load_filter(args.filter)
    board_list = boards(set(args.sector or []), set(args.country or []))
    if not board_list:
        print("# no boards match --sector/--country in db/companies", file=sys.stderr)

    before_ids = existing_posting_ids()
    results, dead = fetch_all(board_list)

    company_names = db.company_index()
    today = datetime.date.today().isoformat()

    matches = []  # (company_id, posting dict, family, seniority)
    seen_urls_per_company = {}
    for company_id, postings in results.items():
        urls = set()
        for posting in postings:
            if not posting.get("url"):
                continue
            urls.add(posting["url"])
            if matches_filter(posting, filt):
                family, seniority = classify.classify(posting["title"])
                matches.append((company_id, posting, family, seniority))
        seen_urls_per_company[company_id] = urls

    new_matches = [m for m in matches if db.posting_id(m[1]["url"]) not in before_ids]
    shown = new_matches if args.diff else matches

    lines = []
    header = (f"### scanned {sum(len(v) for v in results.values())} postings on {len(results)} boards "
              f"({len(dead)} dead), {len(matches)} matches, {len(new_matches)} new")
    lines.append(header)
    lines.append("")
    for company_id, posting, family, seniority in sorted(shown, key=lambda m: (company_names.get(m[0], {}).get("name", m[0]), m[1]["title"])):
        name = company_names.get(company_id, {}).get("name", company_id)
        lines.append(f"- [{name}] {posting['title']} | {posting.get('location') or ''}")
        lines.append(f"  {posting['url']}")
    if args.diff and not new_matches:
        lines.append("No new matches.")
    output = "\n".join(lines)
    print(output)
    if args.report:
        with open(args.report, "w", encoding="utf-8", newline="\n") as f:
            f.write(output + "\n")

    # Dead boards are never swallowed: always printed, dry-run or not.
    if dead:
        print(f"\n### {len(dead)} boards dead, re-check with resolve.py --recheck-dead", file=sys.stderr)
        for company_id, provider, slug, err in sorted(dead):
            print(f"{provider:16}{slug:24}{company_id:24}{err}", file=sys.stderr)

    if args.dry_run:
        print("\n(--dry-run: nothing written to db/)", file=sys.stderr)
        return 0

    # Write back: board status, matched postings, closed postings, sweep-run.
    write_errors = 0
    for company_id, provider, slug in board_list:
        if company_id in dead_ids(dead):
            status = "dead"
        else:
            status = "live" if results.get(company_id) else "empty"
        rec = {"id": company_id, "ats": {"provider": provider, "slug": slug, "status": status, "checked_on": today}}
        try:
            db.upsert_record("company", rec)
        except ValueError as e:
            print(f"ERROR updating company {company_id}: {e}", file=sys.stderr)
            write_errors += 1

    for company_id, posting, family, seniority in matches:
        rec = {
            "company_id": company_id,
            "title": posting["title"],
            "family": family,
            "seniority": seniority,
            "location": posting.get("location") or None,
            "url": posting["url"],
            "status": "open",
            "evidence": {"source": "ats-api", "verified_on": today},
            "first_seen": today,
            "last_seen": today,
            "found_by": args.filter,
        }
        rec = {k: v for k, v in rec.items() if v is not None}
        try:
            db.upsert_record("posting", rec)
        except ValueError as e:
            print(f"ERROR upserting posting {posting['url']}: {e}", file=sys.stderr)
            write_errors += 1

    # Close postings this filter previously found on a board that answered
    # this run, but whose URL is no longer listed.
    matched_urls_by_company = {}
    for company_id, posting, _, _ in matches:
        matched_urls_by_company.setdefault(company_id, set()).add(posting["url"])
    for path in db.files_of("posting"):
        for rec in db.read(path):
            if rec.get("found_by") != args.filter or rec.get("status") == "closed":
                continue
            company_id = rec.get("company_id")
            if company_id not in results:
                continue  # board did not answer this run, don't guess
            if rec["url"] not in matched_urls_by_company.get(company_id, set()):
                try:
                    db.upsert_record("posting", {"id": rec["id"], "status": "closed"})
                except ValueError as e:
                    print(f"ERROR closing posting {rec['id']}: {e}", file=sys.stderr)
                    write_errors += 1

    sweep_run = {
        "id": f"{today}-{args.filter}",
        "date": today,
        "filter": args.filter,
        "boards_total": len(board_list),
        "boards_dead": len(dead),
        "postings_scanned": sum(len(v) for v in results.values()),
        "matches": len(matches),
        "new_matches": len(new_matches),
    }
    try:
        db.upsert_record("sweep-run", sweep_run)
    except ValueError as e:
        print(f"ERROR writing sweep-run: {e}", file=sys.stderr)
        write_errors += 1

    return 1 if write_errors else 0


def dead_ids(dead):
    return {d[0] for d in dead}


if __name__ == "__main__":
    sys.exit(main(sys.argv))
