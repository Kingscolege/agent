# BEAST Engineering Kit

Production-grade engineering architecture, skills, and verification gates for **Google Antigravity (AGY)** agents.

## Quickstart

### 1. Clone & Install
```bash
git clone git@github.com:Kingscolege/agent.git beast-engineering-kit
cd beast-engineering-kit

# macOS / Linux
bash installers/install.sh

# Windows (PowerShell)
.\installers\install.ps1
```

### 2. Activate BEAST Mode
In any AGY session, type:
```text
BEAST
```
or
```text
BEAST: implement payment checkout flow
```

To deactivate:
```text
NORMAL
```

## Available Triggers
- `BEAST`: Full 12-step production engineering workflow.
- `DEBUG`: 4-phase root-cause debugging (`systematic-debugging`).
- `AUDIT`: Security hardening and diff-scoped anti-slop pass (`security-audit`, `deslop`).
- `REVIEW`: Multi-angle code review (`code-review-lead`).
- `NORMAL`: Return to standard AGY conversation.

## Repository Layout
- `plugin/`: The native AGY plugin files (skills, rules, hooks, scripts).
- `commands/`: Reference documentation for triggers and commands.
- `installers/`: Cross-platform installation and uninstallation scripts.
- `docs/`: In-depth architecture, configuration, and troubleshooting guides.
- `tests/`: Automated regression and cross-platform test suites.

## License
Apache-2.0
