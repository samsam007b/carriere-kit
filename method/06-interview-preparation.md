# Interview preparation, and everything after

The method doesn't stop at the interview door. This file covers preparation, the 24 hours
after, the wait, the offer, the negotiation, and a decline or withdrawal.

> Scope warning: the offer and negotiation sections touch labor law and pay practices that vary
> by country. Nothing here is legal advice. Any amount, legal deadline, or pay scale must be
> checked against an official source for the relevant country before it's used in a
> negotiation.

## Before the interview

Build a brief in the application's case file (`workspace/applications/<slug>/`), not from
memory, right before the interview:

- The exact posting text, re-verified at the source (postings get edited).
- The company's recent public activity: news, product launches, funding, leadership changes.
- Your own angle for this specific interview: the two or three points you want to land no
  matter what's asked.
- Likely questions given the role and seniority, with a short answer sketch for each, backed by
  `workspace/facts.md`, never an invented number.
- Questions to ask them. A candidate with no questions reads as uninterested.

An `interview-coach` style agent (see `.claude/agents/interview-coach.md`) can run a recruiter
roleplay drill against this brief and score the answers before the real thing.

## The 24 hours after

Two actions, in this order.

**Write the debrief while it's fresh**, in the case file's README. What's lost after 48 hours
and never reconstructed:

```markdown
### Interview on {{date}} with {{name}}, {{title}}

**Format**: {{video / on-site / phone}}, {{actual duration}}
**Next step as stated by them**: {{exact wording}}, within {{stated timeframe}}

**Questions that surprised me**:
- {{question}} -> what I answered / what I should have answered

**What they said about the role that the posting didn't**:
- {{point}}

**Signals about the team and context**: {{turnover, reorganisation, budget, urgency}}
**My interest level after the conversation**: {{up / down / unchanged}}, and why
```

The last line matters as much as the others. Interest dropping after an interview is a data
point, not a flaw to fix.

**Send the follow-up email** within 24 hours, following the pattern in
`templates/emails/outreach.md`. It needs to carry substance, not a thank-you alone: a fuller
answer to a question that came up, or a specific point from the conversation. Without
substance, better not to send it.

## The wait

The timeframe they stated is the one that counts. Log it in `workspace/calendar.md`, with
**three business days of buffer** before any follow-up.

| Situation | Action |
|---|---|
| Stated deadline passed by less than 3 business days | Nothing. Processes slip; following up too early shows |
| Stated deadline passed by more than 3 business days | A four-line follow-up, no reproach, referencing the timeframe **they** gave |
| No deadline stated | Follow up at 10 business days |
| Another offer arrives with a deadline | State it factually, with the date. Not an ultimatum, a real calendar constraint. Never invent a competing offer |
| Second follow-up with no answer | Close the lead in `workspace/tracker.md`. Don't send a third |

## The offer arrives

**Never accept on the call.** Thank them, stay positive, ask for the offer in writing and a
few days to consider it. A short reflection period is a normal ask; an employer who refuses one
has just told you something about themselves.

Check the following on the written document, before any discussion of amount:

- Exact title, reporting line, location, on-site or remote and how it's formalised.
- Contract type, duration, probation period and its termination conditions.
- Compensation: base, variable, and **the exact condition that triggers the variable**,
  quantified benefits.
- Start date, leave entitlement, notice period.
- Any clause that binds you beyond the contract: non-compete, intellectual property,
  exclusivity. Read them line by line; they weigh most heavily on a profile that runs projects
  on the side.

Compare every element against **localised** market data: same country, same sector, same
seniority. A pay scale imported from a different market is worth nothing (see PATTE-CAR-05 in
[05-career-anti-patterns.md](05-career-anti-patterns.md)).

## Negotiating

Three principles, nothing more.

**One negotiation cycle.** Gather every ask into a single round. Negotiating point by point
across several exchanges burns goodwill and reads as indecisive.

**Justify from the market or the scope, never from personal need.** "The role includes
{{responsibility}}, which wasn't in the posting" is an argument. "I have rent to pay" is not.

**Only ask for what you'd accept if granted.** Every ask that's granted comes with an implicit
commitment to sign. Asking to test the waters, then declining anyway, burns the contact and the
network behind them.

The amount isn't the only variable. Often easier to move: start date, remote days, a training
budget, a scheduled compensation review date, the job title itself.

## Declining an offer, or withdrawing

This happens more often than expected, and it's the moment that builds or breaks a long-term
relationship. Three rules:

- **Fast.** As soon as the decision is made. Every day of delay blocks their process and
  another candidate.
- **Same channel, same person.** No disappearing, no delegating to a form.
- **No invented reason.** "I've accepted another role" or "the scope isn't what I'm looking
  for" is enough. A fabricated reason creates a story you'll have to maintain if the contact
  resurfaces years later.

The sector is smaller than the number of postings suggests. The person you decline today may be
the one hiring where you want to go next.

## Closing the loop

Whatever the outcome, close the lead cleanly:

- `workspace/tracker.md`: final status, date, and **one line on what you took from it**.
- `workspace/calendar.md`: remove deadlines that no longer apply.
- The company's record (in `db/companies/` if the fact is objective and shareable, or a note in
  the case file if it's a personal judgement call): a decline isn't a closed door, it's a dated
  one.
- If the outcome taught something transferable, a mechanism, not an anecdote, it belongs
  wherever this method keeps what's been learned across attempts (a project-specific notes
  file, if the kit's user keeps one). The question to ask: what would I do differently, and at
  exactly which point in the process.
