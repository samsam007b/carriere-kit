# Contributing

The kit gets better in two ways: the **shared database** grows every time someone searches,
and the **method and tools** improve when someone finds a better way.

## 1. Database: automatic

You do not need to do anything. When you use the kit, Claude records objective discoveries
(companies, their ATS boards, postings with their real requirements, job titles, market
facts) in `db/`. At the end of each Claude Code session, `tools/contribute.py`:

1. compares your `db/` with the main repository, record by record;
2. validates the new or changed records and scans them for personal data;
3. opens a pull request from your fork (branch `db-contrib/<your-login>`), or updates the one
   already open.

Your `workspace/` folder (profile, tracker, applications) is never read by this tool and is
ignored by git.

| You want to | Do |
|---|---|
| See what would be sent | `python3 tools/contribute.py --dry-run` |
| Send now | `python3 tools/contribute.py` |
| Turn automatic sending off | `"auto_contribute": false` in `workspace/config.json` |
| Hide a word everywhere (your name, school, city) | Add it to `private_terms` in `workspace/config.json` |
| Get everyone else's additions | Automatic at session start, or `python3 tools/sync.py` |

Requirements: the GitHub CLI logged in (`gh auth login`). Commits use your GitHub noreply
address, so your email is not published.

### The rules the database enforces

- **One vocabulary**: every sector, job family, seniority, ATS, status comes from
  [db/vocab.json](db/vocab.json). Need a new value? Open a separate pull request that only
  changes `vocab.json` and explains why.
- **One writer**: `python3 tools/db.py upsert <dataset> '<json>'`. Never edit JSONL by hand.
- **Impersonal**: no people, no first person, no opinions relative to one candidate.
- **Evidence**: a posting is `open` only if verified on the official source that day.

Full schemas: [db/README.md](db/README.md).

### For maintainers

CI (`.github/workflows/db-check.yml`) validates every pull request. A `db-contrib/` branch
that touches anything outside `db/` fails. Review for plausibility (a real company, a real
posting URL), then squash-merge. Contributors' next session pulls the merge and their pull
request empties itself.

## 2. Method, skills, tools: regular pull requests

- Fork, branch, change, open a pull request with a short why.
- English in every file. No personal data, even as an example: use the fictional persona in
  `examples/`.
- Run `python3 -m unittest discover -s tools/tests` and `python3 tools/db.py validate`.
- Skills and agents must follow [CLAUDE.md](CLAUDE.md): explain before acting, one table,
  the user chooses, same vocabulary.
