#!/usr/bin/env bash
# verify-runner.sh - Executes the project's verify.sh gate or fails closed.
set -euo pipefail

TARGET_DIR="${1:-.}"
FAST_FLAG=""
if [ "${2:-}" = "--fast" ] || [ "${1:-}" = "--fast" ]; then
    FAST_FLAG="--fast"
    if [ "$TARGET_DIR" = "--fast" ]; then
        TARGET_DIR="."
    fi
fi

cd "$TARGET_DIR"

if [ -f "./verify.sh" ]; then
    echo "Running local quality gate: ./verify.sh $FAST_FLAG"
    bash ./verify.sh $FAST_FLAG
elif [ -f "./.agents/verify.sh" ]; then
    echo "Running local quality gate: ./.agents/verify.sh $FAST_FLAG"
    bash ./.agents/verify.sh $FAST_FLAG
else
    echo "❌ ERROR: No verify.sh found in $TARGET_DIR." >&2
    echo "FAIL CLOSED: You must generate a verification gate before work can be marked complete." >&2
    echo "Run: repo-intelligence skill or 'repo-scout.py --generate-verify'" >&2
    exit 1
fi
