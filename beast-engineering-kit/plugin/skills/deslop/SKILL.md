---
name: deslop
description: Use when a feature or task is finished, before requesting review or creating pull requests. Diff-scoped AI-slop cleanup pass stripping comment bloat, defensive paranoia, type-laundering (as any), and style drift from the current diff.
---

# Deslop: Anti-Slop Code Cleaner

## Overview
AI coding agents frequently introduce "slop": commentary explaining obvious code, redundant `try/catch` wrappers protecting impossible states, type-laundering (`as any`, `@ts-ignore`), and one-off helper abstractions.

**The deslop pass scrubs this noise from the current branch diff before code review.**

---

## Scope & The Iron Rule
- **Diff-Scoped Only:** Inspect only the hunks in `git diff` against the base branch (`git diff origin/main` or `git diff HEAD~1`). Never perform repo-wide cleanups!
- **Behavior-Neutral:** Make NO functional changes. If a change might alter runtime behavior, leave it alone and report it instead.

---

## The Deslop Checklist

Inspect every changed line in the diff for:

1. **Comment Slop:**
   - Obvious narration: `// loop through items`, `// return the result`
   - Restating syntax: `// declare variable x as string`
   - Generated disclaimers: `// Note: this function handles errors safely`
2. **Defensive Paranoia:**
   - Wrapping predictable, pure in-memory logic in huge `try/catch` blocks that swallow errors.
   - Adding null checks for values guaranteed non-null by types or upstream validation.
3. **Type Laundering:**
   - Using `as any`, `as unknown as T`, `reinterpret_cast`, or `# type: ignore` to bypass type safety.
   - Fix the actual type definition instead of laundering the type!
4. **Abstraction Bloat:**
   - Single-use private helper functions that do not simplify control flow or add domain clarity.
   - Redundant variable aliases: `const res = result; return res;`
5. **Drift from Surrounding Style:**
   - Using unfamiliar naming conventions, quotes, or indentation conflicting with the surrounding file.

---

## Execution
Run the automated deslop scanner:
```bash
deslop-runner.py
# or: python3 path/to/scripts/deslop-runner.py
```
Review flagged hunks and apply clean, behavior-neutral simplifications.
