# Research and sources

## Database first

Before any web search: `python3 tools/db.py find <name or keyword>` and
`python3 tools/db.py stats`. Someone else's clone of this kit may already have scanned that
company, that sector, or that ATS board. Reusing that work is the entire point of `db/` being
shared. Only search the web for what the database does not already answer.

## No duplicates, ever

Before presenting or deep-diving any lead: `python3 tools/tracker.py check "Name" "Other
Name" ...`. It searches `workspace/tracker.md`, `workspace/tracker-archive.md`,
`workspace/applications/` folder names, and company records in `db/companies/*.jsonl`, after
normalizing case, accents and punctuation. Exit code 1 means at least one name is already
known: treat it as known, don't re-present it as new, unless something material changed (a
posting reopened, a status update needs verifying).

When you brief a `researcher` subagent for a wider search, hand it the list of names already
known (from `tracker.py check` or a quick scan of the tracker) as "already known, exclude
these." Filter at the source, not only after the fact on the consolidated result.

## Two-phase research

1. A `researcher` (or `doc-reader`) subagent, on Haiku, returns a summary under 400 tokens
   plus a short "worth a deep dive" table.
2. You deep-dive 1 to 3 of the most promising entries yourself.

Never ask Haiku to write or edit a document, draft an email, or produce anything that goes to
a third party; a hook blocks it. Research only.

## Verify at the source, never an aggregator alone

A posting counts as **open** only when confirmed on the company's own careers page, its ATS
board, or LinkedIn Jobs, on the day you check. A third-party aggregator (a generic job board,
a re-post site) is never enough by itself: it can carry a fabricated or stale deadline on a
posting that has been closed for years at the source.

If a fetch only returns a title (a JavaScript-rendered page, an ATS board loaded inside an
iframe like Ashby or Greenhouse), that is not evidence the posting doesn't exist. Switch to a
real browser (a Playwright-driven session, not a raw HTML fetch) before concluding anything.

Every lead added to `db/` or `workspace/tracker.md` carries what was actually verified: a
direct link plus what you read there, not a job title copied from a summary.

A lead marked "waiting" for more than 2 to 3 weeks gets re-verified at the source before any
follow-up: the posting may have been filled or pulled since you applied.

## Read the full posting

Gates hide in the body, not the title: minimum years of experience, a specific degree, a
language requirement, an on-site constraint. Read the whole posting before calling a lead
solid, never rely on the title alone. This is the check that catches a "junior" title sitting
over a five-year experience requirement.

## The ghost-job checklist

Before investing real time in a posting, check for the pattern (external benchmark: roughly a
quarter of postings on major boards show these signs):

- Live for more than 30 days with no sign of movement.
- Absent from the company's own careers page even though it's live on an aggregator.
- No salary range where the market or the regulation would normally require one.
- Generic description with no real detail about the team, the tools, or the actual work.

Any two of these together mark a posting as suspect. Verify harder (call, LinkedIn activity on
the recruiter's profile, a direct email) before building a full case file around it.

## Agents can invent plausible detail

A delegated research pass can produce deadlines, headcounts, and links that don't hold up at
the source. Anything pulled from an automated search and destined for an email or a case file
gets re-verified at the primary source first. A false fact cited to a recruiter who knows
their own company costs more than a shorter, less impressive email.
