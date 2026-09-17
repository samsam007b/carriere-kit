---
name: sector-scan
description: Map a whole sector or ecosystem from a member directory (industry federation, chamber of commerce, cluster, accelerator portfolio, ranking) into the shared database, detect each company's hiring channel, and surface the employers worth a deep dive. Use for "which companies in X are hiring", "explore the energy sector", "scan the members of <federation>", or when sweeps return too little.
---

# sector-scan

The hidden market is in companies nobody searched yet. This skill turns a list of members
into structured, reusable knowledge for every user of the kit.

Announce in 3 lines: source you will use, what gets recorded in the shared database
(companies, ATS boards, postings), what stays private (the shortlist and fit judgements, in
`workspace/`), and roughly how long it takes.

## 1. Check what exists

```bash
python3 tools/db.py stats
grep -h '"id"' db/sources.jsonl
python3 tools/db.py find "<sector or federation>"
```

If the source was already collected (`db/sources.jsonl`), do not redo it: extend it (missing
clusters) or go straight to step 4.

## 2. Collect the member list

- Find the directory (federation site, cluster page). Open it with the `browser` skill when
  it is paginated or JavaScript.
- Extract per member: name, website, city, country, the directory's own category.
- Record the source once:
  `python3 tools/db.py upsert source '{"id":"<slug>","name":"...","type":"member-directory","url":"...","country":"..","sectors":[...],"method":"how to redo the collection step by step","last_run":"YYYY-MM-DD"}'`
- Map the directory categories to vocab `sectors` and record each company with
  `sources: [{"type":"member-directory","ref":"<source-id>:<category>","seen_on":"..."}]`.
  Large lists: write a JSONL file in the scratchpad and pipe it to `tools/db.py upsert company -`.

## 3. Detect hiring channels

```bash
python3 tools/resolve.py names.txt --sector <sector> --country <CC> --write
```

Companies without a public ATS board: note `careers_url` when found. Split the rest into
clusters of 30 to 80 and give each cluster to a `researcher` subagent with: the list, the
known names to exclude (`tools/tracker.py check`), the user's target families and gates, and
the output table format. Two-phase research: ≤ 400 tokens back, then you deep-dive 1 to 3.

## 4. Sweep and score

```bash
python3 tools/sweep.py --filter <id> --sector <sector> --diff
```

Score companies for the user in `workspace/` only (e.g. `workspace/research/<source-id>.md`):
relevance to targets, open roles, size, languages, location. Scores and "fit" never go to
`db/`.

## 5. Present

One table (top 10 to 15), with a column "why" in 1 line and a column "evidence" (URL). Then
propose: open applications, spontaneous outreach to the best employers without postings, or
a follow-up scan of the next cluster. Update the source's `coverage` in `db/sources.jsonl`
(clusters done, counts) so the next person continues where you stopped.
