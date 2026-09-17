---
name: sweep
description: Scan every known ATS job board in the shared database for postings matching a search filter, report what is new since the last run, and record matches. Use for "find me jobs", "what's open", "new postings", "run a sweep", or to refresh a sector.
---

# sweep

Announce in 2 lines: you will query the public job boards of the companies already in the
database (Lever, Greenhouse, Ashby, SmartRecruiters, Recruitee, Workable, Personio), keep the
postings matching a filter, and show only what is new. No login, nothing sent.

## 1. Choose or build the filter

```bash
ls db/search-filters/
python3 tools/db.py stats
```

- Show the existing filters in a table (id, description) and propose the closest to the
  user's targets from `workspace/profile.md`.
- None fits: build one with the user (titles regex from `db/job-titles.jsonl` for their
  families and seniority, exclude regex for traps like "senior|head of", locations regex),
  then save it with `python3 tools/db.py upsert filter '<json>'`. Filters are shared: keep
  them generic (no name, no personal wording).

## 2. Run

```bash
python3 tools/sweep.py --filter <id> --diff [--sector <sector>] [--country <CC>]
```

`--dry-run` to test without writing. Sweeping all boards takes a few minutes: run it in the
background and tell the user.

The tool writes matched postings (status `unverified` until checked), closes postings that
vanished from a board that still answers, updates board status, and appends a `sweep-run`.

## 3. Triage (method/01-research-and-sources.md)

1. `python3 tools/tracker.py check "<company>" ...` on the new matches: known leads are
   marked, not presented as new.
2. For the promising ones, read the full posting (skill `browser` if the page is JavaScript)
   and record gates in the posting record (`requirements`), `status: open`,
   `evidence.verified_on` today.
3. Apply the user's gates. Uncertain gate stays with "to verify".

## 4. Present

One table, most relevant first:

| # | Company | Title | Seniority | Location | Gates vs profile | Deadline | Link |

Then ask which ones to open (`new-application`) and whether to broaden (more boards with
`sector-scan`, other filters). Never apply on your own.

## Growing coverage

A sweep only sees companies whose board is known. To add companies:
`python3 tools/resolve.py names.txt --sector <s> --country <CC> --write` detects their ATS
board and records it. Dead boards are rechecked with `--recheck-dead`.
