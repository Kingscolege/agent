# Troubleshooting Guide

## Common Issues & Solutions

### 1. Plugin Not Found by AGY
- Verify that `~/.gemini/config/plugins/engineering-agent-kit` exists.
- Run `agy plugin list` to check whether it appears in the installed list.
- If missing, run `installers/install.sh` again.

### 2. Python Detection Issues
- Ensure `python3` or `python` is in your `PATH`.
- You can override the interpreter path by setting the `PYTHON` environment variable:
  ```bash
  export PYTHON=/path/to/python3
  ```

### 3. Missing `verify.sh` Warning
- If a project lacks a verification gate, run:
  ```bash
  repo-scout.py --generate-verify
  chmod +x verify.sh
  ```
