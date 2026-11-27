#!/usr/bin/env python3
"""
Deslop Runner: Diff-scoped code cleanliness and anti-slop scanner.
Scans git diff for common AI coding agent anti-patterns.
"""
import subprocess
import re
import sys

SLOP_PATTERNS = [
    (r"\bas\s+any\b", "Type laundering: 'as any' bypasses type safety"),
    (r"\bas\s+unknown\s+as\b", "Double-cast type laundering: 'as unknown as'"),
    (r"@ts-ignore|@ts-nocheck", "TypeScript directive silencing type checker"),
    (r"#\s*type:\s*ignore", "Python type ignore suppression"),
    (r"#\s*(?:initialize|declare|return|loop|check)\b.*", "Comment narration stating obvious syntax"),
    (r"//\s*(?:initialize|declare|return|loop|check)\b.*", "Comment narration stating obvious syntax"),
    (r"except\s+Exception:\s*pass", "Empty catch block swallowing errors silently"),
    (r"catch\s*\([^)]*\)\s*\{\s*\}", "Empty catch block swallowing errors silently"),
    (r"//\s*TODO:\s*(?:implement|add\s+later)", "Unfinished placeholder comment"),
]

def main():
    # Get current git diff
    diff_targets = ["HEAD~1", "origin/main", "main"]
    diff_text = ""
    for target in ["", "HEAD~1"]:
        cmd = f"git diff {target}".strip()
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            diff_text = res.stdout
            break

    if not diff_text:
        # Check cached / staged diff
        res = subprocess.run("git diff --cached", shell=True, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            diff_text = res.stdout

    if not diff_text:
        print("✅ No active git diff found to inspect. Clean state.")
        sys.exit(0)

    lines = diff_text.splitlines()
    current_file = ""
    findings = []

    for line in lines:
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:].strip()
            for pattern, reason in SLOP_PATTERNS:
                if re.search(pattern, added_content, re.IGNORECASE):
                    findings.append((current_file, added_content, reason))

    if findings:
        print(f"⚠️  Deslop Scanner: Found {len(findings)} potential slop pattern(s) in active diff:\n")
        for f, content, reason in findings:
            print(f"  [{f}]")
            print(f"    Line:   {content[:80]}")
            print(f"    Issue:  {reason}\n")
        print("Action required: Review flagged hunks and clean up before proceeding to code review.")
        sys.exit(1)
    else:
        print("✨ Deslop Scanner: Git diff is clean of known AI slop patterns.")
        sys.exit(0)

if __name__ == "__main__":
    main()
