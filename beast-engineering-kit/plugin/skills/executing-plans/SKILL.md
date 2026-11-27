---
name: executing-plans
description: Use when executing an approved implementation plan step-by-step. Enforces execution ledgers, rulings, and continuous execution.
---

# Executing Implementation Plans

## Overview
Execute tasks systematically according to the approved plan. Maintain execution state, record technical rulings, and keep progress visible without unnecessary stalls.

---

## The Execution Ledger
During plan execution, track state continuously using either the live `update_steps` checklist or a task artifact.

For each task:
1. Announce the task currently in progress.
2. Follow `test-driven-development` (Red -> Green -> Refactor).
3. Run the task's verification command.
4. Mark the task done only when the verification command succeeds.

---

## Rulings, Not Stalls

When encountering minor ambiguities, edge cases, or plan discrepancies:
- **Do not stall the session** asking trivial questions if the spec or surrounding codebase implies the correct path.
- **Issue a Ruling:** Make the pragmatic decision, record it in your ledger, and continue.
  - Format: `Ruling: <What was decided> — <Why> — <Cost/Risk if wrong>`
- **When you MUST stop and ask:**
  1. Irreversible or destructive operations (dropping data, force pushes).
  2. Security or authentication architectural boundaries.
  3. Changes breaking existing public APIs or external consumer contracts.

---

## Plan Completion Hand-off
Once all tasks are finished:
1. Run `./verify.sh` to ensure full project health.
2. Run `deslop` over the git diff.
3. Request independent review via `code-review-lead`.
4. Run `verification-before-completion` before reporting completion to the user.
