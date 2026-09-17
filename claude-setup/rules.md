<!-- carriere-kit:rules:start -->
## Working rules (installed by carriere-kit claude-setup)

### Models and tokens
| Work | Model |
|---|---|
| Web research, reading long documents, scanning many files | Haiku subagent (read-only) |
| Planning, strategy, hard reasoning | Opus in Plan Mode (`opusplan`, Shift+Tab) |
| Writing code, documents, running tools | Sonnet |

- Never use Haiku to write or modify code or documents.
- Research in two phases: a Haiku subagent returns at most 400 tokens and a "worth a deep
  dive" table, then deep-dive 1 to 3 items.
- Edit files in place instead of pasting them in chat. Tables for 3 or more items. No filler.
- Suggest `/compact` around half context, a new session for a new topic.

### Safety
- Anything that leaves the machine (email, form, post, message) needs the full text shown and
  an explicit yes in the user's latest message.
- Never write secrets in tracked files; use a git-ignored `.env`.
- Prefer a CLI (`gh`, `npm`, ...) over an MCP server doing the same thing.
- Explain in 1 or 2 lines before a multi-step action, then say what changed.
<!-- carriere-kit:rules:end -->
