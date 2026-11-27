#!/usr/bin/env python3
"""
Test Pollution Bisector.
Finds which test file pollutes shared state causing subsequent tests to fail.
Usage: python3 find-polluter.py <failing-test-target> <test-command-prefix>
"""
import sys
import subprocess
import glob
import os

def run_test(cmd):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return proc.returncode == 0

def main():
    if len(sys.argv) < 3:
        print("Usage: find-polluter.py <failing-test-target> <test-cmd-prefix>")
        print("Example: find-polluter.py tests/test_payment.py 'pytest'")
        sys.exit(2)

    victim = sys.argv[1]
    cmd_prefix = sys.argv[2]

    # Verify victim passes in isolation
    isolated_cmd = f"{cmd_prefix} {victim}"
    print(f"Checking if victim passes in isolation: {isolated_cmd}")
    if not run_test(isolated_cmd):
        print(f"Victim {victim} fails on its own! Not a test pollution issue.")
        sys.exit(1)
    print(f"Confirmed: {victim} passes in isolation.")

    # Find candidate test files
    candidates = []
    for root, _, files in os.walk("."):
        for f in files:
            if (f.startswith("test_") or f.endswith(("_test.py", ".test.ts", ".test.js", ".spec.ts", ".spec.js"))) and f != os.path.basename(victim):
                rel = os.path.relpath(os.path.join(root, f), ".")
                if not any(x in rel for x in ["node_modules", ".venv", "venv", ".git"]):
                    candidates.append(rel)

    print(f"Discovered {len(candidates)} candidate test files.")

    # Pairwise test to find polluter
    polluters = []
    for cand in candidates:
        pair_cmd = f"{cmd_prefix} {cand} {victim}"
        if not run_test(pair_cmd):
            print(f"🚨 FOUND POLLUTER: {cand} causes {victim} to fail!")
            polluters.append(cand)

    if polluters:
        print(f"\nPollution Summary: {len(polluters)} polluter(s) detected: {', '.join(polluters)}")
        sys.exit(0)
    else:
        print("No pairwise polluter found. Pollution may depend on a combination of 2+ files.")
        sys.exit(0)

if __name__ == "__main__":
    main()
