#!/usr/bin/env python3
"""
Automated tests for BEAST installer and uninstaller lifecycle.
Validates clean installation, backup behavior, and safe uninstallation.
"""
import unittest
import os
import sys
import tempfile
import shutil
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTALLER_SH = os.path.join(REPO_ROOT, "installers", "install.sh")
UNINSTALLER_SH = os.path.join(REPO_ROOT, "installers", "uninstall.sh")

class TestInstallerLifecycle(unittest.TestCase):
    """Tests installation, idempotency, backup, and uninstallation in isolated environments."""

    def setUp(self):
        self.test_home = tempfile.mkdtemp()
        self.env = os.environ.copy()
        self.env["HOME"] = self.test_home
        self.env["XDG_CONFIG_HOME"] = os.path.join(self.test_home, ".config")
        self.expected_dest = os.path.join(self.test_home, ".gemini", "config", "plugins", "engineering-agent-kit")

    def tearDown(self):
        shutil.rmtree(self.test_home, ignore_errors=True)

    def test_installer_fresh_install(self):
        proc = subprocess.run(["bash", INSTALLER_SH], env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Installer failed: {proc.stdout}\n{proc.stderr}")
        self.assertTrue(os.path.isdir(self.expected_dest), "Plugin directory was not created")
        self.assertTrue(os.path.isfile(os.path.join(self.expected_dest, "plugin.json")))
        self.assertTrue(os.path.isfile(os.path.join(self.expected_dest, "hooks.json")))
        self.assertTrue(os.path.isfile(os.path.join(self.expected_dest, "rules", "AGENTS.md")))
        self.assertTrue(os.path.isfile(os.path.join(self.expected_dest, "skills", "beast", "SKILL.md")))

    def test_installer_idempotency_and_backup(self):
        # First install
        proc1 = subprocess.run(["bash", INSTALLER_SH], env=self.env, capture_output=True, text=True)
        self.assertEqual(proc1.returncode, 0)

        # Place a canary file in the installed dir
        canary = os.path.join(self.expected_dest, "canary.txt")
        with open(canary, "w") as f:
            f.write("canary")

        # Second install (upgrade/re-install)
        proc2 = subprocess.run(["bash", INSTALLER_SH], env=self.env, capture_output=True, text=True)
        self.assertEqual(proc2.returncode, 0)
        self.assertTrue(os.path.isdir(self.expected_dest))

        # Verify a backup was created containing the canary
        parent = os.path.dirname(self.expected_dest)
        backups = [d for d in os.listdir(parent) if "engineering-agent-kit.bak" in d]
        self.assertGreaterEqual(len(backups), 1, "Backup directory was not created during re-install")
        backup_canary = os.path.join(parent, backups[0], "canary.txt")
        self.assertTrue(os.path.isfile(backup_canary), "Canary file should exist inside backup")

    def test_uninstaller_lifecycle(self):
        # Install first
        subprocess.run(["bash", INSTALLER_SH], env=self.env, capture_output=True, text=True)
        self.assertTrue(os.path.isdir(self.expected_dest))

        # Uninstall
        proc = subprocess.run(["bash", UNINSTALLER_SH], env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Uninstaller failed: {proc.stdout}\n{proc.stderr}")
        self.assertFalse(os.path.isdir(self.expected_dest), "Plugin directory should be removed")

        # Verify uninstaller archive exists
        parent = os.path.dirname(self.expected_dest)
        archives = [d for d in os.listdir(parent) if "engineering-agent-kit.uninstalled" in d]
        self.assertGreaterEqual(len(archives), 1, "Uninstaller archive should exist")

if __name__ == "__main__":
    unittest.main()
