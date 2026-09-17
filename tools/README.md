# tools/

Command-line tools that read and write `db/`. Python 3.9+, standard library only,
cross-platform (macOS/Linux/Windows). Every path is computed from `__file__`, so
each tool runs correctly from any current directory.

## db.py

The shared database layer. Every other tool and every agent writes to `db/`
through this module, never by hand, so all clones of the kit keep the same
format and vocabulary. See [`db/README.md`](../db/README.md) for the schemas.

```bash
python3 tools/db.py validate                 # check every file against db/vocab.json
python3 tools/db.py fmt                      # rewrite every file in canonical form
python3 tools/db.py stats                    # counts per dataset and per sector
python3 tools/db.py find <text>              # search companies, postings, job titles
python3 tools/db.py upsert <dataset> '<json>'
python3 tools/db.py pii-scan [files...]      # look for personal data
python3 tools/db.py id company "Name"        # print the canonical id for a name
```

For other tools written in Python, `import db` (after adding this directory to
`sys.path`) gives programmatic access without shelling back out to the CLI:

- `db.read(path)`, `db.files_of(dataset)`, `db.company_index()`
- `db.slug(text)`, `db.posting_id(url)`
- `db.upsert_record(dataset, rec_dict)` -- the in-process twin of
  `db.py upsert`. Validates, merges by id with the existing record, writes,
  and returns `(action, id, dest_path)` where action is `"added"` or
  `"updated"`. Raises `ValueError` (message = the validation/PII errors) and
  writes nothing on failure. This is what `resolve.py` and `sweep.py` use to
  write into `db/`; the CLI's `cmd_upsert` is now a thin wrapper around it, so
  behaviour is unchanged.

## ats.py

Seven ATS connectors, shared by `resolve.py` and `sweep.py`: `ashby`,
`greenhouse`, `lever`, `personio`, `recruitee`, `smartrecruiters`, `workable`
(ids match `db/vocab.json`'s `ats` keys exactly). Each `ats.FN[provider](slug)`
returns a list of `{title, location, url}` dicts.

Raises `ats.BoardError` when a board does not exist or does not answer at all
(wrong slug, moved ATS, network error, HTTP error). Returns `[]`, not an
error, when a board answers but currently lists zero postings -- a live empty
board and a dead board must never be reported the same way, or a whole slice
of the watch list can go stale without anyone noticing.

Two lessons baked in, both paid for the hard way in an earlier version:

- **Ashby rate-limits fast.** A burst of concurrent requests from a 16-thread
  pool gets HTTP 429 back almost immediately. `ats.py` backs off
  exponentially on 429 and caps simultaneous Ashby requests at 4 regardless
  of the caller's pool size. Without this, a rate-limit looks exactly like a
  dozen boards dying at once.
- **A parseable-but-empty response is not a dead board.** `personio` used to
  raise on an empty result; fixed so an empty `<position>` list returns `[]`.

## resolve.py

```bash
python3 tools/resolve.py names.txt
python3 tools/resolve.py names.txt --sector software-saas --country BE --write
python3 tools/resolve.py --recheck-dead --write
```

Turns company names into verified `(provider, slug)` pairs by probing a
handful of spelling variants against all seven ATS, instead of guessing.
Prints `<provider> <slug> <n postings>` per name, flagging `(empty)` boards
that answered with zero postings -- those are real, verified matches, not
failures, and must not be dropped (an earlier bug did exactly that: any board
that came back empty was treated as "not found").

`--write` upserts into `db/companies/`: an existing company (matched by the
id `db.slug(name)` would produce) only gets its `ats` field updated; a new
company additionally needs `--sector` and `--country` to satisfy the schema,
and is refused otherwise.

`--recheck-dead` re-probes every company whose `ats.status` is `dead` using
its *stored* provider+slug (not name guessing -- the slug was already
verified once) and updates the status. Run this occasionally instead of
re-guessing dead boards from scratch.

**Run this before `sweep.py`**, not instead of it: `sweep.py` only scans
boards that are already recorded in `db/companies`, it never discovers new
ones on its own.

## sweep.py

```bash
python3 tools/sweep.py --filter junior-strategy-policy-eu
python3 tools/sweep.py --filter junior-strategy-policy-eu --sector software-saas ai-data
python3 tools/sweep.py --filter junior-strategy-policy-eu --diff --report sweep-report.md
python3 tools/sweep.py --filter junior-strategy-policy-eu --dry-run
```

Scans every company in `db/companies` that has an `ats` entry (optionally
narrowed with `--sector`/`--country`, each taking one or more values),
against a named filter from `db/search-filters/<id>.json` (`title_regex`,
`exclude_title_regex`, `location_regex`, `keep_empty_location`, all
case-insensitive Python regex). Fetches concurrently on 16 threads.

Unless `--dry-run`, it writes back to `db/`:

- each company's `ats.status` (`live`/`empty`/`dead`) and `checked_on`
- each matching posting, upserted (so `first_seen`/`last_seen` widen instead
  of resetting), classified into `family`/`seniority` by `classify.py`
- postings this same filter previously found, on a board that answered this
  run but no longer lists the URL, get `status: "closed"` (their `last_seen`
  is left as it was -- the date they were last actually confirmed, not today)
- one `sweep-run` record per run (`<date>-<filter>`)

**Dead boards are never swallowed.** They are collected and always printed to
stderr at the end, dry-run or not -- an earlier version dropped exceptions
silently and lost two thirds of a watch list over a few weeks without anyone
noticing, because a dead board and a board with no matches produced the same
output.

`--diff` only prints matches whose posting id (derived from the URL, see
`db.posting_id`) was not already in `db/` before this run, and always prints
a header line with scanned/boards/dead/matches/new counts regardless. The
diff is by URL, not by `title | location` text -- both those fields can
themselves contain the pipe character, so text-diffing is not reliable.

`--report <path>` writes the same markdown to a file in addition to stdout.

**Cadence**: every 1-2 weeks, not every session. The bottleneck in practice
is not how often boards are scanned, it is that the market for junior
generalist roles moves slowly through public ATS boards at all.

## classify.py

```bash
python3 tools/classify.py "Job title"   # prints "family seniority"
```

The keyword classifier `sweep.py` uses to fill `family`/`seniority` on a
posting. Callable standalone by an agent that wants a quick read on one
title. It is a heuristic over the title alone, not a parser of the full
posting -- treat its output as a starting point; real requirements live in
the body of the listing (see `db/README.md` on the `notes` field).

## tracker.py

```bash
python3 tools/tracker.py followups            # overdue / due today / missing a follow-up date
python3 tools/tracker.py check "Name" ...     # already known? exits 1 if any name matches
python3 tools/tracker.py lint                 # 7-column schema, ISO dates, vocab ids
```

Reads the private `workspace/tracker.md` and `workspace/tracker-archive.md`
(`--workspace <dir>` to point elsewhere). Nothing it reads ever goes to `db/`.

`check` is step 0 of any research round: it normalises case, accents and
dashes, then matches against tracker rows, archive rows,
`workspace/applications/` folder names and `db/companies`. A match means the
lead is already known and must not be presented as new.

The SessionStart hook runs `followups`, so overdue follow-ups show up at the
start of every session.

## sync.py

Pulls the main repository (`kit.json` → `upstream`) at every session start. No account
needed.

| Command | Effect |
|---|---|
| `python3 tools/sync.py` | Fast-forward to the main repo, report what changed |
| `python3 tools/sync.py --check` | Only say how many updates are available |
| `python3 tools/sync.py --quiet` | Print only when something happened (SessionStart hook) |

Your uncommitted `db/` records are saved to `workspace/.logs/sync-backup-*.jsonl`, the update
is applied, then they are merged back record by record (the fresher record wins field
conflicts). If kit files outside `db/` were edited, or the clone has its own commits, nothing
is changed and the report says why.

## contribute.py

Sends `db/` records that the main repo does not have yet, as a pull request.

| Command | Effect |
|---|---|
| `python3 tools/contribute.py --dry-run` | List what would be sent |
| `python3 tools/contribute.py` | Send now |
| `python3 tools/contribute.py --auto` | SessionEnd hook: silent, skipped if `workspace/config.json` is missing or `auto_contribute` is false |

Steps: fetch main repo, compare record by record, validate and scan each record for personal
data (`private_terms` included), rebuild branch `db-contrib/<login>` on top of the main repo in
a temporary worktree, run `db.py validate` there, push to your fork, open or update the pull
request. Commits use the GitHub noreply address. Without `gh` logged in, records are written
to `workspace/outbox/db-contribution.jsonl` and sent at the first run after connecting.
Logs: `workspace/.logs/contribute.log`, `workspace/.logs/last-contribution.json`.

## approve_send.py

`python3 tools/approve_send.py "<what, to whom>"` records the user's yes for one final send
in the current turn. The `send-guard.sh` hook requires it before browser clicks that send,
submit or apply, and erases it at the user's next message.

## init.py

`python3 tools/init.py` creates `workspace/` from `templates/` without overwriting.
`--status` prints the workspace state as JSON for the SessionStart hook.
