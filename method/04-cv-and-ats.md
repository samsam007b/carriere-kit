# CV structure, ATS formatting, keyword alignment

## What an ATS actually does

Most applicant tracking systems parse a CV into plain text before a human ever sees it, then
index that text for keyword search and sometimes auto-score it against the posting. A CV that
looks good on screen but relies on columns, text boxes, tables for layout, or text embedded in
an image can parse into scrambled or missing text. The rules below exist for that reason, not
for aesthetics.

## Structure that parses reliably

- **Single column.** A two-column layout can parse left-to-right across both columns, mixing a
  job title from one column with a date from the other.
- **Real text, never an image.** A name, a skills list, or a logo rendered as an image is
  invisible to the parser. Everything that carries information is live text.
- **Semantic headings**, not just bold text at a larger size: a clear heading structure
  (Experience, Education, Skills) that both a parser and a human scan the same way.
  Standard section names beat clever ones: "Experience," not "My Journey."
  "Skills," not "What I Bring."
- **Standard fonts and no text effects** that could break character encoding on export or
  parsing (WordArt-style effects, small caps rendered as separate glyphs, icon fonts standing
  in for words).
- **Contact info as plain text** at the top, not inside a header/footer element some parsers
  skip, and not as an image.
- **Dates in a consistent, unambiguous format** (Month YYYY, or YYYY-MM), same format
  throughout the document.
- **PDF export that preserves text**, not a flattened image PDF. If in doubt, select the text
  in the exported file; if selection fails, the parser will fail too.

## Content structure

1. **Header**: name, one professional title or headline, contact details, portfolio/LinkedIn
   link if relevant.
2. **Summary** (optional, 2 to 3 lines): only if it adds a specific angle the rest of the CV
   doesn't already convey. A generic summary ("results-driven professional with strong
   communication skills") is worse than no summary.
3. **Experience**: reverse chronological, each entry with role, organisation, dates, and 2 to 4
   bullet points that lead with what was done and what resulted, not a duty list. Quantify
   where a real number exists; never invent one.
4. **Education**: degree, institution, dates. Relevant coursework or a thesis topic only if it
   adds signal for this specific role.
5. **Skills**: grouped and specific (tools, methods, languages with real proficiency levels
   from `db/vocab.json`'s language level scale), not a wall of buzzwords.
6. **Projects** (if relevant): a personal or academic project that demonstrates capability a
   formal role didn't give room for.

Keep every fact traceable to `workspace/facts.md`. A figure on the CV that isn't backed by a
row in that file, with a source and a confidence level, doesn't go on the CV.

## Keyword alignment, not keyword stuffing

Before finalising a CV for a specific posting, compare the posting's own vocabulary against
the CV's current wording. The goal is alignment, using the term the posting uses when it
genuinely matches what you did, not insertion of terms that don't reflect real experience.

A simple manual process:

1. Copy the posting's requirements and responsibilities sections.
2. List the recurring nouns and skills it uses (its vocabulary, not yours).
3. For each one already true of your experience, check whether the CV currently uses the same
   term or a synonym; align the wording if it's a genuine match.
4. For each one that isn't true, leave it out. A CV that claims a skill the interview will
   expose as absent costs more than a slightly thinner match.
5. Never let keyword alignment change a fact. The number stays the number.

## The final check-up

Before a CV goes out, read it once for aesthetics and logic independent of the ATS pass:
consistent spacing and font sizes, bullet points that parallel each other grammatically, no
orphaned single-word lines, chronological order that actually holds together, no leftover
placeholder text. A CV that passes the parser but reads awkwardly to a human still fails the
next stage of the process.
