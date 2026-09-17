---
name: browser
description: Drive a real, visible browser with Playwright to show the user what you do - read job postings behind JavaScript or ATS iframes, explore careers portals, fill application forms and draft emails in webmail, while the user handles logins, captchas and approves every final send. Use proactively whenever a web page matters, when WebFetch returns only a title, for any application portal or webmail, and to demo the kit.
---

# browser

The browser is the kit's most convincing feature: the user **sees** you work. Be proactive.

## Always offer it

- When a posting, careers page or portal is involved: "Want me to open it in the browser so
  you can watch?" If the user already agreed once in this session, just open it.
- When WebFetch returns only a title or an empty body: switch to the browser. Never conclude
  that a posting does not exist from a failed fetch.
- For new users: offer a 30-second demo (below).

## Setup check (first use on a machine)

The Playwright MCP server is declared in `.mcp.json` and needs Node.js.

1. If `mcp__playwright__*` tools are available, go.
2. If not: check `node --version`. Missing → point to https://nodejs.org (LTS) and ask the
   user to restart Claude Code after installing. Present but tools missing → ask the user to
   run `/mcp` and enable `playwright`, or restart Claude Code in this folder.
3. First navigation may download a browser: say so ("one-time download, about a minute").

## Demo (30 seconds)

1. Pick a company with an `ats` board in the database (`python3 tools/db.py find ...`) or a
   careers page the user names.
2. `browser_navigate` to it, narrate in one line what they see.
3. Open one posting, extract with `browser_evaluate(() => document.body.innerText)` the
   gates (experience, languages, degree, location, salary, deadline) and show them as a table.
4. Explain in 3 lines what else you can do: fill forms, prepare an email in their webmail,
   keep evidence (screenshot) of what the posting said on that day.

## Working rules

| Moment | What you do |
|---|---|
| Login page, 2FA, captcha, cookie wall asking for consent choices | Stop. Say exactly what is needed ("please log in to X in the browser window, tell me when done"). Never type the user's password, never try to solve a captcha |
| Reading | Prefer `browser_snapshot` or `innerText` over screenshots (cheaper). Screenshot when the user should see layout or as evidence |
| Forms | Fill field by field from `workspace/profile.md` and `facts.md` only. Unknown answer → ask, never guess. Upload files only from `workspace/applications/<slug>/` |
| Before the final click (send, submit, apply, post) | Take a screenshot, show the full text, recipient or portal, attachments, and ask "Send it? (yes / change)". Wait |
| After the user's yes | Run `python3 tools/approve_send.py "<what, to whom>"`, then click. Confirm with a screenshot of the confirmation page and update `workspace/tracker.md` (Submitted date, Follow-up date) |
| Objective discovery (ATS provider, posting gates, deadline) | Record it in `db/` via `tools/db.py upsert` |

The send guard hook blocks final-send clicks without that same-turn approval. If it blocks
you, it means you skipped the confirmation: ask the user, do not work around it.

## Email through webmail

Draft in the webmail compose window (recipient, subject, body, attachment), show the
screenshot and the full text in chat, wait for the yes, approve, send. Scheduling ("send
tomorrow 9:00") uses the webmail's own schedule feature, with the same confirmation.
