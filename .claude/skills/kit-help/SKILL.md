---
name: kit-help
description: Explain the kit itself - the shared vocabulary (sectors, job families, seniority, ATS, statuses), what the database contains, which tool or skill does what, how models and safety are set up. Use for "what does X mean", "which sectors exist", "what's in the database", "how do you choose models", "is it safe", "what can you do".
---

# kit-help

Answer the question asked, in 3 to 8 lines, then offer one deep dive. Do not dump files.

| Question about | Source of truth | Useful command |
|---|---|---|
| Sectors, job families, seniority, ATS, statuses | `db/vocab.json` | `python3 -c "import json;v=json.load(open('db/vocab.json'));print(', '.join(v['sectors']))"` |
| What the database holds | `db/README.md` | `python3 tools/db.py stats`, `python3 tools/db.py find <text>` |
| A company or a title | `db/companies/`, `db/job-titles.jsonl` | `python3 tools/db.py find <name>` |
| Tools and flags | `tools/README.md` | `python3 tools/<tool>.py --help` |
| Method | `method/00-overview.md` | |
| Models and tokens | `CLAUDE.md` section 6 | |
| Safety, permissions, sends | `CLAUDE.md` section 7, `.claude/hooks/` | |
| Sharing | `CONTRIBUTING.md` | |
| Machine-wide Claude Code setup | `claude-setup/README.md` | |

When you show vocabulary, show ids exactly as written (they are the shared language between
every user and every Claude). If the user describes something that fits no id, say which
id is closest and that a new value needs its own pull request on `db/vocab.json`.

## What the kit can do (use for "what can you do")

| Need | Skill |
|---|---|
| Know the user | `profile` |
| Find opportunities | `sweep`, `sector-scan` |
| Watch it work in a browser, fill portals | `browser` |
| One application end to end | `new-application`, `cv` |
| Follow-ups and pipeline | `follow-ups`, `status` |
| Interviews | `interview-prep` (drills with `interview-coach`) |
| Share and receive database | `contribute`, `connect-github` |
