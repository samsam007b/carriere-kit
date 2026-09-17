#!/usr/bin/env python3
"""ATS connectors shared by resolve.py and sweep.py.

Each function takes a board slug and returns a list of dicts
{title, location, url}. It raises on a board that does not exist or does not
answer (wrong slug, company moved ATS, network/HTTP error), which lets
resolve.py and sweep.py tell "board absent" apart from "board answered with
zero postings" -- the two must never collapse into the same silent outcome
(see tools/README.md, "boards must never be swallowed silently").

Seven ATS covered. Lever, Greenhouse and Ashby cover dollar-funded scale-ups;
SmartRecruiters, Recruitee, Workable and Personio cover the part of the
European market invisible to the first three (a real finding from an earlier
audit: a whole cluster of Belgian and German employers had zero presence on
Lever/Greenhouse/Ashby and only showed up once these four were added).

Provider ids match db/vocab.json's `ats` keys exactly: ashby, greenhouse,
lever, personio, recruitee, smartrecruiters, workable.
"""
import json
import random
import threading
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

UA = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
TIMEOUT = 20
RETRIES = 4


class BoardError(Exception):
    """Raised when a board does not exist or does not answer at all.
    Distinct from a board that answers and lists zero postings (that is a
    normal, valid result: an empty list, not an exception).
    """


# Ashby returns HTTP 429 as soon as more than a handful of requests hit the
# same host at once. An earlier sweep run lost 12 Ashby boards in a row this
# way and, because 429s and dead boards were not told apart, those companies
# silently dropped out of the watch list until someone noticed by hand.
# Two guardrails fix that: an exponential backoff on 429, and a concurrency
# gate capping simultaneous Ashby requests regardless of the caller's own
# thread pool size.
ASHBY_GATE = threading.Semaphore(4)


def _get(url, data=None):
    last_err = None
    for attempt in range(RETRIES):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=UA), timeout=TIMEOUT)
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 404:
                raise BoardError(f"404 at {url}") from e
            if e.code != 429 or attempt == RETRIES - 1:
                raise BoardError(f"HTTP {e.code} at {url}") from e
            time.sleep((2 ** attempt) + random.random())
        except urllib.error.URLError as e:
            raise BoardError(f"unreachable: {url} ({e})") from e
    raise BoardError(f"gave up after {RETRIES} retries: {url}") from last_err


def lever(slug):
    try:
        d = json.load(_get(f"https://api.lever.co/v0/postings/{slug}?mode=json"))
    except json.JSONDecodeError as e:
        raise BoardError(f"invalid JSON from lever/{slug}") from e
    if not isinstance(d, list):
        raise BoardError(f"unexpected lever response for {slug}")
    return [{"title": p.get("text", ""), "location": (p.get("categories") or {}).get("location") or "",
             "url": p.get("hostedUrl", "")} for p in d]


def greenhouse(slug):
    d = json.load(_get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"))
    if "jobs" not in d:
        raise BoardError(f"no 'jobs' key for greenhouse/{slug}")
    return [{"title": j.get("title", ""), "location": (j.get("location") or {}).get("name", ""),
             "url": j.get("absolute_url", "")} for j in d["jobs"]]


def ashby(slug):
    with ASHBY_GATE:
        return _ashby(slug)


def _ashby(slug):
    q = {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {"organizationHostedJobsPageName": slug},
        "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) { jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) { jobPostings { id title locationName } } }",
    }
    d = json.load(_get("https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobBoardWithTeams", json.dumps(q).encode()))
    jb = (d.get("data") or {}).get("jobBoard")
    if not jb:
        raise BoardError(f"jobBoard null for ashby/{slug}")
    return [{"title": p.get("title", ""), "location": p.get("locationName") or "",
             "url": f"https://jobs.ashbyhq.com/{slug}/{p['id']}"} for p in jb["jobPostings"]]


def smartrecruiters(slug):
    d = json.load(_get(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100"))
    if "content" not in d:
        raise BoardError(f"no 'content' key for smartrecruiters/{slug}")
    out = []
    for p in d["content"]:
        loc = p.get("location") or {}
        out.append({"title": p.get("name", ""), "location": ", ".join(x for x in [loc.get("city"), loc.get("country")] if x),
                    "url": f"https://jobs.smartrecruiters.com/{slug}/{p.get('id')}"})
    return out


def recruitee(slug):
    d = json.load(_get(f"https://{slug}.recruitee.com/api/offers/"))
    if "offers" not in d:
        raise BoardError(f"no 'offers' key for recruitee/{slug}")
    return [{"title": o.get("title", ""), "location": o.get("location") or o.get("city") or "",
             "url": o.get("careers_url") or o.get("careers_apply_url") or ""} for o in d["offers"]]


def workable(slug):
    d = json.load(_get(f"https://apply.workable.com/api/v1/widget/accounts/{slug}?details=true"))
    if "jobs" not in d:
        raise BoardError(f"no 'jobs' key for workable/{slug}")
    out = []
    for j in d["jobs"]:
        loc = j.get("location") or {}
        out.append({"title": j.get("title", ""), "location": ", ".join(x for x in [loc.get("city"), loc.get("country")] if x),
                    "url": j.get("url") or j.get("application_url") or ""})
    return out


def personio(slug):
    # Standard library only (project constraint), so this uses xml.etree
    # rather than defusedxml. Acceptable here: the only input is a job feed
    # fetched directly from the company's own personio.de subdomain over
    # HTTPS, not user-supplied XML.
    try:
        root = ET.fromstring(_get(f"https://{slug}.jobs.personio.de/xml").read())
    except ET.ParseError as e:
        raise BoardError(f"invalid XML from personio/{slug}") from e
    positions = list(root.iter("position"))
    # Fix vs. the original implementation: an XML document that parses fine
    # but lists zero <position> elements is a live, empty board, not a dead
    # one. Only a board that fails to answer at all (network error, bad XML,
    # wrong host) should raise -- see BoardError docstring above.
    out = []
    for p in positions:
        def field(tag):
            e = p.find(tag)
            return (e.text or "").strip() if e is not None else ""
        out.append({"title": field("name"), "location": field("office"),
                    "url": f"https://{slug}.jobs.personio.de/job/{field('id')}"})
    return out


FN = {
    "ashby": ashby,
    "greenhouse": greenhouse,
    "lever": lever,
    "personio": personio,
    "recruitee": recruitee,
    "smartrecruiters": smartrecruiters,
    "workable": workable,
}
