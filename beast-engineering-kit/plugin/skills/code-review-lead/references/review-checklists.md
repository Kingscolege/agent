# Exhaustive Review Checklists by Dimension

## 1. Logic & Correctness Checklist
- [ ] Inputs are validated at the perimeter before passing to domain services.
- [ ] Return values and error types match the declared function signatures.
- [ ] Off-by-one errors in loops, ranges, and array slices are absent.
- [ ] Fallback branches in `switch` or `if/else` handle unexpected inputs gracefully.
- [ ] Idempotency is preserved where network operations may retry.

## 2. Concurrency & State Checklist
- [ ] In Go/Rust/Java: Goroutines/threads have clean cancellation signals via `context.Context` or channels.
- [ ] Shared maps, arrays, or counters accessed across threads use synchronization primitives (mutex, atomic, concurrent map).
- [ ] Mutex unlocks use `defer` or RAII to guarantee release even during panics or exceptions.
- [ ] In React/Frontend: `useEffect` dependencies do not create infinite re-renders or stale closures.

## 3. Security Checklist
- [ ] All database queries use parameterized statements; zero string interpolation into SQL.
- [ ] System commands executed via subprocess or shell sanitize arguments; user input is never passed directly to `sh -c`.
- [ ] Sensitive tokens, passwords, API keys, or private keys are not hardcoded or logged.
- [ ] File paths constructed from user input prevent directory traversal (`../`).

## 4. Performance Checklist
- [ ] Collections with known bounds are pre-allocated with initial capacity.
- [ ] Loops avoid redundant function calls or repeated property evaluations in loop conditions.
- [ ] Database calls avoid N+1 query patterns; joins or batch lookups are used instead.
- [ ] Large objects or byte buffers avoid unnecessary deep cloning.
