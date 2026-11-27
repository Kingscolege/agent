# Implementation Plan Template

```markdown
# Implementation Plan: [Feature / Refactor Name]

**Objective:** [Brief 1-sentence statement of what we are building]
**Spec / ADR Reference:** [Link to spec or ADR]
**Target Quality Gate:** `./verify.sh`

---

## Proposed Tasks

### Task 1: [Task Name]
- **Files:** `path/to/target.py`, `tests/test_target.py`
- **Actions:**
  - [Action item 1]
  - [Action item 2]
- **Verification:** `[Exact command, e.g., pytest tests/test_target.py]`
- **Expected Outcome:** `[Exit code 0, all tests pass]`

### Task 2: [Task Name]
- **Files:** `path/to/target2.py`, `tests/test_target2.py`
- **Actions:**
  - [Action item 1]
- **Verification:** `[Exact command]`
- **Expected Outcome:** `[Exit code 0]`

---

## Final Verification & Gate
- **Full Verification:** `./verify.sh`
- **Deslop Pass:** `.agents/skills/deslop/SKILL.md`
- **Code Review:** `code-review-lead`
```
