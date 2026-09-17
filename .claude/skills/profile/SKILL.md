---
name: profile
description: Get to know the person Claude works for. Structured interview, CV/LinkedIn ingestion and optional research of their public professional footprint, written to workspace/profile.md and workspace/facts.md with sources and confidence. Use at onboarding, when the profile is empty or stale, when the user shares a CV, or when a new durable fact about them appears ("update my profile", "I got promoted", "I now speak...").
---

# profile

Goal: after this skill, you can describe the user as precisely as a good recruiter who
spent an hour with them, and every fact you would put on a CV is sourced.

Principles:
- **Facts over flattery.** Never round up, invent or embellish. Unknown stays unknown.
- **Short rounds.** At most 3 questions per message, easiest first. Show progress
  ("round 2 of 6").
- **Use what exists before asking.** A CV or LinkedIn export answers half the interview.
- **Reflect back.** After each round, write to the files, then summarise in 2 lines what you
  understood. The user corrects cheaply.
- Answer in the user's language; files stay in English (quotes keep their language).

## Mode A: first interview

### Round 0: inputs (propose all, all optional)

1. "Do you have a CV, a LinkedIn PDF export, a portfolio or a past cover letter? Drop the
   file path or paste the text." Read long files through the `doc-reader` subagent with the
   brief: list facts (titles, organisations, dates, figures, degrees, languages, tools),
   each with where it was found, no judgement.
2. "May I look up your public professional footprint (LinkedIn, personal site, GitHub,
   publications, press)? Give me the links or the name to search." **Only with an explicit
   yes.** Use the `researcher` subagent, or open the pages with the `browser` skill so they
   see what you see. Anything found online is confidence C until the user confirms it.
3. Pre-fill `workspace/profile.md` and `workspace/facts.md` from these sources, then ask
   only about gaps and contradictions.

### Rounds 1 to 6

| Round | Theme | Examples of questions (pick, adapt, skip what is known) |
|---|---|---|
| 1 | Now | What do you do today? Since when? What are you looking for, and by when? |
| 2 | Proof | Three things you built, changed or delivered that you are proud of. For each: context, what you did yourself, result with a number if one exists, who can confirm it |
| 3 | Gates | Languages and honest CEFR level per language (spoken and written). Locations and relocation. Remote. Contract types. Salary floor. Years of relevant experience. Degrees and their exact names. Work permit |
| 4 | Energy | Which tasks give you energy, which drain you? Sectors or missions you would refuse? What made you leave or stay in past roles? |
| 5 | Voice | How do you want to sound in an email: formal, direct, warm? Words you never use? Paste a message you wrote and liked |
| 6 | Red lines | What must never appear in your applications (a former employer, a side business, a name, health, a gap)? Add sensitive words to `private_terms` |

Techniques for good answers:
- **Ask for a story, not an adjective.** "Tell me about a time" beats "are you organised?".
- **Dig once on vague answers.** "Many clients" → "roughly how many, over what period?"
- **Separate contribution from team result.** "What part was yours?"
- **Check numbers twice** when they will go on a CV: "Is 40% measured or estimated?"
- **Contradiction = question, not correction.** "The CV says 2021, you said 2022: which one?"
- **Offer an escape**: "skip" is always a valid answer.

### Writing

- `workspace/profile.md`: fill the template sections, replace `{{placeholders}}`, keep
  `{{to confirm}}` where unknown.
- `workspace/facts.md`: one row per citable fact: `fact | value | source | confidence | last checked`.
  Confidence A = verified document or public source confirmed by the user, B = stated by the
  user, C = inferred or found online and not confirmed yet. Only A and B go on a CV.
- `workspace/config.json`: `language`, `private_terms` (their full name, city, school,
  employer names they want hidden from the shared database), `onboarded_on`.
- `workspace/positioning.md` and `workspace/storytelling.md`: draft only if the user wants
  to go further at the end (offer it).

### Close

Give a 5-line portrait of the person as you now understand it, 3 open questions left, and
propose next steps: `sweep` / `sector-scan` to find opportunities, or `new-application`.

## Mode B: update

Triggered when a new durable fact appears in conversation, or on "update my profile".

1. State the fact you would add or change, with its source and confidence.
2. On yes, edit `facts.md` (update `last checked`) and the matching section of `profile.md`.
3. If a fact changed a number used in past applications, list the applications in
   `workspace/applications/` that quote the old value. Do not rewrite sent documents.

## Mode C: review

On "who am I for you?" or before a major application: summarise the profile in 10 lines,
flag facts older than 6 months or still at confidence C, and ask up to 3 questions to refresh.
