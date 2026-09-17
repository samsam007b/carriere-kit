---
name: interview-prep
description: Prepare for an upcoming interview, or debrief one that just happened. Use when the user says "I have an interview", "prep me for X", "help me get ready for the call with Y", or "just had the interview, let's debrief".
---

# Interview prep

Two distinct moments: before, and the 24-hours-after debrief. Don't conflate them.

## Before the interview

1. Read the case file at `workspace/applications/<slug>/README.md`: Objective, Angle,
   Contact, and any posting details already gathered.
2. Read `workspace/facts.md` and `workspace/storytelling.md` for the figures and the angle
   the user actually stands behind. Never invent an answer to a likely question, if the
   fact isn't in `facts.md`, ask or mark it `{{to confirm}}`.
3. Build a short brief per
   [method/06-interview-preparation.md](../../method/06-interview-preparation.md): likely
   questions given the posting and the angle, the three key questions from
   `workspace/storytelling.md`, and anything about the interviewer or format worth flagging.
4. Offer a roleplay drill via the `interview-coach` agent for the questions that feel
   hardest. Pass it the application slug so it can read the same case file and log notes
   back to it.

## After the interview (debrief)

1. Prompt the debrief template from
   [method/06-interview-preparation.md](../../method/06-interview-preparation.md): questions
   that surprised the user, anything the interviewer said that the posting didn't mention,
   and a read on interest level, up or down.
2. Append it to the case file under an "Interview debrief" section, dated.
3. Update the tracker row: Status likely stays `waiting`, Last action updated, and a new
   Follow-up date set per [method/03-follow-up-and-gates.md](../../method/03-follow-up-and-gates.md)
   (their stated timeframe plus a 3 business day buffer, if they gave one). Run
   `python3 tools/tracker.py lint` after editing.

## Propose the next step

Before: offer the roleplay drill. After: offer to draft the post-interview follow-up email,
but never send it without showing the full text and getting explicit confirmation in the
current turn.
