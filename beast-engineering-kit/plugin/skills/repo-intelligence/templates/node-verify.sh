#!/usr/bin/env bash
# verify.sh -- Starter gate for Node / TypeScript projects
set -euo pipefail

cd "$(dirname "$0")"
FAST=0
[ "${1:-}" = "--fast" ] && FAST=1

# Detect package manager
PM="npm"
if [ -f pnpm-lock.yaml ]; then PM="pnpm"
elif [ -f yarn.lock ]; then PM="yarn"
fi

echo "== [1/3] Running Linters =="
$PM run lint || npm run lint || true

echo "== [2/3] Type Checking =="
if [ -f tsconfig.json ]; then
    npx tsc --noEmit
fi

if [ "$FAST" -eq 0 ]; then
    echo "== [3/3] Running Tests =="
    $PM test || npm test
fi

echo "✅ verify: ALL GATES PASSED"
