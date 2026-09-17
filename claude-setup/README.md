# Claude Code setup

Inside this repo everything is already configured by `.claude/settings.json`, `.claude/hooks/`
and `.mcp.json`. This folder is for people who want the same habits machine-wide.

## What the repo configures

| Area | Setting | Why |
|---|---|---|
| Speed | `permissions.defaultMode: bypassPermissions` | No approval prompt for every file edit or command |
| Safety net | `permissions.deny` + hooks in `.claude/hooks/` | Blocks destructive commands, force pushes, reading credentials, secrets in files, direct edits of database files, final sends without the user's yes |
| Models | `model: opusplan`, `CLAUDE_CODE_SUBAGENT_MODEL=sonnet`, Haiku agents `researcher` and `doc-reader` | Opus plans (Plan Mode), Sonnet executes, Haiku reads and searches. A hook blocks Haiku for writing |
| Browser | `.mcp.json` Playwright server, `enableAllProjectMcpServers` | A visible browser for postings, portals and webmail |
| Session briefing | `SessionStart` hook | Pulls the shared database, shows workspace state and follow-ups |
| Sharing | `SessionEnd` hook | Sends database findings as a pull request, in the background |

## If bypass mode does not start

Depending on the Claude Code version and how it is launched, bypass mode set by a project can
be ignored until it is allowed at user level. Either:

- launch with `claude --permission-mode bypassPermissions` from the repo folder, or
- run `python3 claude-setup/install.py --apply bypass` once.

## Machine-wide install

```bash
python3 claude-setup/install.py              # shows what would change
python3 claude-setup/install.py --apply all  # models, bypass, rules
```

Backups (`*.bak-<timestamp>`) are written next to each file changed. The rules added to
`~/.claude/CLAUDE.md` are in [rules.md](rules.md), inside a marked block you can delete.

## Prerequisites

| Tool | Needed for | Install |
|---|---|---|
| Claude Code | everything | https://claude.com/claude-code |
| Python 3.9+ | tools | https://www.python.org (preinstalled on macOS and most Linux) |
| git | sync | https://git-scm.com |
| Node.js LTS | browser (Playwright) | https://nodejs.org |
| GitHub CLI + free account | sending database findings (optional) | https://cli.github.com, then skill `connect-github` |
