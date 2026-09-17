---
name: cv
description: Build or tailor a CV for a specific application. Use when the user asks for a CV, wants to tailor their CV to a posting, or mentions ATS keyword alignment.
---

# CV

## 1. Source of truth

Read `workspace/profile.md` and `workspace/facts.md` before writing anything. Every figure,
title, and date on the CV must trace back to `facts.md`. Never invent or round a number.
Missing fact: ask, or mark `{{to confirm}}` and flag it to the user, do not fill the gap
yourself.

## 2. Start from the template, not a blank page

Copy [templates/cv-template.html](../../templates/cv-template.html) (or `-fr.html` if the
target language is French) into the application folder as
`workspace/applications/<slug>/cv.html`. Keep the structure: single column, semantic
headings, plain-text contact line. Per
[method/04-cv-and-ats.md](../../method/04-cv-and-ats.md), an ATS parser reads structure, not
layout, do not add a second column, an icon font, or a photo.

## 3. Tailor, don't rewrite

What changes between two CVs for the same person: order of skill blocks, which experience
bullets are surfaced, the positioning headline. What never changes: the facts themselves.

Run the keyword alignment step from
[method/04-cv-and-ats.md](../../method/04-cv-and-ats.md): compare the posting's vocabulary
against the CV's, and align wording only where the underlying skill or experience is real.
Keyword stuffing (adding a term the user doesn't actually have grounds for) is a violation of
"never embellish", not a tactic.

## 4. Final check-up

Before presenting the result: read it once for aesthetics (does it fit one page, is spacing
consistent) and once for logic (does every bullet still make sense in the new order, does the
headline match the rest of the document).

## 5. Propose the next step

Offer to export to PDF and attach it to the draft outreach email or application-portal case
file. Never submit or attach-and-send on the user's behalf without showing the final document
and getting explicit confirmation in the current turn.
