#!/usr/bin/env bash
# run-hook.sh - Portable lifecycle hook runner for BEAST Engineering Kit
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
HOOK_NAME="${1:-}"

# Portable python detection without hardcoded paths
PY_BIN=""

if [ -n "${PYTHON:-}" ] && [ -x "${PYTHON}" ]; then
    PY_BIN="${PYTHON}"
elif command -v python3 >/dev/null 2>&1 && python3 --version >/dev/null 2>&1; then
    PY_BIN="$(command -v python3)"
elif command -v uv >/dev/null 2>&1; then
    PY_BIN="$(uv python find 3 2>/dev/null || true)"
elif [ -d "${HOME}/.local/share/uv/python" ]; then
    CANDIDATE="$(find "${HOME}/.local/share/uv/python" -name "python3" -type f -perm +111 2>/dev/null | head -n 1 || true)"
    if [ -n "$CANDIDATE" ] && [ -x "$CANDIDATE" ]; then
        PY_BIN="$CANDIDATE"
    fi
elif command -v python >/dev/null 2>&1 && python --version >/dev/null 2>&1; then
    PY_BIN="$(command -v python)"
fi

if [ -n "$PY_BIN" ] && [ -x "$PY_BIN" ]; then
    exec "$PY_BIN" "$DIR/$HOOK_NAME.py"
else
    # Fallback to minimal shell response if python is temporarily unavailable
    if [ "$HOOK_NAME" = "pre-tool-safety" ]; then
        echo '{"decision": "allow"}'
    elif [ "$HOOK_NAME" = "session-start" ]; then
        echo '{"injectSteps": [{"systemMessage": {"systemMessage": "BEAST Engineering Kit initialized."}}]}'
    else
        echo '{}'
    fi
fi
