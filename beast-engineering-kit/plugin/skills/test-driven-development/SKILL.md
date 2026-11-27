---
name: test-driven-development
description: Use when implementing any feature, bugfix, or behavior change before writing implementation code. Enforces the Red-Green-Refactor cycle.
---

# Test-Driven Development (TDD)

## Core Principle
Write the test first. Watch it fail. Write minimal code to pass. Refactor cleanly.

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you didn't watch the test fail, you do not know if it tests the right thing or if it was already passing by accident.

---

## When to Use
**Always:**
- New features and business logic
- Bug fixes and regression prevention
- API endpoint additions or changes
- Refactoring existing behavior

**Exceptions (confirm with user first):**
- Throwaway one-off exploratory scripts
- Pure documentation edits
- Static markdown or asset files

---

## The TDD Cycle: RED -> GREEN -> REFACTOR

```
       ┌────────────────────────┐
       ▼                        │
   1. RED: Write test           │
   Watch it FAIL with           │
   expected error               │
       │                        │
       ▼                        │
   2. GREEN: Write MINIMAL code │
   Watch it PASS                │
       │                        │
       ▼                        │
   3. REFACTOR: Clean code      │
   Keep all tests GREEN ────────┘
```

### Phase 1: RED (Failing Test)
1. Write a focused, isolated test covering the single behavior or bug in question.
2. Run the test command via `run_command`.
3. **VERIFY FAILURE:**
   - Confirm the test exits non-zero.
   - Confirm the failure reason is the *intended missing behavior*, NOT a syntax error, import failure, or test setup glitch.
   - If the test passes immediately, your test is invalid or the behavior already exists. Fix the test!

### Phase 2: GREEN (Minimal Implementation)
1. Write the *minimal amount of code* required to make the failing test pass.
2. Do not write ahead of the tests or implement speculative edge cases yet.
3. Run the test command again.
4. Verify the test exits `0` with all assertions satisfied.

### Phase 3: REFACTOR (Maintain Quality)
1. Clean up implementation:
   - Remove duplication.
   - Improve variable naming and control flow.
   - Ensure types and docstrings adhere to project standards.
2. Run `./verify.sh` to confirm that all tests remain green and no regressions were introduced.

---

## Framework Commands Reference

- **Python (pytest):** `pytest tests/test_feature.py -k "test_name" -v`
- **Node / TypeScript (vitest/jest):** `npm test -- tests/feature.test.ts`
- **Go:** `go test -v -run TestFeature ./pkg/...`
- **Rust:** `cargo test test_feature`
