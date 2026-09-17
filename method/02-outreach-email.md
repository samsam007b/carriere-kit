# Outreach email: method and anti-patterns

> Built from a simple practice: compare the draft an AI assistant produces against the email
> actually sent after a human edited it. The gaps repeat. They are named here as anti-patterns
> so the next draft starts closer to the sent version.

## Step 0: settle the objective before writing a line

Non-negotiable. An email written without a settled objective ends on a soft "let me know if
you'd like to chat," the first sign of a text nobody thought through.

| Objective | Register | CTA type | Length |
|---|---|---|---|
| Internship / traineeship | Motivated, never pleading, a precise start date | "Available from {{date}}. Happy to discuss." | ~120-150 words |
| Specific open role | Direct on the fit between role and profile, no long story | "Would you be open to a conversation about this?" | Short to medium |
| Speculative application | Factual observation, then concrete value, never presumptuous | Open invitation to talk, never a direct ask for a job | Short |
| Freelance / consulting pitch | Value proposition by the second sentence, credentials in support | Open call, no unsolicited demo promised | ~100 words |
| Network contact | Genuine curiosity, a checkable reference | Open question, no sales CTA | Very short |

If the objective isn't already written in the case file, settle it there first.

## The ceiling: 150 words

Past 150 words, a cold email doesn't get read in full. The limit forces a single argument,
which is exactly the right constraint.

Structure that fits the budget:

1. Named salutation.
2. One sentence: who you are, with your hardest-to-fake piece of evidence.
3. One or two sentences: the concrete link with **them**, not a compliment.
4. "CV attached."
5. Open CTA, one line.
6. Sign-off and name.

## The anti-patterns

### PATTE-OUT-01: no named salutation

Starting straight into the argument reads like a recycled cover-letter excerpt, not a message
addressed to a person. Default to `Dear {{First name}},` (or `Hi {{First name}},` in informal
tech/startup contexts); reserve a title-only salutation for a senior contact or a formal
organisation, and never use "To whom it may concern" when a name is available.

### PATTE-OUT-02: over-qualifying a point already made

Adding a clause after a point is finished ("...without formal training, **by using AI to
execute fast**") or an emphasis adjective ("the **exact** intersection of your two mandates")
dilutes instead of strengthening. The most common manual edit. Ask of every sentence: does the
second half add information, or just emphasis? Cut if it's only emphasis.

### PATTE-OUT-03: indefinite article on an identified role

"**A** role at your company" when the target role is precisely identified signals a mass
send; "**the** role" signals real research. Free signal of seriousness once a named role
exists in the case file.

### PATTE-OUT-04: attachment never mentioned

Attaching the CV without ever naming it in the body leaves ambiguity. One short line, "CV
attached," right before the CTA.

### PATTE-OUT-05: missing or over-commercial CTA

Ending on the argument with no explicit invitation, or omitting the sign-off, leaves the
reader with no easy action. On the other side, a CTA that names a fixed duration ("a 20-minute
call") or promises an unsolicited demo tips into sales pitch. Use an open invitation, no
number, no promised deliverable, then sign-off and name.

### PATTE-OUT-06: tics recognisable as AI-generated text

Check every draft against this list before sending:

- **Punctuation**: em dash and en dash used as connectors. The single biggest tell. Replace
  with a comma, period, colon or parentheses. A short hyphen inside a compound word is fine. A
  semicolon used as a stylistic link rather than a grammatical one has the same problem.
- **"Boost" vocabulary**: leverage, unlock potential, shape, supercharge, deploy outside a
  technical context, transform used as filler.
- **Formulaic openers**: "I hope this email finds you well," "I am reaching out because,"
  "In today's fast-paced world..."
- **Empty emphasis**: truly, clearly, "both... and," rhetorical triplets ("fast, efficient and
  relevant").
- **Artificial contrast**: "I don't just do X, I do Y," "not only X but Y." Reads hollow.
  Replace with the plain factual claim.
- **Generic closers**: "Don't hesitate to reach out," "I remain at your full disposal."
- **Too-perfect symmetry**: three paragraphs of near-identical length, each built the same way
  (observation, link, benefit). A human varies.

A candidacy email that reads as machine-generated hurts more when the profile claims real
fluency with these tools. Prefer a slightly irregular rhythm: variable sentence length, one
factual observation stated without a connector.

### PATTE-OUT-07: stating the obvious shared connection

Spelling out the link ("the same school as you," "we share this path") infantilizes the reader
and reads like a sales technique. State the fact; let the reader draw the connection.

## The review protocol

In this order, for every draft:

1. Objective settled (step 0), or don't write yet.
2. Draft.
3. Count words. Over 150: cut, don't rephrase.
4. Check against PATTE-OUT-01 to 07, with extra weight on 06.
5. Check every figure against `workspace/facts.md`. Nothing unverified goes out.
6. **Show the full text**, even if the content was already agreed earlier in the
   conversation. Get an explicit "yes, send" in the current turn. An approval from a previous
   turn is expired.
7. After sending, if the text was hand-edited, log the diff in the application's case file.
   That is what calibrates the next draft.

## Keep your own diff table

The most valuable habit in this method: after every send, compare the draft against the email
that actually left (check Sent, not the draft, which may have changed before sending), and log
the gap.

The rows below are illustrative starters, not a real log. They show the expected grain, a
concrete correction, not a vague note like "too long." Replace them with your own; only your
own diffs calibrate your drafts.

| Draft | Sent | Pattern |
|---|---|---|
| "the **exact** intersection of your two mandates" | "the intersection of your two mandates" | Drop emphasis adjectives; they weaken instead of strengthen |
| "I am reaching out regarding..." | "{{Observed fact about them}}." | Cut the apologetic opener, start with substance |
| "a role within your team" | "the {{exact title}} role" | Definite article plus exact title; the indefinite signals a mass send |
| "I'd love to chat for 15 minutes about my approach" | "Would you be open to a conversation about this?" | Drop the fixed duration and the promised pitch; the CTA opens, it doesn't sell |
| "fast, rigorous and results-driven" | "{{one dated, quantified fact}}" | Replace the adjective triplet with a proof; an adjective is asserted, a fact is checkable |
| "your well-known expertise in {{field}}" | _(deleted)_ | Cut the flattery; it says nothing about the candidate and reads as a mail-merge |

Five or six rows of your own diffs are usually enough to converge. If three sends in a row
produce no manual correction, the calibration holds and the table can rest until the register
or the language changes.
