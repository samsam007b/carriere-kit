---
name: connect-github
description: Connect this machine to GitHub so database contributions are sent as pull requests. Installs and logs in the GitHub CLI, guides account creation if needed, then flushes the local outbox. Use when contribute.py says GitHub is not connected, when setting up a new machine, or when the user asks about GitHub, pull requests or sharing.
---

# connect-github

Explain first, in 3 lines: receiving the shared database needs nothing; sending your
objective findings back needs a free GitHub account and the GitHub CLI (`gh`); it takes about
2 minutes and nothing personal is sent. Without it, findings wait in `workspace/outbox/`.

## 1. Check

```bash
gh --version; gh auth status
```

## 2. Install gh if missing (announce the command before running it)

| OS | Command |
|---|---|
| macOS | `brew install gh` (if brew is missing, point to https://cli.github.com) |
| Windows | `winget install --id GitHub.cli` |
| Debian / Ubuntu | see https://github.com/cli/cli/blob/trunk/docs/install_linux.md |

## 3. Account

Ask: "Do you have a GitHub account?" If not, offer to open https://github.com/signup in the
browser (skill `browser`) and walk them through it. **They type their email, password and
solve the captcha themselves**; you wait and continue when they say done.

## 4. Log in

`gh auth login` is interactive, so the user runs it in this Claude Code prompt with the `!`
prefix:

```
! gh auth login --hostname github.com --git-protocol https --web
```

Tell them: copy the one-time code shown, press Enter, paste it in the browser page, approve.
Then verify with `gh auth status`.

## 5. Flush and confirm

```bash
python3 tools/contribute.py --dry-run
python3 tools/contribute.py
```

Show the pull request link. Say three things plainly, before the first send rather than
after: a fork of the kit is created automatically under their account (a public repository
they own, deletable at any time, recreated at the next send); their pull request is read by
the repository owner and merged by them, never automatically; later contributions happen by
themselves at session end, and `"auto_contribute": false` in `workspace/config.json` turns
that off.
