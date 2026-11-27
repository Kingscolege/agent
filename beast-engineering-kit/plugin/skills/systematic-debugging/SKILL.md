---
name: systematic-debugging
description: Use when encountering any bug, test failure, exception, crash, or unexpected behavior before proposing or applying fixes. Enforces root-cause investigation before code modification.
---

# Systematic Debugging

## Core Principle
**ALWAYS find root cause before attempting fixes. Symptom fixes are failure.**

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you have not completed Phase 1, you CANNOT propose or apply code changes.

---

## When to Use
Use for ANY technical issue:
- Test failures (unit, integration, e2e)
- Runtime exceptions, crashes, or unhandled rejections
- Unexpected state, incorrect output, or silent data corruption
- Performance degradation or memory leaks
- Build, packaging, or dependency errors

---

## The Four Phases

You MUST complete each phase in order before proceeding to the next.

### Phase 1: Root Cause Investigation

Before modifying any file:
1. **Read Error Messages & Stack Traces Completely:**
   - Note exact error types, messages, file paths, and line numbers.
   - Do not skip warnings or preceding logs.
2. **Reproduce Consistently:**
   - Establish the exact minimal command or script to trigger the failure.
   - If flaky or non-deterministic, isolate environmental variables or use `scripts/find-polluter.py` to identify test pollution.
3. **Trace Data Flow Backward:**
   - Where did the bad value or null reference enter?
   - Trace callers up the call stack until you locate the source defect.
   - See [root-cause-tracing.md](./references/root-cause-tracing.md) for data flow tracing techniques.
4. **Isolate Component Boundaries:**
   - In multi-layer systems (e.g. Controller -> Service -> Database, or CLI -> Process -> IPC):
   - Add temporary diagnostic instrumentation at each boundary to inspect inputs and outputs.
   - Pinpoint the exact layer where reality diverges from expectation before writing the fix.

### Phase 2: Pattern Analysis

1. **Find Working Examples:**
   - Search the codebase for similar components, queries, or functions that work correctly.
2. **Compare Against Reference:**
   - List every difference between the broken code and the working pattern.
   - Do not assume "that difference couldn't matter."
3. **Check Recent Commits / Changes:**
   - Run `git diff` or inspect recent git history to see what was touched when the regression began.

### Phase 3: Hypothesis Formulation & Verification

1. **Formulate a Testable Hypothesis:**
   - State clearly: *"The failure occurs because X is causing Y under condition Z."*
2. **Test One Variable at a Time:**
   - Verify the hypothesis by testing the specific condition without making broad architectural changes.
   - If the hypothesis is disproven, return to Phase 1. Do not push speculative edits.

### Phase 4: Minimal Implementation & Regression Test

1. **Write a Failing Regression Test First:**
   - Follow `test-driven-development` to capture the failure in an automated test.
2. **Apply the Minimal Root-Cause Fix:**
   - Fix the defect at the source, not at the symptom site.
   - Do not add defensive `try/catch` wrappers or arbitrary fallback null checks to suppress errors.
3. **Verify Clean Fix:**
   - Run `./verify.sh` to confirm the regression test passes and no existing tests broke.
