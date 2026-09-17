---
name: contribute
description: Share database findings with the main kit repository, check what was sent, or receive everyone else's updates. Use for "share", "send my findings", "pull request", "update the database", "sync", "what did I contribute", or after a sweep or sector scan produced many records.
---

# contribute

Explain in 2 lines if the user has not seen it yet: only `db/` records (companies, boards,
postings, titles, notes) are shared, after validation and a personal-data scan; everything
in `workspace/` stays on this machine.

| User wants | Run | Then |
|---|---|---|
| Receive updates | `python3 tools/sync.py` | Summarise what changed (`python3 tools/db.py stats`) |
| Preview what would be sent | `python3 tools/contribute.py --dry-run` | Show the table of records |
| Send now | `python3 tools/db.py validate` then `python3 tools/contribute.py` | Give the pull request link |
| Last contribution | read `workspace/.logs/last-contribution.json` and the tail of `workspace/.logs/contribute.log` | |
| Stop automatic sending | set `"auto_contribute": false` in `workspace/config.json` | Confirm |

- "GitHub not connected" → skill `connect-github`. Records wait in `workspace/outbox/`.
- A record rejected by the personal-data scan: show the reason, fix the record in `db/` via
  `tools/db.py upsert` (remove the name, first person or judgement), or leave it out. Never
  weaken the scan.
- A new vocabulary value is needed: explain it goes in its own pull request editing
  `db/vocab.json`, and prepare it only if the user agrees.
- Sync says kit files were edited locally: show `git status`, ask whether to keep those edits
  (then commit on a branch) or discard them. Do not discard without a yes.
