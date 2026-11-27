---
name: verification-before-completion
description: Use when about to claim any task, bugfix, or feature is complete, fixed, or passing. Requires executing fresh verification commands and quoting evidence.
---

# Verification Before Completion

## Core Principle
**Evidence before claims, always.**

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not executed the verification command and confirmed the output in your current interaction turn, you CANNOT claim the work is complete, fixed, or passing.

---

## The Verification Gate Function

Before stating that an issue is resolved, code is ready, or a task is finished:

```
1. IDENTIFY: What command deterministically proves the claim?
2. RUN:      Execute the FULL command fresh in the current turn via run_command.
3. READ:     Inspect the complete output, check the exit code (must be 0),
             and count passed/failed test cases.
4. EVALUATE: Does the command output unequivocally prove success?
             - If NO: State actual failure with error output and diagnose.
             - If YES: Quote the exact command, exit code, and test results.
5. CONCLUDE: Only now state that the task is complete.
```

---

## Prohibited Behaviors (Anti-Patterns)

- **Claiming success from past turns:** "As shown previously, tests passed." (Run it again fresh!)
- **Assuming success without execution:** "The code change is correct, so tests will pass now."
- **Hiding test output:** Reporting "All tests passed" without quoting the test runner summary.
- **Ignoring non-zero exit codes:** Treating a warning or partial failure as a pass.

---

## Required Completion Handoff Format

When declaring a task finished, your response MUST include:

```markdown
### 📋 Verification Summary

- **Verification Gate:** `./verify.sh` (or specific test command)
- **Exit Code:** `0`
- **Results:**
  ```text
  [Paste actual test runner summary, e.g. 42 passed in 1.24s]
  ```
- **Files Modified:** `path/to/file1.py`, `path/to/test1.py`
- **Remaining Risks / Follow-ups:** None (or explicitly listed)
```
