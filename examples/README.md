# Worked example

This folder shows the system running on **one** lead, from spotting it to closing it. It
answers the question empty templates don't: what level of detail is expected in practice.

> **Everything here is fictional.** The organisation "Norvent," the people, and the facts don't
> exist. The fictional candidate's figures are marked as such. Nothing in this folder should
> ever be copied into a real application.

- [`norvent/README.md`](norvent/README.md): the full application case file, as it looks after
  three weeks of process.

Below, the tracker and calendar rows that carry this same lead, at the same point in time.

---

## Excerpt from `tracker.md`

```markdown
| Lead | Type | Status | Submitted | Follow-up | Last action | Source |
|---|---|---|---|---|---|---|
| Norvent | outreach | waiting | 2026-03-14 | 2026-04-21 | Interview on 2026-04-02, follow-up email sent 2026-04-03. They stated a reply "within two weeks" (by 2026-04-16); follow-up date is that plus 3 business days | workspace/applications/norvent/README.md |
```

One row, seven columns, no ambiguity about what happens next.

## Excerpt from `calendar.md`

```markdown
| Date | Deadline | Lead | Status |
|---|---|---|---|
| 2026-04-03 | Post-interview follow-up email (done) | Norvent | Watch |
| 2026-04-16 | End of the timeframe they stated | Norvent | Watch |
| 2026-04-21 | Follow up if still no answer (their deadline plus 3 business days of buffer) | Norvent | Watch |
```

The calendar is the source of truth if it ever disagrees with the tracker: one file owns every
date.

## What the example illustrates

| Point | Where to see it |
|---|---|
| A hook that wouldn't work anywhere else | The "Angle" section of the case file |
| A contact verified in the right order, with written proof | The "Contact" section |
| A language decided from signals, not assumed | The "Language" section |
| An email under 150 words, with the draft-to-sent diff | The "Email sent" and "Draft to sent" sections |
| A dated history that lets the case file be picked back up six weeks later | The "History" section |
