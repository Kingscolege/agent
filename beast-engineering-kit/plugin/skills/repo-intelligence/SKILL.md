---
name: repo-intelligence
description: Use when onboarding into a repository or inspecting project tools. Discovers language, framework, linters, type checkers, and test runners to generate verify.sh and project AGENTS.md.
---

# Repository Intelligence & Environment Scout

## Overview
Never guess a project's build, test, or linting commands. This skill inspects repository configuration files, lockfiles, and environment structures to derive ground-truth commands, generate a deterministic `./verify.sh` gate, and generate a tailored project `AGENTS.md`.

---

## When to Use
- When onboarding into a new repository with missing instructions
- When setting up verification gates for the first time
- When `./verify.sh` or `AGENTS.md` is absent or needs updating
- When checking repository readiness before starting work

---

## The Workflow

### 1. Run the Repo Scout Script
Execute the repo scout script to analyze the project:
```bash
repo-scout.py --inspect
# or: python3 path/to/scripts/repo-scout.py --inspect
```
The scout detects:
- Primary language(s) and runtime versions.
- Package manager (`uv`, `poetry`, `npm`, `pnpm`, `yarn`, `go modules`, `cargo`).
- Linters (`ruff`, `eslint`, `golangci-lint`, `clippy`).
- Type checkers (`mypy`, `pyright`, `tsc`).
- Test runners (`pytest`, `vitest`, `jest`, `go test`, `cargo test`).

### 2. Scaffold `./verify.sh`
If `./verify.sh` does not exist, generate it:
```bash
repo-scout.py --generate-verify
chmod +x ./verify.sh
```
Test the generated script immediately:
```bash
./verify.sh --fast
```

### 3. Generate Project-Specific `AGENTS.md`
Generate the tailored repository instruction file:
```bash
repo-scout.py --generate-agents-md
```

### 4. Verify Local Readiness
Run the setup check to confirm all gates and rules are active:
```bash
setup-check.py .
```
