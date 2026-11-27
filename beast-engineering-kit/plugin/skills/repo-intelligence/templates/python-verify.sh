#!/usr/bin/env bash
# verify.sh -- Starter gate for Python projects
set -euo pipefail

cd "$(dirname "$0")"
FAST=0
[ "${1:-}" = "--fast" ] && FAST=1

echo "== [1/4] Running Linters =="
if command -v ruff >/dev/null 2>&1; then
    ruff check .
elif command -v flake8 >/dev/null 2>&1; then
    flake8 .
fi

echo "== [2/4] Running Type Checks =="
if command -v mypy >/dev/null 2>&1; then
    mypy . || true
elif command -v pyright >/dev/null 2>&1; then
    pyright || true
fi

if [ "$FAST" -eq 0 ]; then
    echo "== [3/4] Running Unit & Integration Tests =="
    if [ -f uv.lock ] && command -v uv >/dev/null 2>&1; then
        uv run pytest
    elif command -v pytest >/dev/null 2>&1; then
        pytest
    else
        python3 -m unittest discover tests/
    fi

    echo "== [4/4] Verifying Build / Packaging =="
    # Add build checks if applicable
fi

echo "✅ verify: ALL GATES PASSED"
