# Command: DEBUG (`/debug`)

**Syntax:**
- `DEBUG`
- `debug`
- `/debug`
- `DEBUG: <issue>` / `debug <issue>`

## Description
Activates the dedicated Systematic Debugging workflow without full feature planning overhead.

## Iron Law
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The 4 Debugging Phases
1. **Root Cause Investigation:** Read full stack traces, reproduce failure consistently, trace data flow backward to origin.
2. **Pattern Analysis:** Compare broken behavior with working code in the repository.
3. **Hypothesis Testing:** Test one variable at a time before touching production code.
4. **Minimal Fix & TDD:** Write failing regression test first, apply minimal fix, verify with `./verify.sh`.

## Visual Banner
```text
[DEBUG MODE ACTIVATED]
Workflow: Systematic Root-Cause Debugging
Owning Skill: systematic-debugging
Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Deactivation
Type `NORMAL` or `/normal` to return to standard AGY workflow.
