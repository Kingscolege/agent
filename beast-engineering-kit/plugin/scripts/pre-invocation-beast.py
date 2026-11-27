#!/usr/bin/env python3
"""
Pre-Invocation Hook for BEAST Engineering Kit.
Intercepts user input to detect BEAST, DEBUG, AUDIT, REVIEW, and NORMAL triggers,
injecting specialized engineering instructions and maintaining conversation persistence.
"""
import sys
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from beast_state import parse_trigger, activate_mode, deactivate_beast, get_active_mode

BANNERS = {
    "beast": """[BEAST MODE ACTIVATED]
Engineering Constitution: ACTIVE
Architecture-First: ACTIVE
Systematic Debugging: ACTIVE
TDD: ACTIVE
Independent Review: ACTIVE
Verification Gate: ACTIVE""",

    "debug": """[DEBUG MODE ACTIVATED]
Workflow: Systematic Root-Cause Debugging
Owning Skill: systematic-debugging
Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST""",

    "audit": """[AUDIT MODE ACTIVATED]
Workflow: Security Hardening & Deslop Cleanup
Owning Skills: security-audit, deslop
Standards: OWASP/CWE compliance, zero leaked secrets, zero AI slop""",

    "review": """[REVIEW MODE ACTIVATED]
Workflow: Multi-Angle Independent Code Review
Owning Skill: code-review-lead
Dimensions: Logic & Correctness, Concurrency, Security, Performance"""
}

WORKFLOW_INSTRUCTIONS = {
    "beast": """
### 🛡️ MANDATORY BEAST ENGINEERING WORKFLOW
Every coding task MUST strictly execute through the 12-step engineering lifecycle:
1. **Repository Reconnaissance:** Check project stack and verify gate (`repo-intelligence`).
2. **Requirements Analysis:** Establish clear Given/When/Then acceptance criteria (`spec-driven-development`).
3. **Root-Cause Investigation:** If fixing an issue, complete Phase 1 of `systematic-debugging` (no symptom fixes).
4. **Architecture & Impact Analysis:** Check invariants, ADRs, and backwards compatibility.
5. **Implementation Planning:** Break work into bite-sized verifiable tasks (`writing-plans`).
6. **Skill Discovery & Activation:** Explicitly load owning skills.
7. **Intelligent Agent Delegation:** Dispatch isolated subagents for multi-task plans (`subagent-driven-development`).
8. **Implementation via TDD:** Ironclad Red -> Green -> Refactor cycle (`test-driven-development`).
9. **Automated Validation:** Execute `./verify.sh` to deterministic zero-error pass.
10. **Independent Code Review:** Multi-angle review across Logic, Concurrency, Security, Perf (`code-review-lead`).
11. **Security & Anti-Slop:** Audit inputs/auth (`security-audit`) and strip AI slop (`deslop`).
12. **Verification Before Completion:** Execute fresh verification command and quote exit code + test output (`verification-before-completion`).

Display the [BEAST MODE ACTIVATED] banner prominently at start, and provide a concise completion report upon finishing.
""",

    "debug": """
### 🔍 DEBUG WORKFLOW ACTIVE (systematic-debugging)
Execute the 4-Phase Root-Cause Investigation:
1. **Root Cause:** Read full stack traces, reproduce failure consistently, trace data flow backward to origin.
2. **Pattern Analysis:** Compare broken behavior with working code in the repository.
3. **Hypothesis Testing:** Test one variable at a time before touching production code.
4. **Minimal Fix & TDD:** Write failing regression test first, apply minimal fix, verify with `./verify.sh`.
""",

    "audit": """
### 🔒 AUDIT WORKFLOW ACTIVE (security-audit & deslop)
Execute Comprehensive Security & Code Cleanliness Audit:
1. **Security Audit:** Inspect inputs, SQL/command injection, authentication, SSRF, secrets, and LLM boundaries.
2. **Deslop Pass:** Scrub comment narration, type-laundering (`as any`), empty try/catches, and unnecessary helpers.
""",

    "review": """
### 👓 CODE REVIEW WORKFLOW ACTIVE (code-review-lead)
Execute 4-Angle Independent Review:
1. **Logic & Correctness:** Verify spec compliance, edge cases, error propagation.
2. **Concurrency & State:** Check mutexes, race conditions, resource leaks, Goroutine/thread lifecycles.
3. **Security Audit:** Check OWASP top 10 vulnerabilities, injection points, permissions.
4. **Performance Review:** Algorithmic complexity, memory allocations, N+1 query patterns.
Report findings classified as [CRITICAL], [IMPORTANT], or [MINOR].
"""
}

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({}))
            return

        payload = json.loads(raw_input)
        conv_id = payload.get("conversationId", "default")
        user_input = payload.get("lastUserInput", "")

        trigger = parse_trigger(user_input)
        action = trigger["action"]
        mode = trigger.get("mode", "")
        task = trigger.get("task", "")

        if action == "activate":
            activate_mode(conv_id, mode, task)
            banner = BANNERS.get(mode, BANNERS["beast"])
            instructions = WORKFLOW_INSTRUCTIONS.get(mode, WORKFLOW_INSTRUCTIONS["beast"])

            if task:
                prompt_text = (
                    f"{banner}\n\n"
                    f"**Task Initiated under {mode.upper()} Mode:** `{task}`\n"
                    f"{instructions}"
                )
            else:
                prompt_text = (
                    f"{banner}\n\n"
                    f"{mode.upper()} mode is now ACTIVE for this conversation.\n"
                    f"Acknowledge activation by printing the exact banner above.\n"
                    f"All subsequent tasks in this session will follow this workflow.\n"
                    f"To return to normal mode at any time, type `NORMAL`."
                )
            resp = {
                "injectSteps": [
                    {
                        "systemMessage": {
                            "systemMessage": prompt_text
                        }
                    }
                ]
            }
            print(json.dumps(resp))
            return

        elif action == "deactivate":
            deactivate_beast(conv_id)
            deactivation_msg = (
                "[BEAST MODE DEACTIVATED]\n"
                "Engineering Constitution: STANDBY\n"
                "Returned to normal AGY workflow."
            )
            resp = {
                "injectSteps": [
                    {
                        "systemMessage": {
                            "systemMessage": deactivation_msg
                        }
                    }
                ]
            }
            print(json.dumps(resp))
            return

        active_mode = get_active_mode(conv_id)
        if active_mode:
            # Mode is persistently active for this conversation
            banner = BANNERS.get(active_mode, BANNERS["beast"])
            instructions = WORKFLOW_INSTRUCTIONS.get(active_mode, WORKFLOW_INSTRUCTIONS["beast"])
            prompt_text = (
                f"⚡ **{active_mode.upper()} MODE PERSISTENTLY ACTIVE**\n"
                f"{instructions}"
            )
            resp = {
                "injectSteps": [
                    {
                        "systemMessage": {
                            "systemMessage": prompt_text
                        }
                    }
                ]
            }
            print(json.dumps(resp))
            return

        # Normal mode
        print(json.dumps({}))

    except Exception as e:
        print(json.dumps({}))

if __name__ == "__main__":
    main()
