# Configuration Guide

## Customizing Rules
The global rules for the agent reside in `plugin/rules/AGENTS.md`. You can tailor project-specific rules by generating a local `AGENTS.md` in any project root:
```bash
repo-scout.py --generate-agents-md
```

## Customizing Quality Gates
Each project defines its quality gate in `./verify.sh`:
- Fast mode: `./verify.sh --fast` (linters and type checkers only).
- Full mode: `./verify.sh` (linters, type checkers, tests, and build).

## Triggers & Commands
The kit provides one-word triggers:
- `BEAST`: Activates the 12-step engineering lifecycle.
- `DEBUG`: Activates root-cause investigation mode.
- `AUDIT`: Activates security and code cleanliness audit.
- `REVIEW`: Activates multi-angle code review.
- `NORMAL`: Returns to default unconstrained interaction.
