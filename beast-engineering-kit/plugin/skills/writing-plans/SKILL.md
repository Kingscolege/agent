---
name: writing-plans
description: Use when decomposing complex tasks into bite-sized, atomic, verifiable implementation steps before writing code.
---

# Writing Implementation Plans

## Overview
A high-quality plan is a series of bite-sized, atomic tasks where each task can be executed, tested, and verified independently.

---

## Task Sizing Rule
**Each task must represent 2–5 minutes of work.**
If a task touches 5 different files or includes both a database migration and a frontend redesign, it is too large. Break it down.

---

## Structure of Each Task

Every task in the plan MUST follow this schema:

```markdown
### Task [N]: [Short imperative description, e.g., 'Add user validation helper']
- **Files to modify / create:** `src/models/user.py`, `tests/test_user.py`
- **Specification / Requirement:**
  - Define `validate_user_email(email: str) -> bool`.
  - Validate syntax and reject empty domains.
- **Verification Command:** `pytest tests/test_user.py -k "test_validate_user_email"`
- **Expected Result:** Exit code 0, 3 test cases passed.
```

---

## Guidelines for Authoring Plans

1. **Order Tasks by Dependency:** Foundational data models and schemas first, business logic second, API endpoints third, UI last.
2. **Include Verification at Every Step:** Every single task must name the command that proves it works.
3. **Use Artifacts for Tracking:** Save the plan as a Markdown artifact in the brain directory (`write_file`) or maintain it with `update_steps`.
4. **Reference Implementation Template:** See [plan-template.md](./references/plan-template.md) for full document layout.
