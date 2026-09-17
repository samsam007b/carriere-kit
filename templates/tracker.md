# Tracker: active leads

> One row per active lead. A lead only spotted, not yet acted on, still gets a row here with
> `Type: lead` and `Status: todo`; a full sector sweep with many candidates belongs in `db/`,
> not as individual rows. When a lead closes, move its row to `workspace/tracker-archive.md`
> rather than deleting it.
>
> Before adding any row: `python3 tools/tracker.py check "Name"` first. See
> [`method/01-research-and-sources.md`](../method/01-research-and-sources.md).

| Lead | Type | Status | Submitted | Follow-up | Last action | Source |
|---|---|---|---|---|---|---|
| {{Organisation or contact name}} | {{application \| outreach \| lead \| research-round \| project}} | {{todo \| active \| waiting \| offer \| parked \| closed \| rejected}} | {{YYYY-MM-DD or —}} | {{YYYY-MM-DD, required when Status is waiting}} | {{one line, dated}} | {{direct link}} |

## Legend

- **Type**: one of `db/vocab.json`'s `pipeline_types`: `application` (formal, submitted through
  a portal or email), `outreach` (message to a named contact), `lead` (spotted, nothing sent
  yet), `research-round` (a search session with its own result table), `project` (side project,
  exam, programme).
- **Status**: one of `db/vocab.json`'s `pipeline_status`: `todo`, `active` (in progress,
  interviews or conversation), `waiting` (sent, needs a `Follow-up` date), `offer`, `parked`
  (paused on purpose), `closed` (accepted, withdrawn, or no answer after follow-ups),
  `rejected`.
- **Submitted / Follow-up**: `YYYY-MM-DD`, always. A `waiting` row with no `Follow-up` date is
  invalid; `tools/tracker.py lint` flags it, and a hook may block writing it in the first place
  depending on how this kit was set up.
- **Last action**: a short, dated line. Enough to reconstruct what happened without opening the
  application's case file.
- **Source**: a direct link, not a description. If the lead came from `db/companies/` or
  `db/postings/`, link the record id instead.

Run `python3 tools/tracker.py followups` regularly to see what's overdue, due today, or missing
a follow-up date. Run `python3 tools/tracker.py lint` before trusting this file after a manual
edit.
