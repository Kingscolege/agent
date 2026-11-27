#!/usr/bin/env python3
"""
Setup & Quality Gate Readiness Auditor.
Validates if a target repository has all necessary gates, rules, and scripts configured.
Usage: python3 setup-check.py <target-dir>
"""
import sys
import os

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    target_dir = os.path.abspath(target_dir)

    print(f"Auditing repository setup at: {target_dir}")
    print("=" * 60)

    checks = []

    # 1. verify.sh gate
    verify_sh = os.path.join(target_dir, "verify.sh")
    if os.path.isfile(verify_sh):
        if os.access(verify_sh, os.X_OK):
            checks.append(("PASS", "Deterministic gate: verify.sh exists and is executable"))
        else:
            checks.append(("WARN", "verify.sh exists but is not executable (run chmod +x verify.sh)"))
    else:
        checks.append(("FAIL", "Missing verify.sh (run repo-scout.py --generate-verify to generate)"))

    # 2. AGENTS.md instructions
    agents_md = os.path.join(target_dir, "AGENTS.md")
    if os.path.isfile(agents_md):
        with open(agents_md, "r", errors="ignore") as f:
            content = f.read()
        if "<placeholder>" in content.lower() or "<project name>" in content.lower():
            checks.append(("FAIL", "AGENTS.md contains unpopulated template placeholders"))
        else:
            checks.append(("PASS", "Project AGENTS.md exists and is project-specific"))
    else:
        checks.append(("WARN", "Local AGENTS.md absent (universal AGENTS.md from engineering-agent-kit applies)"))

    # 3. Git repository state
    git_dir = os.path.join(target_dir, ".git")
    if os.path.isdir(git_dir):
        checks.append(("PASS", "Git version control active"))
    else:
        checks.append(("INFO", "Not a git root directory"))

    # Print summary
    failed = False
    for status, msg in checks:
        icon = "✅" if status == "PASS" else ("⚠️" if status in ["WARN", "INFO"] else "❌")
        print(f"{icon} [{status}] {msg}")
        if status == "FAIL":
            failed = True

    print("=" * 60)
    if failed:
        print("Setup Status: INCOMPLETE (Fix the failures above before commencing agent workflows)")
        sys.exit(1)
    else:
        print("Setup Status: READY FOR PRODUCTION ENGINEERING")
        sys.exit(0)

if __name__ == "__main__":
    main()
