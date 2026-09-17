---
name: status
description: Give a state-of-the-search overview. Use when the user asks "what's the state of my search", "where do things stand", "give me a status", or wants a summary across all active leads.
---

# Status

A one-screen answer to "where do I stand", not a re-read of every case file.

## 1. Gather

- `python3 tools/tracker.py lint` first: fix any schema errors before reporting numbers
  built on a broken file.
- `python3 tools/tracker.py followups` for what's due, overdue, or missing a date.
- Read `workspace/tracker.md` for the full active list: counts by Status (`todo`, `active`,
  `waiting`, `offer`, `parked`), and by Type.
- Read `workspace/calendar.md` for upcoming deadlines that aren't tracker follow-ups
  (admin dates, event windows).

## 2. Present as a table

One table, leads as rows, columns close to the tracker's own (Lead, Type, Status, next
action or date). Put anything overdue or due soon at the top. Keep it to what fits on one
screen; point to `workspace/tracker.md` for the full history rather than dumping every row's
`Last action` text.

## 3. Do not editorialize on strategy uninvited

If several leads look stalled or the user's positioning seems scattered across
incompatible tracks, name it in one line and point to
[method/07-long-term-strategy.md](../../method/07-long-term-strategy.md) and
`workspace/positioning.md`, rather than launching into a strategy review they didn't ask for.

## 4. Propose the next step

End with one concrete suggestion: the most overdue follow-up, or the lead closest to a
decision point.
