# Profile

> Facts about you: identity, education, experience, skills. For the source-of-truth table of
> verified figures with confidence levels, see `workspace/facts.md`; nothing here should
> contradict it.

## Identity

| Field | Value |
|---|---|
| Full name | {{First name Last name}} |
| Contact email | {{email}} (the one on the CV, so the one you send from) |
| Phone | {{phone}} |
| City | {{City, Country}} |
| LinkedIn | {{URL}} |
| Website / portfolio | {{URL}} |
| Nationality, work permit | {{...}} |
| Availability | {{date, or "immediate"}} |

**Default sending address**: {{email}}.
{{If you have a secondary academic or professional address: state exactly when it's used
instead of the default. Useful rule: only with a real anchor to the target, not as a habit.
Watch for an address that expires at the end of studies while a reply might land after.}}

## Education

| Degree | Institution | Period | Notes |
|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{specialisation, thesis topic}} |

## Experience

For each entry: exact title, organisation, dates, and two or three **quantified** facts.

### {{Title}}, {{Organisation}} ({{period}})

- {{Quantified fact 1}}
- {{Quantified fact 2}}
- {{What was actually your responsibility, without inflating it}}

## Languages

| Language | Real level | Evidence |
|---|---|---|
| {{...}} | {{one of the `db/vocab.json` `language_levels`: A1, A2, B1, B2, C1, C2, native}} | {{test, time lived, professional use}} |

Never claim a level that wouldn't hold up in an interview.

## Skills

Grouped by block, ordered by relevance to the dominant target. The CV mirrors this structure.

- **{{Block 1}}**: {{...}}
- **{{Block 2}}**: {{...}}
- **{{Block 3}}**: {{...}}
- **Tools**: {{...}}

## Gates I check on every posting

Fill this once, reuse it on every lead (see
[`method/03-follow-up-and-gates.md`](../method/03-follow-up-and-gates.md)).

| Gate | Your real threshold | Notes |
|---|---|---|
| Years of experience | {{...}} | |
| Language | {{...}} | |
| Degree / certification | {{...}} | |
| Location | {{...}} | A role honestly based elsewhere isn't excluded on its own; only a misleading location listing is |

## What I don't claim

Explicit list of labels never to self-apply, with the reason. This is what keeps an AI
assistant from over-selling by default.

- Never "{{label}}": {{reason, e.g. no formal experience, would be a false signal}}
- Never "{{label}}": {{reason}}

## Administrative details

> Useful for official forms and portals. **Never commit this to a public repository.** Keep
> this section in a file outside version control if this workspace is ever pushed anywhere,
> even though `workspace/` is gitignored by default.

Typically requested fields: date and place of birth, full address, national ID number, marital
status, current status, bank account for travel expense reimbursement.
