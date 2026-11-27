---
name: spec-driven-development
description: Use when starting a new project, feature, major refactor, or API design before writing code. Enforces specification and Architecture Decision Records (ADR).
---

# Spec-Driven Development

## Overview
Write a structured specification before writing any code. The specification serves as the contract between user requirements and technical implementation. Code without a spec is guessing.

---

## When to Use
- Starting a new feature or service
- Requirements are ambiguous, implicit, or incomplete
- Changes span multiple files, modules, or services
- Making significant architectural, schema, or API decisions
- Any task estimated to take more than 15 minutes of agent work

**When NOT to use:** Single-line typo fixes, trivial dependency bumps, or straightforward local bugfixes with clear reproductions.

---

## The Gated Workflow

```
PHASE 0: Scope Check
       │
       ▼
PHASE 1: Specify (PRD / Feature Spec)
       │
       ▼
PHASE 2: Architectural Decision (ADR)
       │
       ▼
PHASE 3: Implementation Plan (writing-plans)
```

### Phase 0: Scope Check
Before drafting, verify whether the request bundles multiple independent capabilities. If so, split them into distinct capability milestones instead of attempting a monolithic implementation.

### Phase 1: Feature Specification
Draft a concise spec covering:
1. **User Goal & Problem Statement:** Why this is needed.
2. **Acceptance Criteria:** Given/When/Then testable conditions.
3. **API & Interface Contracts:** Exact method signatures, endpoints, request/response JSON schemas, and error codes.
4. **Non-Functional Requirements:** Performance, security, backwards compatibility, telemetry.

### Phase 2: Architecture Decision Record (ADR)
For non-trivial architectural choices (e.g. database schema, library selection, concurrency pattern), document the decision using the template at [adr-template.md](./references/adr-template.md).

### Phase 3: Handoff to Planning
Once the spec and ADR are established, transition to `writing-plans` to generate atomic implementation steps.
