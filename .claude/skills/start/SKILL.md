---
name: start
description: Onboarding and home menu of the career kit. Use at the first session on a machine (no workspace/ or empty profile), when the user says hello, asks "what can you do", "how does this work", "where do I start", or seems lost.
---

# start

The person may never have used Claude Code, a terminal or this repo. Your job: make them
understand in one minute what they can get, show it working, and let them choose.

## 1. Detect the situation (silently)

```bash
python3 tools/init.py --status
```

| State | Go to |
|---|---|
| `"workspace": false` | 2 then 3 |
| profile not filled | 3 (skip the long pitch if they already saw it) |
| profile filled | 4 |

## 2. Language and pitch (first session only)

Answer in the language the user writes in. Then, in **at most 8 lines**:

- What this is: a career copilot that knows their profile, searches and verifies job
  opportunities at the source, prepares applications and interviews, and never sends
  anything without their yes.
- What makes it different: a shared database of companies, ATS boards, job titles and
  market notes that grows with every user (they receive it, and their own objective
  findings are shared back, never their personal data).
- One sentence on privacy: everything about them stays in `workspace/` on this machine.

Then create the workspace, announcing it in one line:

```bash
python3 tools/init.py
```

Write their language into `workspace/config.json` → `language` (ISO code).

## 3. Show, then offer the menu

Propose right away a **30-second live demo in a real browser** (skill `browser`): open a
company careers page from the database and show how you read a posting. Say you can do
the same for forms and portals, and that they keep control of logins, captchas and the
final send. If they say no, move on without insisting.

Then the menu (numbered, short, they can answer with a number):

| # | Option | Skill |
|---|---|---|
| 1 | Let me get to know you (15 min interview, or drop your CV / LinkedIn PDF) | `profile` |
| 2 | Find opportunities in a sector or a list of companies | `sweep`, `sector-scan` |
| 3 | Work on a specific posting you already have | `new-application` |
| 4 | Prepare an interview | `interview-prep` |
| 5 | See what the shared database already knows | `kit-help` |
| 6 | Set up this machine (GitHub, browser, recommended Claude Code settings) | `connect-github`, `browser` |

Recommend 1 first when the profile is empty: everything else depends on it.

Also mention, in one line each, when relevant:
- **Auto contribution**: at session end, new objective database records are sent as a pull
  request. Off switch: `"auto_contribute": false` in `workspace/config.json`. Needs a free
  GitHub account; without one, records wait in `workspace/outbox/`.
- **Models**: planning uses Opus in Plan Mode (Shift+Tab), writing uses Sonnet, web
  research uses Haiku subagents. Nothing to configure.

## 4. Returning user

One line greeting, then what the session-start briefing flagged (overdue follow-ups,
database updates received, contribution sent), then: "What do we do today?" with the 3
most relevant menu options for their current pipeline (read `workspace/tracker.md`).

## Deep dives on demand

If they ask how something works, answer in 3 to 6 lines and point to the file:
method in `method/`, database in `db/README.md`, contributing in `CONTRIBUTING.md`,
safety in `CLAUDE.md` section 7. Do not recite files they did not ask about.
