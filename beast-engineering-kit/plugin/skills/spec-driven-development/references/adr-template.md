# Architecture Decision Record (ADR) Template

```markdown
# ADR-[NUMBER]: [Short descriptive title]

**Date:** [YYYY-MM-DD]  
**Status:** [Proposed | Accepted | Superseded | Deprecated]  
**Author(s):** [Names / AI Agent]  

## 1. Context & Problem Statement
What is the problem we are solving? What constraints (technical, business, performance) must be respected?

## 2. Options Considered
- **Option A:** [Description, Pros, Cons]
- **Option B:** [Description, Pros, Cons]
- **Option C:** [Description, Pros, Cons]

## 3. Decision
We decided to adopt **[Option X]** because [primary justification].

## 4. Invariants & Key Trade-offs
- What invariants must not be violated?
- What are we intentionally sacrificing (e.g. slight memory increase for O(1) latency)?

## 5. Consequences
- **Positive:** [Expected benefits, simplified maintenance]
- **Negative / Risks:** [Added complexity, migration cost]
- **Mitigation:** [How risks will be monitored and handled]
```
