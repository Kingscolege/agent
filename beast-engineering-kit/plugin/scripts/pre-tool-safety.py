#!/usr/bin/env python3
"""
Pre-tool execution safety guard for Engineering Agent Kit.
Audits run_command arguments on stdin to block destructive or irreversible operations.
"""
import sys
import json
import re

DESTRUCTIVE_PATTERNS = [
    (r"\brm\s+-(?:rf|fr|r)\s+(?:/|~|\.\.?/\*|\*)", "Recursive root, home, or wildcard deletion"),
    (r"\bgit\s+reset\s+--hard\b", "Hard git reset which may discard uncommitted changes"),
    (r"\bgit\s+clean\s+-(?:f|fd|fdx|xdf)\b", "Git clean which deletes untracked repository files"),
    (r"\b(?:drop\s+database|drop\s+table|truncate\s+table)\b", "Database destruction command"),
    (r"\bmkfs\b|\bdd\s+if=.*of=/dev/", "Raw disk write or formatting operation"),
]

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        if tool_name == "run_command":
            cmd = args.get("CommandLine", "")
            cmd_lower = cmd.lower()

            for pattern, desc in DESTRUCTIVE_PATTERNS:
                if re.search(pattern, cmd_lower):
                    response = {
                        "decision": "force_ask",
                        "reason": f"Safety Gate: Potentially destructive command detected ({desc}): `{cmd}`. User confirmation required."
                    }
                    print(json.dumps(response))
                    return

        # Default allow
        print(json.dumps({"decision": "allow"}))
    except Exception as e:
        # Fail safe
        print(json.dumps({"decision": "allow", "reason": f"Safety check error: {str(e)}"}))

if __name__ == "__main__":
    main()
