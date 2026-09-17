#!/usr/bin/env python3
"""Small keyword classifier: job title -> (family, seniority).

Used by sweep.py to fill the `family` and `seniority` fields of a posting
record, and callable standalone by an agent that just wants a quick read on
one title. Both outputs are vocab ids from db/vocab.json (job_families,
seniority) -- never free text.

This is a heuristic, not a parser. Titles are messy and ambiguous on purpose
(a "Chief of Staff" posting can hide anything); the classifier picks the
single best keyword match and falls back to "other" / "unknown" rather than
guessing. Treat its output as a starting point, not ground truth -- the real
requirements live in the body of the posting (see db/README.md on `notes`).

Usage: python3 tools/classify.py "Job title" -> prints "family seniority"
"""
import re
import sys

# Ordered most-specific-first: the first matching pattern wins. This matters
# because many titles overlap two families ("Regulatory Affairs Manager"
# reads as both legal-regulatory and public-affairs-policy; we deliberately
# want the second).
FAMILY_RULES = [
    ("public-affairs-policy", r"public (affairs|policy)|govern?ment (affairs|relations)|regulatory affairs|policy (manager|lead|officer|advisor)"),
    ("legal-regulatory", r"\blegal\b|compliance|\bcounsel\b|\bregulatory\b"),
    ("strategy-operations", r"chief of staff|founder'?s? associate|entrepreneur in residence|strategy (&|and) op|business operations?|\bbizops\b|special projects|executive office|operations manager|strategy (manager|lead|director)"),
    ("project-program", r"project manager|program(me)? manager|\bpmo\b"),
    ("communications-marketing", r"communications?|marketing|\bpr\b|\bbrand\b|\bcontent\b"),
    ("consulting", r"\bconsultant\b|\bconsulting\b"),
    ("data-ai", r"data scientist|data analyst|\bdata\b|analytics|machine learning|\bml\b|\bai\b|artificial intelligence"),
    ("engineering", r"\bengineer\b|\bdeveloper\b|\bsoftware\b"),
    ("finance", r"\bfinance\b|financial|accounting|\bcontroller\b|investment"),
    ("hr-people", r"\bhr\b|recruit|talent|people (operations|partner)"),
    ("product-design", r"product (manager|owner)|\bux\b|\bui\b|\bdesigner\b|design lead"),
    ("sales-bizdev", r"\bsales\b|business development|account manager|\bbizdev\b"),
]

# Also ordered most-specific-first: intern/graduate patterns are checked
# before the broader executive/lead/senior/junior tiers so "Graduate Chief
# of Staff Programme" (rare, but exists) reads as graduate, not executive.
SENIORITY_RULES = [
    ("intern", r"\bintern(ship)?\b|\bstage\b|\bstagiair"),
    ("graduate", r"\bgraduate\b|\btrainee\b|entry[- ]level"),
    # "Chief of Staff" is explicitly not an executive title by seniority --
    # it varies wildly by company and tells you nothing on its own.
    ("_chief_of_staff_exception", r"chief of staff"),
    ("executive", r"\bdirector\b|\bvp\b|\bchief\b"),
    ("lead", r"\blead\b|head of|\bprincipal\b"),
    ("senior", r"\bsenior\b|\bsr\.?\b"),
    ("junior", r"\bjunior\b|\bassociate\b"),
]


def classify(title):
    """Return (family, seniority), both vocab ids, best-effort from the title alone."""
    t = title or ""
    family = "other"
    for fam, pat in FAMILY_RULES:
        if re.search(pat, t, re.I):
            family = fam
            break
    seniority = "unknown"
    for sen, pat in SENIORITY_RULES:
        if re.search(pat, t, re.I):
            seniority = "unknown" if sen == "_chief_of_staff_exception" else sen
            break
    return family, seniority


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 tools/classify.py \"Job title\"", file=sys.stderr)
        return 1
    family, seniority = classify(argv[1])
    print(f"{family} {seniority}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
