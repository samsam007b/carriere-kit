#!/usr/bin/env python3
"""Tests for tracker.py. Runs entirely in temp directories, no real workspace/ touched.

Run with: python3 -m unittest tools/tests/test_tracker.py
"""
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tracker

HEADER = tracker.HEADER
SEP = "|---|---|---|---|---|---|---|"

VOCAB = {
    "pipeline_types": {"application": {}, "outreach": {}, "lead": {}, "research-round": {}, "project": {}},
    "pipeline_status": {"todo": {}, "active": {}, "waiting": {}, "offer": {}, "parked": {}, "closed": {}, "rejected": {}},
}


def row(lead, type_="application", status="waiting", submitted="2026-01-01",
        followup="2026-01-15", action="Sent", source="workspace/applications/x/README.md"):
    return f"| {lead} | {type_} | {status} | {submitted} | {followup} | {action} | {source} |"


class TrackerTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.ws = os.path.join(self.tmp, "workspace")
        os.makedirs(self.ws)
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        # keep tests independent of the real db/vocab.json content
        self._orig_load_vocab = tracker.load_vocab
        tracker.load_vocab = lambda: VOCAB

    def tearDown(self):
        tracker.load_vocab = self._orig_load_vocab

    def write_tracker(self, rows, path=None):
        path = path or os.path.join(self.ws, "tracker.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Tracker\n\n")
            f.write(HEADER + "\n")
            f.write(SEP + "\n")
            for r in rows:
                f.write(r + "\n")
        return path

    def run_cmd(self, args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = tracker.main(args)
        return code, out.getvalue(), err.getvalue()


class TestTemplates(TrackerTestCase):
    def test_fresh_templates_lint_clean(self):
        # the placeholder rows escape their pipes (\|): a fresh workspace must not fail lint
        tpl = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "templates")
        for name in ("tracker.md", "tracker-archive.md"):
            shutil.copyfile(os.path.join(tpl, name), os.path.join(self.ws, name))
        code, _, err = self.run_cmd(["--workspace", self.ws, "lint"])
        self.assertEqual(code, 0, err)


class TestFollowups(TrackerTestCase):
    def test_overdue_due_missing(self):
        self.write_tracker([
            row("Overdue Corp", followup="2020-01-01"),
            row("Due Today Inc", followup=tracker.dt.date.today().isoformat()),
            row("No Date Ltd", followup="-"),
            row("Active One", status="active", followup="2020-01-01"),  # not waiting, ignored
        ])
        code, out, err = self.run_cmd(["followups", "--workspace", self.ws])
        self.assertEqual(code, 0)
        self.assertIn("Overdue Corp", out)
        self.assertIn("Due Today Inc", out)
        self.assertIn("No Date Ltd", out)
        self.assertNotIn("Active One", out)

    def test_nothing_to_follow_up(self):
        self.write_tracker([])
        code, out, err = self.run_cmd(["followups", "--workspace", self.ws])
        self.assertEqual(code, 0)
        self.assertIn("Nothing to follow up on.", out)


class TestCheck(TrackerTestCase):
    def test_known_in_tracker(self):
        self.write_tracker([row("Roland Berger")])
        code, out, err = self.run_cmd(["check", "roland-berger", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("KNOWN", out)
        self.assertIn("Roland Berger", out)

    def test_known_in_archive(self):
        self.write_tracker([], path=os.path.join(self.ws, "tracker.md"))
        self.write_tracker([row("Warren")], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["check", "WARREN", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("KNOWN", out)

    def test_known_in_applications_folder(self):
        self.write_tracker([])
        os.makedirs(os.path.join(self.ws, "applications", "acme-corp"))
        code, out, err = self.run_cmd(["check", "Acme Corp", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("KNOWN", out)

    def test_new_name(self):
        self.write_tracker([row("Roland Berger")])
        code, out, err = self.run_cmd(["check", "Totally New Company", "--workspace", self.ws])
        self.assertEqual(code, 0)
        self.assertIn("new", out)

    def test_accent_and_punctuation_normalisation(self):
        self.write_tracker([row("Deloitte")])
        code, out, err = self.run_cmd(["check", "  DEloitté  ", "--workspace", self.ws])
        self.assertEqual(code, 1)


class TestLint(TrackerTestCase):
    def test_clean_file_passes(self):
        self.write_tracker([row("Acme")])
        self.write_tracker([], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["lint", "--workspace", self.ws])
        self.assertEqual(code, 0)
        self.assertIn("OK", err)

    def test_bad_header_fails(self):
        path = os.path.join(self.ws, "tracker.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("| Lead | Type | Status |\n|---|---|---|\n")
        self.write_tracker([], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["lint", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("does not match", err)

    def test_bad_type_and_status_fail(self):
        self.write_tracker([row("Acme", type_="nonsense", status="halfway")])
        self.write_tracker([], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["lint", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("type 'nonsense'", err)
        self.assertIn("status 'halfway'", err)

    def test_bad_date_fails(self):
        self.write_tracker([row("Acme", submitted="14/01/2026")])
        self.write_tracker([], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["lint", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("not YYYY-MM-DD", err)

    def test_waiting_without_followup_fails(self):
        self.write_tracker([row("Acme", status="waiting", followup="-")])
        self.write_tracker([], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["lint", "--workspace", self.ws])
        self.assertEqual(code, 1)
        self.assertIn("requires a Follow-up date", err)

    def test_template_placeholder_row_ignored(self):
        self.write_tracker([row("{{Company}}", type_="{{type}}", status="{{status}}",
                                 submitted="{{date}}", followup="{{date}}")])
        self.write_tracker([], path=os.path.join(self.ws, "tracker-archive.md"))
        code, out, err = self.run_cmd(["lint", "--workspace", self.ws])
        self.assertEqual(code, 0)


class TestNorm(unittest.TestCase):
    def test_norm_collapses_accents_case_punctuation(self):
        self.assertEqual(tracker.norm("Roland-Berger"), tracker.norm("roland berger"))
        self.assertEqual(tracker.norm("Déloitté"), tracker.norm("deloitte"))


if __name__ == "__main__":
    unittest.main()
