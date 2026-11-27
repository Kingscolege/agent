---
name: code-review-lead
description: Use when conducting comprehensive code reviews before merging, creating pull requests, or concluding major milestones. Coordinates multi-angle reviews to eliminate attention dilution.
---

# Code Review Lead: Multi-Angle Review Orchestrator

## Overview
A single-pass code review systematically suffers from **Attention Dilution**: the reviewer focuses on obvious stylistic or syntax issues while missing subtle concurrency bugs, security oversights, and performance bottlenecks.

`code-review-lead` decomposes code review into four independent, specialized review dimensions:

```
                  ┌────────────────────────┐
                  │    Code Review Lead    │
                  └───────────┬────────────┘
                              │
         ┌────────────┬───────┴────────┬─────────────┐
         ▼            ▼                ▼             ▼
    1. Logic &   2. Concurrency   3. Security   4. Performance
    Correctness    & State           Audit         Review
```

---

## When to Use
- Before opening a Pull Request or concluding a development branch
- After completing a multi-task implementation plan
- Before deploying changes to staging or production
- When conducting an architectural or security evaluation

---

## The Four Vertical Angles

### Angle 1: Logic & Correctness Review
- **Spec Compliance:** Does the diff implement all acceptance criteria without scope creep?
- **Edge Cases:** Are boundary conditions, empty collections, zero values, and error states handled?
- **Error Handling:** Are errors checked, wrapped with context, and never swallowed?

### Angle 2: Concurrency & State Management Review
- **Race Conditions:** Are shared in-memory data structures protected by mutexes/locks?
- **Resource Leaks:** Are file handles, database connections, sockets, and goroutines/threads properly closed?
- **State Stability:** In frontend code, are dependencies stable and effects clean?

### Angle 3: Security & Data Integrity Audit
- Follow `security-audit` skill.
- Check injection points (SQL, command, LDAP), unvalidated user inputs, authentication/authorization bypasses, hardcoded secrets, and SSRF.

### Angle 4: Performance & Resource Review
- **Complexity:** Are there accidental $O(N^2)$ loops or nested iterations over large datasets?
- **Memory & Allocation:** Are slices, buffers, or collections pre-allocated when size is known?
- **I/O Efficiency:** Are queries batched? Are there N+1 query patterns?

---

## Finding Classification & Severity

Every review finding MUST specify a severity:
- **`[CRITICAL]`**: Defect causing data loss, security vulnerability, crash, or spec violation. **Blocks completion immediately.**
- **`[IMPORTANT]`**: Structural defect, missing test, or performance hazard. Must be addressed or explicitly justified before completion.
- **`[MINOR]`**: Stylistic improvement, documentation suggestion, or refactoring opportunity. Optional.

See [review-checklists.md](./references/review-checklists.md) for the exhaustive checklist per category.
