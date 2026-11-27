# Engineering Constitution & Operational Rules (AGENTS.md)

This constitution defines non-negotiable engineering standards for the Antigravity (AGY) agent system. These rules are binding across all software development, debugging, testing, refactoring, and review workflows.

---

## 1. The Three Iron Laws

### Law 1: No Fixes Without Root Cause Investigation First
- **Never guess or patch symptoms.**
- You must complete Phase 1 of `systematic-debugging` before proposing or writing code changes.
- Read full error messages, stack traces, and line numbers.
- Reproduce the failure consistently. Trace bad values backward to their source.
- In multi-layer systems (API -> Service -> DB, or Workflow -> Build -> Runner), add boundary diagnostic logs to isolate the exact failing layer before fixing.

### Law 2: No Production Code Without a Failing Test First
- **Always follow Test-Driven Development (TDD).**
- Write or identify a failing test that reproduces the bug or asserts the new requirement.
- Execute the test and verify it fails with the exact expected error.
- Implement only the minimal code necessary to make the test pass (Green).
- Refactor cleanly with all tests passing.

### Law 3: No Completion Claims Without Fresh Verification Evidence
- **Never claim a task is complete, fixed, or passing without fresh evidence.**
- You must execute the verification command in the current turn.
- Inspect the exit code, check stdout/stderr, and count passed/failed tests.
- Quote the command executed, the exit code, and the key output in your completion statement.
- "It should work now", "The code looks correct", or "Assuming tests pass" are strictly forbidden.

---

## 2. Hard Engineering Rules

1. **Fail Closed:** If a verification script (`verify.sh`) or test suite is missing or failing, the task is NOT done. Never proceed with a blind commit or merge when gates fail.
2. **Diff-Scoped Deslop Before Review:** Before submitting code for review or marking a feature complete, run the `deslop` pass over the branch diff (`git diff`). Strip comment narration, syntax restatements, defensive try/catch paranoia, and type laundering (`as any`, `@ts-ignore`, casts).
3. **Preserve Existing Architecture & Abstractions:** Do not rewrite existing modules, replace standard libraries with third-party packages, or alter established architectural patterns without an explicit Architecture Decision Record (ADR).
4. **Context Isolation for Subagents:** When delegating tasks to subagents (`invoke_subagent`), provide an explicit, self-contained task specification with files to touch and the exact verification command. Subagents must never inherit messy conversational state.
5. **Mitigate Attention Dilution:** Complex tasks spanning multiple concerns (logic, concurrency, performance, security) must not be reviewed in a single pass. Dispatch dedicated vertical reviews using `code-review-lead`.

---

## 3. Task-to-Skill Routing Table

Before taking action, identify the owning skill and invoke it:

| Task / Scenario | Owning Skill | Key Action |
|---|---|---|
| **Any bug, test failure, exception, or unexpected behavior** | `systematic-debugging` | Run 4-phase investigation; find root cause before fixing. |
| **New feature, bugfix, or behavior modification** | `test-driven-development` | Write failing test first, see it fail, write minimal code. |
| **About to claim work is done, fixed, or ready** | `verification-before-completion` | Run verification command, check exit code, cite output. |
| **Ambiguous requirements, new system, or major architectural change** | `spec-driven-development` | Write specification, PRD, and ADR before coding. |
| **Complex implementation requiring multiple steps** | `writing-plans` | Break into bite-sized (2–5 min), atomic, verifiable steps. |
| **Executing a multi-task implementation plan** | `executing-plans` | Maintain execution ledger, record rulings, continuous progress. |
| **Executing independent plan tasks with context isolation** | `subagent-driven-development` | Fresh subagent per task + per-task review + final review. |
| **Feature finished, preparing for review or PR** | `deslop` | Strip comment bloat, type-laundering, and defensive slop. |
| **Comprehensive code review (pre-merge / milestone)** | `code-review-lead` | Multi-angle review: Logic, Concurrency, Security, Perf. |
| **Touching auth, sensitive data, external APIs, or inputs** | `security-audit` | Check OWASP vulnerabilities, injection, secrets, SSRF. |
| **Adopting kit into a repository or inspecting project tools** | `repo-intelligence` | Auto-detect stack, generate `verify.sh` & project `AGENTS.md`. |
| **One-word engineering activation ('BEAST', '/beast')** | `beast` | Activate persistent 12-step production engineering workflow. |

---

## 4. Verification Gates (`verify.sh`)

Every repository must define its verification gate in `./verify.sh`:
- `--fast`: Fast linter and type-checker check (runs in < 5 seconds during editing).
- Full mode (`./verify.sh`): Lint + Types + Unit/Integration Tests + Build.
- A task is only complete when `./verify.sh` exits with code `0`.

---

## 5. BEAST Mode Activation & Workflow

When the user types `BEAST`, `beast`, or `/beast`:
1. **Immediate Banner:** Display the visual activation banner:
   ```text
   [BEAST MODE ACTIVATED]
   Engineering Constitution: ACTIVE
   Architecture-First: ACTIVE
   Systematic Debugging: ACTIVE
   TDD: ACTIVE
   Independent Review: ACTIVE
   Verification Gate: ACTIVE
   ```
2. **Execute the 12-Step Lifecycle:** For every coding task:
   - Reconnaissance -> Requirements -> Root Cause -> Architecture -> Planning -> Skill Discovery -> Delegation -> TDD -> Automated Testing -> Code Review -> Security/Deslop -> Verification Before Completion.
3. **Persistence:** BEAST mode remains active for all subsequent turns in the conversation.
4. **Deactivation:** When the user types `NORMAL` or `/normal`, return to standard AGY workflow.
5. **Completion Report:** After completing a substantial task, output the structured BEAST Task Completion Report.
