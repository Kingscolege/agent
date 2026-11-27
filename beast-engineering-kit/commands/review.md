# Command: REVIEW (`/review`)

**Syntax:**
- `REVIEW`
- `review`
- `/review`
- `REVIEW: <PR / commit / branch>` / `review <PR / commit / branch>`

## Description
Activates the Multi-Angle Independent Code Review workflow to eliminate attention dilution before merging.

## The Four Vertical Angles
1. **Logic & Correctness:** Spec compliance, edge cases, off-by-one errors, error propagation.
2. **Concurrency & State:** Mutex locks, race conditions, resource leaks, Goroutine/thread cancellation.
3. **Security Audit:** Vulnerability scan across OWASP/CWE top categories.
4. **Performance Review:** Algorithmic complexity, memory allocations, N+1 queries.

## Finding Classifications
- `[CRITICAL]`: Must fix immediately; blocks merge.
- `[IMPORTANT]`: Must fix or explicitly justify before completion.
- `[MINOR]`: Optional refinement or suggestion.

## Visual Banner
```text
[REVIEW MODE ACTIVATED]
Workflow: Multi-Angle Independent Code Review
Owning Skill: code-review-lead
Dimensions: Logic & Correctness, Concurrency, Security, Performance
```

## Deactivation
Type `NORMAL` or `/normal` to return to standard AGY workflow.
