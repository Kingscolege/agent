# BEAST Engineering Kit Architecture

## Overview
BEAST Engineering Kit is an architecture-driven extension suite for Google Antigravity (AGY). It equips the agent runtime with deterministic quality gates, root-cause debugging workflows, automated testing methodologies, and independent review mechanisms.

## Subsystems

1. **Engineering Constitution (`rules/AGENTS.md`)**
   - Invariant enforcement: Root-cause debugging before code changes, test-driven development, and mandatory verification evidence.
   - Task-to-skill routing matrix.

2. **Lifecycle Hooks Engine (`hooks.json`)**
   - `SessionStart`: Detects project readiness and injects constitutional guidelines.
   - `PreToolUse`: Safety gate blocking accidental execution of destructive commands.
   - `PreInvocation`: Stateful trigger engine recognizing `BEAST`, `DEBUG`, `AUDIT`, `REVIEW`, and `NORMAL` modes.

3. **Core Engineering Skills (`skills/`)**
   - `systematic-debugging`: 4-phase root-cause analysis and test bisection.
   - `test-driven-development`: Red-Green-Refactor development cycle.
   - `verification-before-completion`: Evidence-backed handoff requirements.
   - `spec-driven-development`: Requirements specifications and ADRs.
   - `writing-plans` & `executing-plans`: Atomic task decomposition and execution ledgers.
   - `subagent-driven-development`: Isolated subagent delegation.
   - `deslop`: Diff-scoped code cleanliness and anti-slop pass.
   - `code-review-lead`: Multi-angle review across logic, concurrency, security, and performance.
   - `security-audit`: Vulnerability analysis across OWASP/CWE categories.
   - `repo-intelligence`: Automated stack detection and verification gate scaffolding.
   - `beast`: Complete 12-step engineering methodology orchestrator.
