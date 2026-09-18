#!/usr/bin/env python3
"""Tests for classify.py, sweep.py and the db.py helpers they rely on.

No network access: any ATS call sweep.py would make is monkeypatched onto
ats.FN. No writes to the real db/: every write-touching test builds a
throwaway db/ under a temp directory and points db.DB / db.ROOT at it for
the duration of the test.

Run with: python3 -m unittest discover tools/tests
"""
import datetime
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ats
import classify
import db
import sweep


class TestClassify(unittest.TestCase):
    def test_cases(self):
        cases = [
            ("Chief of Staff", "strategy-operations", "unknown"),
            ("Junior Consultant", "consulting", "junior"),
            ("Marketing Coordinator", "communications-marketing", "unknown"),
            ("Regulatory Affairs Manager", "public-affairs-policy", "unknown"),
            ("Senior Software Engineer", "engineering", "senior"),
            ("VP of Public Affairs", "public-affairs-policy", "executive"),
            ("Graduate Trainee - Strategy & Operations", "strategy-operations", "graduate"),
            ("Head of Data Science", "data-ai", "lead"),
            ("Communications Intern", "communications-marketing", "intern"),
            ("", "other", "unknown"),
        ]
        for title, family, seniority in cases:
            with self.subTest(title=title):
                self.assertEqual(classify.classify(title), (family, seniority))

    def test_cli(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = classify.main(["classify.py", "Chief of Staff"])
        self.assertEqual(code, 0)
        self.assertEqual(buf.getvalue().strip(), "strategy-operations unknown")


class TestFilterMatching(unittest.TestCase):
    FILTER = {
        "title_regex": r"chief of staff|junior consultant",
        "exclude_title_regex": r"intern",
        "location_regex": r"brussels|remote",
        "keep_empty_location": True,
    }

    def test_title_and_location_match(self):
        p = {"title": "Chief of Staff", "location": "Remote"}
        self.assertTrue(sweep.matches_filter(p, self.FILTER))

    def test_title_matches_empty_location_kept(self):
        p = {"title": "Chief of Staff", "location": ""}
        self.assertTrue(sweep.matches_filter(p, self.FILTER))

    def test_location_mismatch_rejected(self):
        p = {"title": "Chief of Staff", "location": "Paris"}
        self.assertFalse(sweep.matches_filter(p, self.FILTER))

    def test_title_mismatch_rejected(self):
        p = {"title": "Software Engineer", "location": "Remote"}
        self.assertFalse(sweep.matches_filter(p, self.FILTER))

    def test_exclude_regex_rejected(self):
        p = {"title": "Chief of Staff Intern", "location": "Remote"}
        self.assertFalse(sweep.matches_filter(p, self.FILTER))

    def test_empty_location_dropped_without_keep_flag(self):
        f = dict(self.FILTER, keep_empty_location=False)
        p = {"title": "Chief of Staff", "location": ""}
        self.assertFalse(sweep.matches_filter(p, f))


class TempDB(unittest.TestCase):
    """Points db.DB / db.ROOT at a scratch directory for the duration of a
    test, with one company on a fake 'greenhouse' board and one filter.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="carriere-kit-test-")
        self.root = self.tmp
        self.dbdir = os.path.join(self.root, "db")
        os.makedirs(os.path.join(self.dbdir, "companies"))
        os.makedirs(os.path.join(self.dbdir, "postings"))
        os.makedirs(os.path.join(self.dbdir, "search-filters"))
        for name in ("job-titles.jsonl", "market-notes.jsonl", "sources.jsonl", "sweep-runs.jsonl"):
            open(os.path.join(self.dbdir, name), "w").close()

        company = {
            "id": "acme", "name": "Acme", "sector": "software-saas", "country": "BE",
            "sources": [{"type": "manual", "ref": "test", "seen_on": "2026-01-01"}],
            "ats": {"provider": "greenhouse", "slug": "acme", "status": "live", "checked_on": "2026-01-01"},
            "updated_on": "2026-01-01",
        }
        with open(os.path.join(self.dbdir, "companies", "software-saas.jsonl"), "w") as f:
            f.write(json.dumps(company) + "\n")

        filt = {
            "id": "test-filter", "description": "test filter", "title_regex": "chief of staff",
            "location_regex": "remote", "keep_empty_location": True, "updated_on": "2026-01-01",
        }
        with open(os.path.join(self.dbdir, "search-filters", "test-filter.json"), "w") as f:
            f.write(json.dumps(filt) + "\n")

        self._orig_root, self._orig_db = db.ROOT, db.DB
        db.ROOT, db.DB = self.root, self.dbdir
        db._company_cache = None
        self._orig_fn = dict(ats.FN)

    def tearDown(self):
        db.ROOT, db.DB = self._orig_root, self._orig_db
        db._company_cache = None
        ats.FN.clear()
        ats.FN.update(self._orig_fn)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read_postings(self):
        path = os.path.join(self.dbdir, "postings", "software-saas.jsonl")
        if not os.path.exists(path):
            return []
        with open(path, encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]

    def run_sweep(self, extra_args=()):
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with redirect_stdout(buf_out), redirect_stderr(buf_err):
            code = sweep.main(["sweep.py", "--filter", "test-filter", *extra_args])
        return code, buf_out.getvalue(), buf_err.getvalue()


class TestUpsertRecord(TempDB):
    def test_add_then_update_preserves_other_fields(self):
        action, rid, dest = db.upsert_record("company", {"id": "acme", "ats": {"provider": "greenhouse", "slug": "acme", "status": "empty", "checked_on": "2026-02-01"}})
        self.assertEqual(action, "updated")
        self.assertEqual(rid, "acme")
        recs = db.read(dest)
        rec = next(r for r in recs if r["id"] == "acme")
        self.assertEqual(rec["ats"]["status"], "empty")
        self.assertEqual(rec["name"], "Acme")  # untouched field survives the merge

    def test_invalid_record_raises_and_writes_nothing(self):
        with self.assertRaises(ValueError):
            db.upsert_record("company", {"id": "bad-co", "name": "Bad Co", "sector": "not-a-real-sector", "country": "BE", "sources": [], "updated_on": "2026-01-01"})
        self.assertNotIn("bad-co", db.company_index())


class TestSweepDiffAndClose(TempDB):
    def test_new_match_written_and_reported(self):
        ats.FN["greenhouse"] = lambda slug: [{"title": "Chief of Staff", "location": "Remote", "url": "https://example.com/job/1"}]
        code, out, err = self.run_sweep(["--diff"])
        self.assertEqual(code, 0)
        self.assertIn("https://example.com/job/1", out)
        self.assertIn("1 new", out)

        postings = self.read_postings()
        self.assertEqual(len(postings), 1)
        self.assertEqual(postings[0]["status"], "open")
        self.assertEqual(postings[0]["found_by"], "test-filter")
        self.assertEqual(postings[0]["family"], "strategy-operations")

    def test_second_run_same_posting_is_not_new(self):
        ats.FN["greenhouse"] = lambda slug: [{"title": "Chief of Staff", "location": "Remote", "url": "https://example.com/job/1"}]
        self.run_sweep()
        code, out, err = self.run_sweep(["--diff"])
        self.assertIn("0 new", out)
        self.assertIn("No new matches.", out)

    def test_posting_gone_from_board_is_closed(self):
        ats.FN["greenhouse"] = lambda slug: [{"title": "Chief of Staff", "location": "Remote", "url": "https://example.com/job/1"}]
        self.run_sweep()
        ats.FN["greenhouse"] = lambda slug: []  # board answers, lists nothing now
        self.run_sweep()
        postings = self.read_postings()
        self.assertEqual(len(postings), 1)
        self.assertEqual(postings[0]["status"], "closed")

    def test_dry_run_writes_nothing(self):
        ats.FN["greenhouse"] = lambda slug: [{"title": "Chief of Staff", "location": "Remote", "url": "https://example.com/job/1"}]
        self.run_sweep(["--dry-run"])
        self.assertEqual(self.read_postings(), [])

    def test_dead_board_reported_and_not_lost(self):
        def boom(slug):
            raise ats.BoardError("simulated outage")
        ats.FN["greenhouse"] = boom
        code, out, err = self.run_sweep()
        self.assertIn("acme", err)
        self.assertIn("boards dead", err)


class TestFreshness(unittest.TestCase):
    """A record only says what was true the day it was confirmed."""
    TODAY = datetime.date(2026, 9, 18)

    def test_age_from_the_confirmation_date(self):
        self.assertEqual(db.age_days({"last_seen": "2026-09-08"}, self.TODAY), 10)
        self.assertEqual(db.age_days({"ats": {"checked_on": "2026-08-19"}}, self.TODAY), 30)

    def test_never_confirmed_counts_as_stale(self):
        self.assertIsNone(db.age_days({"title": "x"}, self.TODAY))
        self.assertTrue(db.is_stale({"title": "x"}, self.TODAY))
        self.assertTrue(db.is_stale({"last_seen": "not-a-date"}, self.TODAY))

    def test_threshold(self):
        self.assertFalse(db.is_stale({"last_seen": "2026-08-01"}, self.TODAY, days=60))
        self.assertTrue(db.is_stale({"last_seen": "2026-07-01"}, self.TODAY, days=60))
        self.assertTrue(db.is_stale({"last_seen": "2026-09-01"}, self.TODAY, days=10))


if __name__ == "__main__":
    unittest.main()
