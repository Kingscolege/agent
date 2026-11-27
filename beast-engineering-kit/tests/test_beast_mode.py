#!/usr/bin/env python3
"""
Automated Test Suite for BEAST Mode Activation & Engineering Workflow.
Validates trigger recognition, persistence, deactivation, and non-interference with normal mode.
"""
import unittest
import os
import sys
import json
import subprocess
import tempfile
import shutil

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "plugin"))
SCRIPTS_DIR = os.path.join(PLUGIN_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from beast_state import parse_trigger, activate_beast, deactivate_beast, is_beast_active

PY_BIN = os.environ.get("PYTHON") or sys.executable

class TestBeastTriggerRecognition(unittest.TestCase):
    """Tests case-insensitive trigger recognition for BEAST, beast, /beast, and NORMAL."""

    def test_uppercase_beast_recognition(self):
        res = parse_trigger("BEAST")
        self.assertEqual(res["action"], "activate")
        self.assertEqual(res["task"], "")

        # Padded with spaces
        res2 = parse_trigger("   BEAST   ")
        self.assertEqual(res2["action"], "activate")

    def test_lowercase_beast_recognition(self):
        res = parse_trigger("beast")
        self.assertEqual(res["action"], "activate")
        self.assertEqual(res["task"], "")

        # Mixed case
        res2 = parse_trigger("Beast")
        self.assertEqual(res2["action"], "activate")

    def test_slash_beast_recognition(self):
        res = parse_trigger("/beast")
        self.assertEqual(res["action"], "activate")
        self.assertEqual(res["mode"], "beast")

        res2 = parse_trigger("/BEAST")
        self.assertEqual(res2["action"], "activate")

    def test_specialized_triggers(self):
        # DEBUG
        res_dbg = parse_trigger("DEBUG")
        self.assertEqual(res_dbg["action"], "activate")
        self.assertEqual(res_dbg["mode"], "debug")

        # AUDIT
        res_aud = parse_trigger("/audit")
        self.assertEqual(res_aud["action"], "activate")
        self.assertEqual(res_aud["mode"], "audit")

        # REVIEW
        res_rev = parse_trigger("review: check auth PR")
        self.assertEqual(res_rev["action"], "activate")
        self.assertEqual(res_rev["mode"], "review")
        self.assertEqual(res_rev["task"], "check auth PR")

    def test_beast_followed_by_task(self):
        # Colon separator
        res1 = parse_trigger("BEAST: fix the database connection pool leak")
        self.assertEqual(res1["action"], "activate")
        self.assertEqual(res1["task"], "fix the database connection pool leak")

        # Space separator
        res2 = parse_trigger("beast implement OAuth2 token refresh flow")
        self.assertEqual(res2["action"], "activate")
        self.assertEqual(res2["task"], "implement OAuth2 token refresh flow")

        # Dash separator
        res3 = parse_trigger("/beast - refactor authentication middleware")
        self.assertEqual(res3["action"], "activate")
        self.assertEqual(res3["task"], "refactor authentication middleware")

    def test_normal_deactivation_trigger(self):
        res1 = parse_trigger("NORMAL")
        self.assertEqual(res1["action"], "deactivate")

        res2 = parse_trigger("normal")
        self.assertEqual(res2["action"], "deactivate")

        res3 = parse_trigger("/normal")
        self.assertEqual(res3["action"], "deactivate")

    def test_normal_mode_unaffected(self):
        # Arbitrary questions or sentences containing 'beast' in other positions
        regular_prompts = [
            "What is the capital of France?",
            "How do I split a string in Python?",
            "The beast was hiding in the dark woods.",
            "Can you explain the beast mode concept?",
            "git status"
        ]
        for prompt in regular_prompts:
            res = parse_trigger(prompt)
            self.assertEqual(
                res["action"],
                "none",
                f"Prompt '{prompt}' should not trigger BEAST mode activation, got: {res}"
            )


class TestBeastPersistenceAndLifecycleHook(unittest.TestCase):
    """Tests end-to-end hook execution, conversation persistence, and deactivation."""

    def setUp(self):
        self.test_conv_id = f"test-conv-{os.getpid()}-{tempfile.mktemp()}"
        self.hook_script = os.path.join(SCRIPTS_DIR, "pre-invocation-beast.py")

    def tearDown(self):
        deactivate_beast(self.test_conv_id)

    def _call_hook(self, conv_id: str, user_input: str) -> dict:
        payload = {
            "conversationId": conv_id,
            "lastUserInput": user_input,
            "workspacePaths": [PLUGIN_ROOT],
            "cwd": PLUGIN_ROOT
        }
        proc = subprocess.run(
            [PY_BIN, self.hook_script],
            input=json.dumps(payload),
            capture_output=True,
            text=True
        )
        self.assertEqual(proc.returncode, 0, f"Hook failed: {proc.stderr}")
        out = proc.stdout.strip()
        return json.loads(out) if out else {}

    def test_activation_banner_emitted_on_beast(self):
        resp = self._call_hook(self.test_conv_id, "BEAST")
        self.assertIn("injectSteps", resp)
        injected = resp["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("[BEAST MODE ACTIVATED]", injected)
        self.assertIn("Engineering Constitution: ACTIVE", injected)
        self.assertIn("Architecture-First: ACTIVE", injected)
        self.assertIn("Systematic Debugging: ACTIVE", injected)
        self.assertIn("TDD: ACTIVE", injected)
        self.assertIn("Independent Review: ACTIVE", injected)
        self.assertIn("Verification Gate: ACTIVE", injected)

    def test_beast_with_task_execution(self):
        task_desc = "Implement high-throughput Kafka producer with exponential backoff"
        resp = self._call_hook(self.test_conv_id, f"beast: {task_desc}")
        self.assertIn("injectSteps", resp)
        injected = resp["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("[BEAST MODE ACTIVATED]", injected)
        self.assertIn(task_desc, injected)
        self.assertIn("12-step engineering lifecycle", injected.lower())

    def test_persistence_across_multiple_turns(self):
        # Turn 1: Activate BEAST
        resp1 = self._call_hook(self.test_conv_id, "BEAST")
        self.assertIn("[BEAST MODE ACTIVATED]", resp1["injectSteps"][0]["systemMessage"]["systemMessage"])

        # Turn 2: Subsequent request without typing BEAST again
        resp2 = self._call_hook(self.test_conv_id, "Now add the schema validation for user accounts")
        self.assertIn("injectSteps", resp2)
        injected2 = resp2["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("BEAST MODE PERSISTENTLY ACTIVE", injected2)
        self.assertIn("12-step", injected2.lower())

        # Turn 3: Another subsequent request
        resp3 = self._call_hook(self.test_conv_id, "Run the verify.sh gate")
        self.assertIn("injectSteps", resp3)
        injected3 = resp3["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("BEAST MODE PERSISTENTLY ACTIVE", injected3)

    def test_deactivation_returns_to_normal(self):
        # Activate
        self._call_hook(self.test_conv_id, "BEAST")
        self.assertTrue(is_beast_active(self.test_conv_id))

        # Deactivate
        resp_deact = self._call_hook(self.test_conv_id, "NORMAL")
        self.assertIn("injectSteps", resp_deact)
        injected = resp_deact["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("[BEAST MODE DEACTIVATED]", injected)
        self.assertFalse(is_beast_active(self.test_conv_id))

        # Subsequent turn is normal mode
        resp_after = self._call_hook(self.test_conv_id, "What is the weather today?")
        self.assertEqual(resp_after, {})

    def test_unactivated_conversation_remains_normal(self):
        clean_conv = f"clean-conv-{os.getpid()}"
        resp = self._call_hook(clean_conv, "Can you help me write a quick sorting algorithm?")
        self.assertEqual(resp, {}, "Normal mode conversation must emit empty injectSteps")


class TestBeastSkillAndRulesIntegration(unittest.TestCase):
    """Verifies that the beast skill and AGENTS.md routing are correctly installed and compliant."""

    def test_beast_skill_md_exists_and_valid(self):
        skill_path = os.path.join(PLUGIN_ROOT, "skills", "beast", "SKILL.md")
        self.assertTrue(os.path.isfile(skill_path), "skills/beast/SKILL.md must exist")
        with open(skill_path, "r") as f:
            content = f.read()
        self.assertTrue(content.startswith("---"))
        self.assertIn("name: beast", content)
        self.assertIn("description:", content)
        self.assertIn("[BEAST MODE ACTIVATED]", content)
        self.assertIn("12-Step Mandatory Engineering Workflow", content)

    def test_agents_md_routing_includes_beast(self):
        agents_md = os.path.join(PLUGIN_ROOT, "rules", "AGENTS.md")
        with open(agents_md, "r") as f:
            content = f.read()
        self.assertIn("BEAST", content)
        self.assertIn("`beast`", content)
        self.assertIn("NORMAL", content)


if __name__ == "__main__":
    unittest.main()
