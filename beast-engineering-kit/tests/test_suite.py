#!/usr/bin/env python3
"""
Comprehensive Quality Assurance & Regression Test Suite for Engineering Agent Kit.
Tests skill manifests, frontmatter, hook contracts, CLI scripts, and verification gates.
"""
import unittest
import os
import sys
import json
import subprocess
import tempfile
import shutil

PLUGIN_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "plugin"))
PY_BIN = os.environ.get("PYTHON") or sys.executable

class TestPluginManifestAndStructure(unittest.TestCase):
    """Validates plugin.json, rules/AGENTS.md, and hooks.json conform to AGY standards."""

    def test_plugin_json_schema(self):
        p = os.path.join(PLUGIN_ROOT, "plugin.json")
        self.assertTrue(os.path.isfile(p), "plugin.json must exist")
        with open(p, "r") as f:
            data = json.load(f)
        self.assertEqual(data.get("name"), "engineering-agent-kit")
        self.assertTrue(bool(data.get("displayName")))
        self.assertTrue(bool(data.get("version")))
        self.assertTrue(bool(data.get("description")))
        self.assertIsInstance(data.get("keywords"), list)
        self.assertGreater(len(data["keywords"]), 3)

    def test_agents_md_rules_budget(self):
        rules_path = os.path.join(PLUGIN_ROOT, "rules", "AGENTS.md")
        self.assertTrue(os.path.isfile(rules_path), "rules/AGENTS.md must exist")
        size = os.path.getsize(rules_path)
        # AGY hard limit is 24,000 bytes per rule file
        self.assertLess(size, 24000, f"AGENTS.md size ({size} bytes) exceeds AGY 24KB limit")
        with open(rules_path, "r") as f:
            content = f.read()
        self.assertIn("The Three Iron Laws", content)
        self.assertIn("systematic-debugging", content)
        self.assertIn("verification-before-completion", content)
        self.assertIn("test-driven-development", content)

    def test_hooks_json_validity(self):
        hooks_path = os.path.join(PLUGIN_ROOT, "hooks.json")
        self.assertTrue(os.path.isfile(hooks_path), "hooks.json must exist")
        with open(hooks_path, "r") as f:
            hooks = json.load(f)
        self.assertIn("engineering-safety-gate", hooks)
        self.assertIn("PreToolUse", hooks["engineering-safety-gate"])
        self.assertIn("engineering-session-bootstrap", hooks)
        self.assertIn("SessionStart", hooks["engineering-session-bootstrap"])
        self.assertIn("engineering-beast-mode", hooks)
        self.assertIn("PreInvocation", hooks["engineering-beast-mode"])


class TestSkillsSchemaAndFrontmatter(unittest.TestCase):
    """Ensures every skill has a valid SKILL.md with proper YAML frontmatter."""

    def setUp(self):
        self.skills_dir = os.path.join(PLUGIN_ROOT, "skills")
        self.expected_skills = [
            "systematic-debugging",
            "test-driven-development",
            "verification-before-completion",
            "spec-driven-development",
            "writing-plans",
            "executing-plans",
            "subagent-driven-development",
            "deslop",
            "code-review-lead",
            "security-audit",
            "repo-intelligence",
            "beast"
        ]

    def test_all_expected_skills_exist(self):
        present = os.listdir(self.skills_dir)
        for s in self.expected_skills:
            self.assertIn(s, present, f"Skill {s} missing from skills directory")

    def test_skill_frontmatter_and_content(self):
        for s in self.expected_skills:
            skill_md = os.path.join(self.skills_dir, s, "SKILL.md")
            self.assertTrue(os.path.isfile(skill_md), f"{skill_md} must exist")
            with open(skill_md, "r") as f:
                content = f.read()

            lines = content.splitlines()
            self.assertEqual(lines[0].strip(), "---", f"{s}/SKILL.md must start with --- frontmatter")

            # Extract frontmatter
            end_idx = -1
            for idx in range(1, len(lines)):
                if lines[idx].strip() == "---":
                    end_idx = idx
                    break
            self.assertGreater(end_idx, 1, f"{s}/SKILL.md frontmatter must be closed with ---")
            fm_text = "\n".join(lines[1:end_idx])

            self.assertIn(f"name: {s}", fm_text, f"{s}/SKILL.md name must match directory name")
            self.assertIn("description:", fm_text, f"{s}/SKILL.md must have description")
            self.assertTrue(
                "Use when" in fm_text or "use when" in fm_text.lower(),
                f"{s}/SKILL.md description should specify 'Use when...'"
            )


class TestLifecycleHookExecution(unittest.TestCase):
    """Validates hook execution contracts over stdin and stdout."""

    def test_pre_tool_safety_benign_command(self):
        cmd = [PY_BIN, os.path.join(PLUGIN_ROOT, "scripts", "pre-tool-safety.py")]
        payload = {
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "pytest tests/test_login.py"}
            }
        }
        proc = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        resp = json.loads(proc.stdout)
        self.assertEqual(resp.get("decision"), "allow")

    def test_pre_tool_safety_destructive_command(self):
        cmd = [PY_BIN, os.path.join(PLUGIN_ROOT, "scripts", "pre-tool-safety.py")]
        destructive_commands = [
            "rm -rf /",
            "rm -rf ~",
            "git reset --hard HEAD~1",
            "git clean -fdx",
            "psql -c 'DROP DATABASE production;'",
            "DROP TABLE users"
        ]
        for bad_cmd in destructive_commands:
            payload = {
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": bad_cmd}
                }
            }
            proc = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0)
            resp = json.loads(proc.stdout)
            self.assertEqual(
                resp.get("decision"),
                "force_ask",
                f"Destructive command '{bad_cmd}' should have been blocked with force_ask, got: {resp}"
            )

    def test_session_start_hook(self):
        cmd = [PY_BIN, os.path.join(PLUGIN_ROOT, "scripts", "session-start.py")]
        payload = {"workspacePaths": [PLUGIN_ROOT], "cwd": PLUGIN_ROOT}
        proc = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        resp = json.loads(proc.stdout)
        self.assertIn("injectSteps", resp)
        injected = resp["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("Engineering Agent Kit Active", injected)


class TestRepositoryScoutAndSetupAuditor(unittest.TestCase):
    """Tests the repo-scout and setup-check CLI tools against simulated repositories."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_repo_scout_python_detection(self):
        # Scaffold a mock python repo
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w") as f:
            f.write('[project]\nname = "test-pkg"\n\n[tool.ruff]\nline-length = 88\n\n[tool.pytest.ini_options]\n')
        with open(os.path.join(self.test_dir, "uv.lock"), "w") as f:
            f.write("# lockfile\n")

        scout_script = os.path.join(PLUGIN_ROOT, "scripts", "repo-scout.py")
        proc = subprocess.run([PY_BIN, scout_script, "--inspect", self.test_dir], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)

        self.assertIn("python", data["languages"])
        self.assertEqual(data["package_manager"], "uv")
        self.assertIn("ruff", data["linters"])
        self.assertIn("pytest", data["test_runners"])

    def test_repo_scout_generate_verify_and_agents(self):
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w") as f:
            f.write('[project]\nname = "demo"\n')
        with open(os.path.join(self.test_dir, "uv.lock"), "w") as f:
            f.write("")

        scout_script = os.path.join(PLUGIN_ROOT, "scripts", "repo-scout.py")
        proc = subprocess.run([PY_BIN, scout_script, "--all", self.test_dir], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)

        verify_sh = os.path.join(self.test_dir, "verify.sh")
        agents_md = os.path.join(self.test_dir, "AGENTS.md")
        self.assertTrue(os.path.isfile(verify_sh), "verify.sh should be generated")
        self.assertTrue(os.path.isfile(agents_md), "AGENTS.md should be generated")
        self.assertTrue(os.access(verify_sh, os.X_OK), "verify.sh should be executable")

        # Test setup-check on the generated repository
        check_script = os.path.join(PLUGIN_ROOT, "scripts", "setup-check.py")
        proc2 = subprocess.run([PY_BIN, check_script, self.test_dir], capture_output=True, text=True)
        self.assertEqual(proc2.returncode, 0, f"setup-check failed: {proc2.stdout} {proc2.stderr}")
        self.assertIn("READY FOR PRODUCTION ENGINEERING", proc2.stdout)

    def test_verify_runner_fails_closed_when_missing(self):
        empty_dir = tempfile.mkdtemp()
        try:
            runner_script = os.path.join(PLUGIN_ROOT, "scripts", "verify-runner.sh")
            proc = subprocess.run(["bash", runner_script, empty_dir], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0, "verify-runner must exit non-zero when verify.sh is missing")
            self.assertIn("FAIL CLOSED", proc.stderr)
        finally:
            shutil.rmtree(empty_dir, ignore_errors=True)


class TestDeslopScanner(unittest.TestCase):
    """Tests the deslop AI anti-slop pattern detector."""

    def test_deslop_regex_rules(self):
        from scripts.deslop_runner import SLOP_PATTERNS
        sample_code_with_slop = [
            ("const user = data as any;", "as any"),
            ("const value = x as unknown as string;", "as unknown as"),
            ("// TODO: implement later", "TODO"),
            ("except Exception: pass", "empty catch"),
        ]

        import re
        for code, expected_kw in sample_code_with_slop:
            matched = False
            for pattern, desc in SLOP_PATTERNS:
                if re.search(pattern, code, re.IGNORECASE):
                    matched = True
                    break
            self.assertTrue(matched, f"Pattern for '{expected_kw}' should have matched: '{code}'")


if __name__ == "__main__":
    unittest.main()
