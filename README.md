# carriere-kit

A career copilot for [Claude Code](https://claude.com/claude-code). Clone it, open Claude Code
in the folder, say hello. It gets to know you, finds and verifies opportunities at the
source, prepares applications and interviews, shows its work in a real browser, and never
sends anything without your yes.

Every user also feeds a **shared database** of companies, their job boards, postings with
their real requirements, job titles and market notes, organised by sector. Your next search
starts from everything the others already found. Your personal data never leaves your machine.

## Quick start

```bash
git clone https://github.com/samsam007b/carriere-kit.git
cd carriere-kit
claude
```

Then type `hi`. Claude explains what it can do in a few lines and offers a menu. First run
creates your private `workspace/` folder.

Prerequisites: Claude Code, Python 3.9+, git. Recommended: Node.js (browser) and a free
GitHub account with the GitHub CLI (to share database findings). Details in
[claude-setup/README.md](claude-setup/README.md).

## What it does

| You want | Skill | What happens |
|---|---|---|
| Be understood | `profile` | Interview in short rounds, reads your CV or LinkedIn PDF, optional research of your public footprint (with your consent). Every fact sourced and rated |
| Find opportunities | `sweep` | Scans hundreds of public ATS boards (Lever, Greenhouse, Ashby, SmartRecruiters, Recruitee, Workable, Personio), shows only what is new |
| Explore a sector | `sector-scan` | Turns a member directory (federation, cluster) into mapped companies, hiring channels and a shortlist |
| Watch it work | `browser` | Opens postings, portals and webmail in a visible browser. You handle logins and captchas, you approve every send |
| Apply | `new-application`, `cv` | Verifies the posting, checks the gates, tailors CV, letter and email, tracks the follow-up date |
| Stay on top | `follow-ups`, `status` | Overdue follow-ups at every session start, pipeline dashboard |
| Interview | `interview-prep` | Company research, likely questions, recruiter roleplay drills |
| Share | `contribute`, `connect-github` | Database findings go to this repo as pull requests, automatically |

## How it is organised

| Path | Content | Shared? |
|---|---|---|
| `workspace/` | Your profile, facts, tracker, applications, settings | Never, ignored by git |
| `db/` | Shared database: companies and postings by sector, job titles, search filters, sources, market notes, one vocabulary | Yes, through pull requests |
| `method/` | The method: research and sources, outreach, follow-ups, gates, CV, interviews, anti-patterns | |
| `templates/`, `examples/` | Starting files and a fictional worked example | |
| `tools/` | Python tools (standard library only): database, tracker, ATS sweep, sync, contribution | |
| `.claude/` | Skills, agents, hooks, settings | |
| `claude-setup/` | Optional machine-wide Claude Code setup | |

## How Claude is set up here

- **Fast**: bypass-permissions mode, no prompt for each action. If Claude still asks
  permission for every action, the project setting was ignored by your Claude Code version:
  run `python3 claude-setup/install.py --apply bypass` once, restart Claude Code (or launch
  it with `claude --permission-mode bypassPermissions`).
- **Safe**: hooks block destructive commands, secrets in files, direct database edits, and any
  final send (email, portal, form) without your explicit yes in the same turn.
- **Token-efficient**: Opus plans (Plan Mode), Sonnet executes, Haiku searches and reads.
  Enforced by settings, agent definitions and a hook.
- **One language**: every clone uses the same ids from [db/vocab.json](db/vocab.json), so
  databases merge cleanly and every Claude understands every other one.

## The shared database

[db/README.md](db/README.md) has the schemas. In short: JSON Lines sorted by id, written
only through `python3 tools/db.py upsert`, validated and scanned for personal data locally
and in CI. At session end, new records are sent as a pull request from your fork (turn off
with `"auto_contribute": false` in `workspace/config.json`). At session start, everyone
else's merged records are pulled in. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).
