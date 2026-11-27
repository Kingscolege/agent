#!/usr/bin/env python3
"""
Session startup hook for Engineering Agent Kit.
Inspects workspace and injects the engineering constitution and verification readiness state.
"""
import sys
import json
import os

def main():
    try:
        raw_input = sys.stdin.read()
        cwd = os.getcwd()
        if raw_input.strip():
            try:
                payload = json.loads(raw_input)
                cwd = payload.get("cwd") or (payload.get("workspacePaths") or [cwd])[0]
            except Exception:
                pass

        has_verify = os.path.exists(os.path.join(cwd, "verify.sh")) or os.path.exists(os.path.join(cwd, ".agents", "verify.sh"))
        has_agents_md = os.path.exists(os.path.join(cwd, "AGENTS.md")) or os.path.exists(os.path.join(cwd, ".agents", "AGENTS.md"))

        status_notes = []
        if has_verify:
            status_notes.append("Local verification gate (`verify.sh`) detected.")
        else:
            status_notes.append("No `verify.sh` detected in project root. Run `repo-intelligence` skill to generate one.")

        if has_agents_md:
            status_notes.append("Project `AGENTS.md` active.")
        else:
            status_notes.append("Universal engineering constitution loaded from `engineering-agent-kit`.")

        system_msg = (
            "🛠️ **Engineering Agent Kit Active**\n\n"
            + "\n".join(f"- {note}" for note in status_notes) + "\n\n"
            "**Binding Laws for this session:**\n"
            "1. **Root Cause First:** Never guess or patch symptoms (`systematic-debugging`).\n"
            "2. **TDD Required:** No production code without a failing test first (`test-driven-development`).\n"
            "3. **Evidence Required:** Never claim completion without fresh command execution evidence (`verification-before-completion`).\n"
            "4. **Deslop:** Run diff-scoped cleanup before review (`deslop`)."
        )

        response = {
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": system_msg
                    }
                }
            ]
        }
        print(json.dumps(response))
    except Exception as e:
        print(json.dumps({
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": f"Engineering Agent Kit initialized. (Note: {e})"
                    }
                }
            ]
        }))

if __name__ == "__main__":
    main()
