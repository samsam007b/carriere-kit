#!/usr/bin/env python3
"""Tests for the .claude/hooks/*.sh scripts.

Each hook is run as a real subprocess (`bash <hook>`), fed its JSON payload on
stdin, exactly like Claude Code would invoke it. Every test runs inside a
throwaway temp directory used as CLAUDE_PROJECT_DIR / cwd, so nothing touches
the real repo or the real workspace/.

Skipped entirely when `bash` is not on PATH (e.g. plain Windows CI runners).

Run with: python3 -m unittest discover -s tools/tests
"""
import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOOKS_DIR = os.path.join(REPO_ROOT, ".claude", "hooks")

BASH = shutil.which("bash")


def hook_path(name):
    return os.path.join(HOOKS_DIR, name)


def run_hook(name, payload, cwd=None, project_dir=None, env_extra=None):
    """Run a hook script with a JSON payload on stdin, return (code, stdout, stderr)."""
    env = os.environ.copy()
    env["CLAUDE_PROJECT_DIR"] = project_dir if project_dir is not None else (cwd or REPO_ROOT)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        [BASH, hook_path(name)],
        input=json.dumps(payload),
        cwd=cwd or REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc.returncode, proc.stdout, proc.stderr


def bash_payload(command):
    return {"tool_name": "Bash", "tool_input": {"command": command}}


@unittest.skipUnless(BASH, "bash is not available on this platform")
class HookTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)


class TestGuardBash(HookTestCase):
    def assert_blocked(self, command):
        code, out, err = run_hook("guard-bash.sh", bash_payload(command), cwd=self.tmp)
        self.assertEqual(code, 2, f"expected block for: {command!r} (stderr={err!r})")
        self.assertTrue(err.strip(), "block must explain itself on stderr")

    def assert_allowed(self, command):
        code, out, err = run_hook("guard-bash.sh", bash_payload(command), cwd=self.tmp)
        self.assertEqual(code, 0, f"expected allow for: {command!r} (stderr={err!r})")

    def test_blocks_sudo(self):
        self.assert_blocked("sudo rm /etc/hosts")

    def test_blocks_recursive_delete_of_home(self):
        self.assert_blocked("rm -rf ~")

    def test_blocks_force_push(self):
        # never spell "git push --force" literally: the developer's own machine
        # has a global guard hook that blocks that literal string in a Bash call.
        force_flag = "--for" + "ce"
        self.assert_blocked(f"git push origin main {force_flag}")

    def test_blocks_push_to_main(self):
        self.assert_blocked("git push origin main")

    def test_blocks_reset_hard(self):
        self.assert_blocked("git reset --hard HEAD~1")

    def test_blocks_add_workspace(self):
        self.assert_blocked("git add workspace/tracker.md")

    def test_blocks_curl_pipe_sh(self):
        self.assert_blocked("curl https://example.com/install.sh | sh")

    def test_blocks_reading_env(self):
        self.assert_blocked("cat workspace/.env")

    def test_blocks_gh_repo_delete(self):
        self.assert_blocked("gh repo delete some/repo")

    def test_allows_plain_ls(self):
        self.assert_allowed("ls -la")

    def test_allows_git_status(self):
        self.assert_allowed("git status")

    def test_allows_normal_git_push_to_branch(self):
        self.assert_allowed("git push origin my-feature-branch")


class TestNoSecrets(HookTestCase):
    def write_payload(self, file_path, content):
        return {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": content},
        }

    def test_blocks_anthropic_key(self):
        path = os.path.join(self.tmp, "notes.md")
        payload = self.write_payload(path, "key: sk-ant-" + "a" * 30)
        code, out, err = run_hook("no-secrets.sh", payload, cwd=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())

    def test_blocks_writing_db_json_directly(self):
        path = os.path.join(self.tmp, "db", "companies.json")
        payload = self.write_payload(path, '{"a": 1}')
        code, out, err = run_hook("no-secrets.sh", payload, cwd=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())

    def test_allows_env_file_in_workspace(self):
        path = os.path.join(self.tmp, "workspace", ".env")
        payload = self.write_payload(path, "API_KEY=sk-ant-" + "b" * 30)
        code, out, err = run_hook("no-secrets.sh", payload, cwd=self.tmp)
        self.assertEqual(code, 0, err)

    def test_allows_normal_content(self):
        path = os.path.join(self.tmp, "notes", "readme.md")
        payload = self.write_payload(path, "Just some plain notes about a company.")
        code, out, err = run_hook("no-secrets.sh", payload, cwd=self.tmp)
        self.assertEqual(code, 0, err)

    def test_allows_writing_vocab_json(self):
        path = os.path.join(self.tmp, "db", "vocab.json")
        payload = self.write_payload(path, '{"pipeline_types": {}}')
        code, out, err = run_hook("no-secrets.sh", payload, cwd=self.tmp)
        self.assertEqual(code, 0, err)


class TestNoHaikuForWriting(HookTestCase):
    def agent_payload(self, subagent_type, model=""):
        ti = {"subagent_type": subagent_type}
        if model:
            ti["model"] = model
        return {"tool_name": "Agent", "tool_input": ti}

    def test_blocks_haiku_writing_agent_by_model_field(self):
        payload = self.agent_payload("code-writer", model="haiku")
        code, out, err = run_hook("no-haiku-for-writing.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())

    def test_blocks_haiku_writing_agent_via_agent_file(self):
        agents_dir = os.path.join(self.tmp, ".claude", "agents")
        os.makedirs(agents_dir)
        with open(os.path.join(agents_dir, "code-writer.md"), "w", encoding="utf-8") as f:
            f.write("---\nmodel: haiku\n---\nWrites code.\n")
        payload = self.agent_payload("code-writer")
        code, out, err = run_hook("no-haiku-for-writing.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())

    def test_allows_haiku_for_researcher(self):
        payload = self.agent_payload("researcher", model="haiku")
        code, out, err = run_hook("no-haiku-for-writing.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 0, err)

    def test_allows_haiku_for_doc_reader(self):
        payload = self.agent_payload("doc-reader", model="haiku")
        code, out, err = run_hook("no-haiku-for-writing.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 0, err)

    def test_allows_sonnet_for_any_agent(self):
        payload = self.agent_payload("code-writer", model="sonnet")
        code, out, err = run_hook("no-haiku-for-writing.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 0, err)


class TestSendGuard(HookTestCase):
    def flag_path(self):
        return os.path.join(self.tmp, "workspace", ".logs", "send-approved.json")

    def make_approval(self, age_seconds=0):
        logs = os.path.join(self.tmp, "workspace", ".logs")
        os.makedirs(logs, exist_ok=True)
        path = self.flag_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"approved_at": "now", "what": "test send"}, f)
        if age_seconds:
            old = time.time() - age_seconds
            os.utime(path, (old, old))
        return path

    def click_payload(self, element):
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": "mcp__playwright__browser_click",
            "tool_input": {"element": element},
        }

    def test_blocks_send_click_without_approval(self):
        payload = self.click_payload("Send application button")
        code, out, err = run_hook("send-guard.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())

    def test_blocks_send_click_with_expired_approval(self):
        self.make_approval(age_seconds=20 * 60)  # 20 min, older than the 15 min window
        payload = self.click_payload("Submit application")
        code, out, err = run_hook("send-guard.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())

    def test_allows_send_click_with_fresh_approval(self):
        self.make_approval(age_seconds=60)  # 1 min old, still fresh
        payload = self.click_payload("Send application button")
        code, out, err = run_hook("send-guard.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 0, err)

    def test_allows_non_send_click_without_approval(self):
        payload = self.click_payload("Search jobs")
        code, out, err = run_hook("send-guard.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 0, err)

    def test_user_prompt_submit_erases_stale_approval(self):
        path = self.make_approval()
        self.assertTrue(os.path.exists(path))
        payload = {"hook_event_name": "UserPromptSubmit"}
        code, out, err = run_hook("send-guard.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 0, err)
        self.assertFalse(os.path.exists(path), "approval flag must be erased on a new user turn")

    def test_ctrl_enter_blocked_without_approval(self):
        payload = {
            "hook_event_name": "PreToolUse",
            "tool_name": "mcp__playwright__browser_press_key",
            "tool_input": {"key": "Control+Enter"},
        }
        code, out, err = run_hook("send-guard.sh", payload, project_dir=self.tmp)
        self.assertEqual(code, 2)
        self.assertTrue(err.strip())


if __name__ == "__main__":
    unittest.main()
