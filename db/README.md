# Shared database

This folder is the part of the kit that grows with every person who uses it. Each
contribution lands in the main repository through a pull request (see
[CONTRIBUTING.md](../CONTRIBUTING.md)), so everyone's next search starts from
everything the others already found.

Two rules make that possible:

1. **One vocabulary.** Every id (sector, job family, seniority, ATS, status) comes from
   [vocab.json](vocab.json). Nothing else is accepted.
2. **One writer.** Records are written with `python3 tools/db.py upsert ...`, never by
   hand. The tool validates, merges by id, sorts and scans for personal data.

Run `python3 tools/db.py validate` after any change. CI runs the same command on every
pull request.

## What is in it

| Path | Dataset | One record is |
|---|---|---|
| `companies/<sector>.jsonl` | `company` | An employer, filed under its primary sector |
| `postings/<sector>.jsonl` | `posting` | A job posting seen at a date, with its evidence |
| `job-titles.jsonl` | `job-title` | A real-world title, its family, typical seniority, markets, traps |
| `search-filters/<id>.json` | `filter` | A named set of regexes used by `tools/sweep.py` |
| `sweep-runs.jsonl` | `sweep-run` | One execution of a sweep: boards scanned, dead, matches |
| `sources.jsonl` | `source` | A place companies were collected from (member directory, ATS registry) and the method used |
| `market-notes.jsonl` | `market-note` | A dated, sourced fact about a market (visa threshold, language expectation, recurring trap) |

Formats: JSON Lines, one object per line, keys sorted, lines sorted by `id`, UTF-8.
This keeps diffs small and lets two people add records to the same file without a
merge conflict.

## Schemas

Required fields are in **bold**. Dates are `YYYY-MM-DD`. Countries are ISO 3166-1
alpha-2 (`BE`, `FR`), or `EU` / `WW` for Europe-wide / worldwide.

### company

| Field | Type | Notes |
|---|---|---|
| **id** | kebab-case | `python3 tools/db.py id company "Name"` gives it |
| **name** | string | Official name |
| **sector** | vocab `sectors` | Primary sector, decides the file |
| sectors_secondary | list of vocab `sectors` | |
| **country** | ISO code | Headquarters or the entity that hires |
| city | string | |
| website, careers_url | URL | `careers_url` is the official careers page |
| ats | `{provider, slug, status, checked_on}` | provider from vocab `ats`, status from `board_status` |
| size | `1-10` … `5000+` | Headcount band |
| tags | list of kebab-case | Free labels, e.g. `graduate-programme`, `eu-office` |
| **sources** | list of `{type, ref, seen_on}` | type from vocab `evidence_source`, ref such as `agoria:energy` |
| notes | string ≤ 500 | Objective facts only |
| **updated_on** | date | |

### posting

| Field | Type | Notes |
|---|---|---|
| **id** | `p-` + 12 hex | Derived from the URL, `upsert` fills it |
| **company_id** | company id | Must exist |
| **title** | string | Verbatim |
| **family** | vocab `job_families` | |
| **seniority** | vocab `seniority` | From the body of the posting, not only the title |
| location, country, remote | | |
| **url** | URL | Primary source if possible |
| **status** | vocab `posting_status` | `open` only when confirmed on the official source |
| **evidence** | `{source, verified_on, ref?}` | source from vocab `evidence_source` |
| **first_seen**, **last_seen** | date | `upsert` keeps the earliest and the latest |
| requirements | `{experience_years_min, languages:[{lang, level}], degree, other:[...]}` | Gates read in the full posting |
| salary | `{min, max, currency, period}` | Only when published |
| deadline | date | |
| found_by | filter id | Which search filter surfaced it |
| notes | string ≤ 500 | Objective, e.g. "title says junior, body asks 3 years" |

### job-title

`{id, title, lang, family, seniority_typical: [...], markets: [...], aliases: [...], notes}`.
One record per title per language. Aliases hold spelling variants.

### filter

`{id, description, title_regex, exclude_title_regex?, location_regex, keep_empty_location?, families?, seniority?, updated_on}`.
Regexes are Python syntax and case-insensitive.

### sweep-run

`{id: "<date>-<filter>", date, filter, boards_total, boards_dead, postings_scanned, matches, new_matches?}`.

### source

`{id, name, type, url?, country?, sectors: [...], coverage?: {...}, method, last_run?}`.
`method` explains how to redo the collection, so the next person can extend it.

### market-note

`{id, scope, topic, note, source_url?, verified_on}`. `scope` is a country code with an
optional city, such as `GB-London`.

## What never goes in db/

The database is public and impersonal. `upsert`, `validate` and CI all refuse:

- names, emails, phone numbers or profile links of people
- first person wording ("my", "je", "mijn") or fit judgements ("good for my profile")
- application status, scores, preferences: those live in `workspace/`, which is never pushed
- any term listed in `workspace/config.json` → `private_terms` (your name, city, school)

If a fact is only true for you, it belongs in `workspace/`. If it is true for anyone
looking at that company or that market, it belongs here.
