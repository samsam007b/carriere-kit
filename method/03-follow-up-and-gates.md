# Follow-up cadence and gates

## Follow-up cadence

Every submission gets a follow-up date the moment it is logged, never as an afterthought.
`workspace/tracker.md`'s `Follow-up` column is not optional for a row with `Status: waiting`.

| Type | Follow-up window | Notes |
|---|---|---|
| Formal application (posted role) | 10 to 14 days after submission | Standard screening cycle in most organisations |
| Cold outreach to a named contact | 7 days after the first message | Shorter, because there's no formal process holding it |
| Warm introduction | 5 to 7 days, but check with the connector first | The connector may already be tracking it |

External benchmark worth keeping in mind: a message followed up on a regular cadence roughly
doubles the odds of a reply compared to a single send with no follow-up. Cold outreach alone
converts far less often than a warm introduction; that gap is large enough to change which
channel you try first, not just a marginal difference.

Before writing a follow-up on a `waiting` row older than 2 to 3 weeks, re-verify the posting is
still live at the source (see
[01-research-and-sources.md](01-research-and-sources.md#verify-at-the-source-never-an-aggregator-alone)).
A role can be filled or pulled between submission and follow-up with no notification back to
the candidate.

Run `python3 tools/tracker.py followups` regularly (weekly is a reasonable default) and work
through what it returns: overdue, due today, waiting with no follow-up date set.

## Warm before cold

Before any cold outreach to a company, check whether a warm path already exists: a contact
already logged in `workspace/vision.md` or `workspace/positioning.md`, a prior connection, an
alumni or community link. When both a warm and a cold path are possible for the same lead,
take the warm one. The gap in response rate between the two is too large to leave on the table.

Never send an unsolicited volume of near-identical applications through an auto-apply tool.
Templated mass-send tools convert at a small fraction of a manually qualified, individually
verified approach. This method is built around fewer, better-verified leads on purpose; a
volume approach is not a shortcut, it is a different and weaker method.

## Gates and a junior-first shortlist

Not every open role is worth a case file. Before committing real time, check the posting
against a small gates table kept in `workspace/profile.md`. A gate is a hard requirement that
disqualifies a candidate outright, not a nice-to-have.

Illustrative gate categories, to be filled with your own thresholds:

| Gate | Typical signal | Action |
|---|---|---|
| Years of experience | A minimum stated in the body, not the title | Below threshold: exclude, unless the range is described as a floor with flexibility |
| Language requirement | Native / C2 fluency required | Exclude if it exceeds your real, current level; a level you're still building isn't a lie, but don't round up |
| Degree or certification | A specific technical degree named as required | Exclude if you don't hold it and the posting doesn't accept equivalent experience |
| Location | On-site only, in a city that doesn't work for you | Exclude only for a **misleading** posting (claims remote/hybrid but the verified real location is different); a role honestly based elsewhere, including abroad, is not automatically excluded if relocating is something you're open to |
| Seniority mismatch | Title says junior, body requires senior-level scope | Exclude; this is the single most common trap, catch it by reading the full posting, not the title |

A gate that's ambiguous from the posting text stays on the shortlist marked "to verify," never
dropped out of caution alone.

### Reading level, not title

A "junior," "associate," "coordinator," or "graduate" title can sit over a senior-level
requirement in the body, and a senior-sounding title (Chief of Staff, Head of, Lead) can
sometimes be genuinely open to less experience when the posting states no floor. Judge every
posting on its actual requirements, never on the title alone.

### The final table

Once a batch of leads has been checked for duplicates, verified at the source, and passed
through the gates table, present them as a single table: one row per lead, gate status, source
link. No application gets triggered automatically from that table. The decision on what to
pursue belongs to the person running the kit, every time.

| Lead | Type | Gates | Source | Notes |
|---|---|---|---|---|
| _example only_ | _application / outreach_ | _pass / fail / to verify_ | _direct link_ | _one line_ |
