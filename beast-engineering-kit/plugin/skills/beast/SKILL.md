---
name: beast
description: Use when the user types BEAST, beast, or /beast to activate the complete production-grade engineering workflow. Enforces the 12-step engineering methodology across all tasks.
---

# BEAST MODE: Complete Production-Grade Engineering Activation

## Overview
**BEAST mode** is the single-word trigger that transitions AGY into a strictly disciplined, architecture-driven, production-grade software engineering agent.

When activated, all shortcuts, probabilistic guesses, and unverified assumptions are strictly prohibited. Every substantial coding task must progress through the 12-step engineering lifecycle.

---

## Trigger Recognition & Activation

Recognized triggers (case-insensitive):
- `BEAST`
- `beast`
- `/beast`

### Activation Behaviors:
1. **Trigger Alone (`BEAST`):**
   - Activate BEAST mode for the conversation.
   - Display the visual activation banner.
   - Await the user's first task.
2. **Trigger with Task (`BEAST: <task>` or `beast <task>`):**
   - Activate BEAST mode for the conversation.
   - Display the visual activation banner.
   - Immediately process the specified task through the 12-step lifecycle.
3. **Deactivation (`NORMAL`):**
   - Return immediately to standard AGY workflow.

---

## 1. Visual Activation Banner

Whenever BEAST mode is triggered or initiated, you MUST prominently display:

```text
[BEAST MODE ACTIVATED]
Engineering Constitution: ACTIVE
Architecture-First: ACTIVE
Systematic Debugging: ACTIVE
TDD: ACTIVE
Independent Review: ACTIVE
Verification Gate: ACTIVE
```

---

## 2. The 12-Step Mandatory Engineering Workflow

Every substantial coding task executed in BEAST mode MUST follow these 12 phases:

```mermaid
flowchart TD
    Step1["1. Repository Reconnaissance (repo-intelligence)"] --> Step2["2. Requirements Analysis (spec-driven-development)"]
    Step2 --> Step3["3. Root-Cause Investigation (systematic-debugging)"]
    Step3 --> Step4["4. Architecture & Impact Analysis (ADR)"]
    Step4 --> Step5["5. Implementation Planning (writing-plans)"]
    Step5 --> Step6["6. Skill Discovery & Activation"]
    Step6 --> Step7["7. Intelligent Agent Delegation (subagent-driven-development)"]
    Step7 --> Step8["8. Implementation via TDD (test-driven-development)"]
    Step8 --> Step9["9. Automated Testing & Validation (./verify.sh)"]
    Step9 --> Step10["10. Independent Multi-Angle Review (code-review-lead)"]
    Step10 --> Step11["11. Security & Anti-Slop Audit (security-audit & deslop)"]
    Step11 --> Step12["12. Verification Before Completion (verification-before-completion)"]
    Step12 --> CompletionReport["Concise Completion Report"]
```

### Phase Details & Owning Skills:
1. **Repository Reconnaissance:** Run `repo-intelligence` / `setup-check.py` to identify the project stack, lockfiles, linters, and verification script (`verify.sh`).
2. **Requirements Analysis:** Establish concrete acceptance criteria and contract specifications using `spec-driven-development`.
3. **Root-Cause Investigation:** If fixing an issue or unexpected behavior, complete Phase 1 of `systematic-debugging` (no symptom fixes or trial-and-error).
4. **Architecture & Impact Analysis:** Document technical trade-offs using ADR standards (`spec-driven-development`).
5. **Implementation Planning:** Decompose work into bite-sized (2–5 min), atomic, verifiable steps using `writing-plans`.
6. **Skill Discovery & Activation:** Explicitly identify and activate all domain and stack skills required.
7. **Intelligent Agent Delegation:** For multi-task plans or multi-angle checks, delegate to isolated subagents (`subagent-driven-development` or `swarm`).
8. **Implementation via TDD:** Strictly follow the Red -> Green -> Refactor cycle using `test-driven-development`.
9. **Automated Testing & Validation:** Execute the project verification gate (`./verify.sh`). Zero gate errors allowed.
10. **Independent Code Review:** Dispatch multi-angle review across Logic, Concurrency, Security, and Performance (`code-review-lead`).
11. **Security & Anti-Slop Assessment:** Run `security-audit` on sensitive data/auth paths and scrub AI slop using `deslop`.
12. **Verification Before Completion:** Execute the full verification command fresh, inspect the exit code and output, and cite the evidence (`verification-before-completion`).

---

## 3. Persistent Conversation Mode

BEAST mode is **stateful within the conversation**:
- Once activated, all subsequent turns in the same conversation automatically run under BEAST mode.
- The mode persists across multiple turns until the user types `NORMAL` (or `/normal`).

---

## 4. Completion Report Format

After each substantial task in BEAST mode, output a structured summary:

```markdown
### 🏆 BEAST Mode Task Completion Report

- **Task Summary:** [Short description of work completed]
- **Architecture & Spec:** [Spec/ADR reference or invariants upheld]
- **Tests Added/Updated:** [Regression or unit test files]
- **Verification Evidence:**
  - **Command:** `./verify.sh`
  - **Exit Code:** `0`
  - **Output:** `[Test runner summary, e.g. 14 passed in 0.4s]`
- **Review & Security Sign-Off:**
  - **Deslop Pass:** Clean (zero type laundering or comment slop)
  - **Code Review:** Approved (Logic, Concurrency, Security, Perf checked)
- **Status:** Complete & Production Ready
```
