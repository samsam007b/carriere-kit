---
name: new-application
description: Start a new application or outreach case file. Use when the user wants to apply to a posting, reach out to a company, or says things like "let's apply to X", "I found a posting at Y", "new lead", or names a company and a role they want to pursue.
---

# New application

Open a new lead the same way every time, so nothing gets skipped.

## 1. Dedup check (before anything else)

Run `python3 tools/tracker.py check "<company name>"` from the repo root. If it comes back
`KNOWN`, show the existing row or case file and ask whether this is a status change (posting
reopened, new contact) rather than a new lead. Do not create a second entry for the same
company without the user confirming it is genuinely a separate, new lead.

Also check the database first: `python3 tools/db.py find "<company name>"`. If a company or
posting record already exists, reuse it instead of re-researching from scratch.

## 2. Verify at the source

Per [method/01-research-and-sources.md](../../method/01-research-and-sources.md): confirm the
posting is live on the company's own careers page, its ATS board, or LinkedIn Jobs, on the
day. An aggregator listing alone is not enough. If a fetch returns only a title, switch to
the browser skill instead of concluding the posting does not exist.

Read the full posting, not just the title. Gates hide in the body.

## 3. Check gates

Compare the posting against `workspace/profile.md` → "Gates I check on every posting". A gate
that cannot be verified from the posting stays in the running, marked "to verify", it is
never a reason to drop a lead on its own.

## 4. Create the case file

Copy [templates/application/README.md](../../templates/application/README.md) to
`workspace/applications/<slug>/README.md` (slug: lowercase, hyphenated company name). Fill in
Status, Objective, Angle, Contact, Language per
[method/02-outreach-email.md](../../method/02-outreach-email.md) and
[method/03-follow-up-and-gates.md](../../method/03-follow-up-and-gates.md).

## 5. Add the tracker row

Append a row to `workspace/tracker.md` using the schema in
[templates/tracker.md](../../templates/tracker.md): Type from `pipeline_types`, Status from
`pipeline_status`, and if Status is `waiting`, a Follow-up date is required (10 to 14 days out
for an application, 7 days for cold outreach, 5 to 7 for a warm intro). Run
`python3 tools/tracker.py lint` to confirm the row is well-formed before moving on.

## 6. Propose the next step

State in 1 to 2 lines what was created and what comes next: usually drafting the outreach
email or CV (offer the `cv` skill), or, if the posting requires a portal application, opening
the browser together. Never draft and send in the same step without showing the full text
first, per [CLAUDE.md](../../CLAUDE.md) section 9.
