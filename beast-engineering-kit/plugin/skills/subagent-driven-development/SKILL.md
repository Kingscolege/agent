---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks using delegated subagents. Dispatches fresh subagents per task to preserve context and quality.
---

# Subagent-Driven Development (SDD)

## Overview
Execute an approved plan by dispatching a fresh, specialized subagent per task, followed by an immediate task review (spec compliance + quality), and concluding with a whole-branch final review.

```
[Coordinator]
     │
     ├─► Dispatch Fresh Implementer Subagent (invoke_subagent: 'self')
     │        │
     │        ▼
     │   Executes Task via TDD -> Runs Task Verification Command
     │        │
     │        ▼
     ├─► Dispatch Task Reviewer Subagent (invoke_subagent: 'research')
     │        │
     │        ▼
     │   Inspects diff & test results -> Verifies compliance
     │
     └─► Repeat for Next Task -> Final Verification & Whole-Branch Review
```

---

## Why Context Isolation Matters
1. **Preserve Coordinator Context:** The primary coordinator retains high-level architectural awareness, avoiding token blowout.
2. **Prevent Attention Dilution:** A subagent focused strictly on a single task does not get confused by prior failures or unrelated file histories.
3. **Strict Clean Slate:** Subagents receive only the context they need: the task spec, affected files, and verification commands.

---

## Tool Mapping for Antigravity (AGY)

| SDD Action | Antigravity Tool | Parameter Guidelines |
|---|---|---|
| **Dispatch Implementer** | `invoke_subagent` | `TypeName: "self"`, `Role: "Task Implementer"`, `Workspace: "inherit"` |
| **Dispatch Read-Only Reviewer**| `invoke_subagent` | `TypeName: "research"`, `Role: "Spec Reviewer"`, `Workspace: "inherit"` |
| **Parallel Domain Dispatch** | `swarm` / `invoke_subagent` | For independent subsystem investigations, dispatch in parallel |
| **Track Overall Plan** | `update_steps` | Maintain live checklist of active and completed plan tasks |

---

## The Workflow

### 1. Construct the Subagent Task Contract
Never pass raw conversation history. Construct a clear prompt using [subagent-prompts.md](./references/subagent-prompts.md):
- Task objective and acceptance criteria.
- Target files to create or modify.
- Strict requirement to follow TDD (Red -> Green -> Refactor).
- Exact verification command to execute.

### 2. Dispatch the Implementer
Invoke `invoke_subagent` with the prepared task prompt. Wait for the subagent's response.

### 3. Review the Task Diff
Before proceeding to the next task:
- Verify that the subagent provided actual verification output.
- Inspect the git diff of the changes (`git diff HEAD~1` or `git status`).
- If defects or slop are found, address them immediately before moving to the next task.

### 4. Final Review & Handoff
Once all tasks are finished:
- Run the full verification suite (`./verify.sh`).
- Run `deslop` on the branch diff.
- Run `code-review-lead` for independent multi-angle validation.
