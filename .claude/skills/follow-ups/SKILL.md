---
name: follow-ups
description: Check what follow-ups are due, overdue, or missing a date. Use when the user asks "what's due", "any follow-ups", "who do I need to chase", or at the start of a session when the tracker has waiting rows.
---

# Follow-ups

## 1. Run the tool

`python3 tools/tracker.py followups` from the repo root. It reads `workspace/tracker.md` and
prints three blocks: overdue, due today, and rows stuck at status `waiting` with no
Follow-up date set.

## 2. Present it as one table or list, not a wall of text

Group by the three blocks the tool already gives you. For each overdue or due-today lead,
name the company and how many days overdue.

## 3. For a row missing a date

That row is a schema gap, not a task. Ask the user for the missing date (or compute one from
[method/03-follow-up-and-gates.md](../../method/03-follow-up-and-gates.md)'s cadence table:
10 to 14 days for an application, 7 for cold outreach, 5 to 7 for a warm intro) and update the
row. Run `python3 tools/tracker.py lint` after editing to confirm the fix.

## 4. Before drafting any follow-up message

Re-verify the posting or the thread is still relevant: per
[method/01-research-and-sources.md](../../method/01-research-and-sources.md), a lead waiting
more than 2 to 3 weeks should be re-checked at the source, the posting may have closed or been
filled without notice.

Draft short, per [method/02-outreach-email.md](../../method/02-outreach-email.md): no new
attachment, no new argument, no comment on the silence. Show the full text and get an explicit
send confirmation in the current turn before anything goes out.

## 5. Propose the next step

After presenting the due list, ask which lead to act on first, or offer to draft the
follow-up for the most overdue one.
