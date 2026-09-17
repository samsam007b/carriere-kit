# Overview: how the system works

## The two zones

| Zone | Content | Git |
|---|---|---|
| `workspace/` | Your profile, facts, tracker, applications, preferences, judgement calls | Ignored, never pushed |
| `db/` | Objective, impersonal facts about companies, postings and markets | Shared, goes through pull requests |

Full rules for each zone: `CLAUDE.md` sections 2 and 3. This file is about the workflow that
runs on top of them.

## The files that carry the work

| File | Holds | Granularity |
|---|---|---|
| `workspace/tracker.md` | Active leads only | One row per lead: type, status, dates, last action |
| `workspace/tracker-archive.md` | Closed or dropped leads | Same schema, kept for grep, not re-read |
| `workspace/calendar.md` | Dates only | One row per deadline, chronological |
| `workspace/applications/<slug>/` | Full case file per serious lead | Posting snapshot, gates, CV, letter, email, log |
| `db/companies/`, `db/postings/` | Objective company and posting data | One record per entity |

A date never lives as a source of truth in two places. `calendar.md` is authoritative for
dates; if a date changes elsewhere, propagate it there.

## The loop, step by step

### 1. Check the database and the tracker first

Before searching anything: `python3 tools/db.py find <name>` and `python3 tools/db.py stats`,
then `python3 tools/tracker.py check "Name" ...`. Someone, possibly you in a past session, may
already have scanned that company or that sector. See
[01-research-and-sources.md](01-research-and-sources.md).

### 2. Qualify

Verify at the source (never an aggregator alone), read the full posting, check it against your
gates in `workspace/profile.md`. If it fails qualification, record why and stop, don't force it
into the tracker.

### 3. Build the case file

`workspace/applications/<slug>/README.md` from `templates/application/README.md`: objective,
angle, contact, language decision, CV notes, draft email, history. This file matters more than
the CV. Months later, before an interview, it is what you reread.

### 4. Write, never send

Draft the CV, letter and email. Follow
[02-outreach-email.md](02-outreach-email.md). Show the full final text. Sending needs an
explicit "yes, send" in the same turn, every time, no matter what was agreed earlier.

### 5. Track and follow up

Add a tracker row with a follow-up date (never optional for a `waiting` row). Weekly, run
`python3 tools/tracker.py followups` and work the three blocks it returns: overdue, due today,
missing a date.

### 6. Close the loop

Whatever the outcome: update the tracker status, move the row to `tracker-archive.md` if
closed, write one line on what you learned. See
[05-career-anti-patterns.md](05-career-anti-patterns.md) for the judgement traps, and
[07-long-term-strategy.md](07-long-term-strategy.md) for how a single outcome fits the larger
picture.

## Map of the method files

| File | Covers |
|---|---|
| [01-research-and-sources.md](01-research-and-sources.md) | Finding and verifying leads |
| [02-outreach-email.md](02-outreach-email.md) | Writing a short, specific outreach email |
| [03-follow-up-and-gates.md](03-follow-up-and-gates.md) | Follow-up cadence, warm vs cold, gates table |
| [04-cv-and-ats.md](04-cv-and-ats.md) | CV structure, ATS formatting, keyword alignment |
| [05-career-anti-patterns.md](05-career-anti-patterns.md) | Career advice to distrust, and why |
| [06-interview-preparation.md](06-interview-preparation.md) | Prepping for and debriefing an interview |
| [07-long-term-strategy.md](07-long-term-strategy.md) | Vision, positioning, portfolio thinking |

## The one recurring routine

Twenty minutes, whenever you sit down with the kit, in this order:

1. `python3 tools/tracker.py followups` and clear what is due.
2. Check the inbox for bounces on anything marked `waiting`.
3. Add any new lead spotted since last time to the tracker or an application folder.
4. Decide this session's batch: a few targeted moves, not fifteen at once.

Without this, the tracker and the calendar drift apart within two weeks and the kit becomes
a graveyard of stale rows.
