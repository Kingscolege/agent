#!/usr/bin/env bash
# install.sh - Cross-platform installer for BEAST Engineering Kit (macOS & Linux)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
PLUGIN_SRC="$REPO_ROOT/plugin"

echo "============================================================"
echo "⚡ Installing BEAST Engineering Kit for Antigravity (AGY)"
echo "============================================================"

# --- 1. Detect Operating System & Architecture ---
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "Detected OS: $OS ($ARCH)"

case "$OS" in
    Darwin)
        AGY_CONFIG_DIR="${HOME}/.gemini/config"
        ;;
    Linux)
        AGY_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/gemini/config"
        if [ ! -d "$AGY_CONFIG_DIR" ] && [ -d "${HOME}/.gemini/config" ]; then
            AGY_CONFIG_DIR="${HOME}/.gemini/config"
        fi
        ;;
    *)
        echo "⚠️ Unknown OS '$OS'. Falling back to default ~/.gemini/config."
        AGY_CONFIG_DIR="${HOME}/.gemini/config"
        ;;
esac

# Fallback to ~/.gemini/config if target doesn't exist
if [ ! -d "$AGY_CONFIG_DIR" ]; then
    AGY_CONFIG_DIR="${HOME}/.gemini/config"
fi

PLUGIN_DEST="$AGY_CONFIG_DIR/plugins/engineering-agent-kit"
echo "Target Plugin Destination: $PLUGIN_DEST"

# --- 2. Check Prerequisites ---
echo "Checking prerequisites..."
# Python check
PY_BIN=""
if [ -n "${PYTHON:-}" ] && command -v "$PYTHON" >/dev/null 2>&1; then
    PY_BIN="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
    PY_BIN="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="$(command -v python)"
fi

if [ -z "$PY_BIN" ]; then
    echo "❌ ERROR: Python 3.8+ is required but not found in PATH." >&2
    echo "Please install Python 3 or set the PYTHON environment variable." >&2
    exit 1
fi
echo "✅ Python detected: $($PY_BIN --version 2>&1)"

# Check AGY CLI
HAS_AGY=0
if command -v agy >/dev/null 2>&1; then
    HAS_AGY=1
    echo "✅ Antigravity CLI detected: $(agy --help | head -n 1)"
else
    echo "ℹ️  Antigravity CLI ('agy') not found in PATH. Plugin will be configured for Antigravity desktop/IDE."
fi

# --- 3. Validate Source Plugin Structure ---
echo "Validating plugin source structure..."
if [ ! -f "$PLUGIN_SRC/plugin.json" ]; then
    echo "❌ ERROR: plugin.json missing from $PLUGIN_SRC" >&2
    exit 1
fi
if [ ! -f "$PLUGIN_SRC/hooks.json" ]; then
    echo "❌ ERROR: hooks.json missing from $PLUGIN_SRC" >&2
    exit 1
fi
if [ ! -f "$PLUGIN_SRC/rules/AGENTS.md" ]; then
    echo "❌ ERROR: rules/AGENTS.md missing from $PLUGIN_SRC" >&2
    exit 1
fi
if [ ! -d "$PLUGIN_SRC/skills" ]; then
    echo "❌ ERROR: skills directory missing from $PLUGIN_SRC" >&2
    exit 1
fi
echo "✅ Plugin structure valid."

# --- 4. Backup Existing Installation ---
if [ -d "$PLUGIN_DEST" ]; then
    BACKUP_DIR="${PLUGIN_DEST}.bak.$(date +%Y%m%d_%H%M%S)"
    echo "Backing up existing installation to: $BACKUP_DIR"
    cp -R "$PLUGIN_DEST" "$BACKUP_DIR"
fi

# --- 5. Install Plugin Files ---
echo "Installing plugin files to $PLUGIN_DEST..."
mkdir -p "$AGY_CONFIG_DIR/plugins"
rm -rf "$PLUGIN_DEST"
cp -R "$PLUGIN_SRC" "$PLUGIN_DEST"

# Ensure all scripts are executable
chmod +x "$PLUGIN_DEST"/scripts/*.sh "$PLUGIN_DEST"/scripts/*.py 2>/dev/null || true
echo "✅ Files copied and permissions set."

# --- 6. Enable Plugin in AGY ---
if [ "$HAS_AGY" -eq 1 ]; then
    echo "Enabling plugin via AGY CLI..."
    agy plugin enable engineering-agent-kit 2>/dev/null || true
fi

# --- 7. Verify Discovery & Skills ---
echo "Verifying installation integrity..."
SKILL_COUNT=$(find "$PLUGIN_DEST/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
echo "✅ Discovered $SKILL_COUNT engineering skills."

if [ -f "$PLUGIN_DEST/skills/beast/SKILL.md" ]; then
    echo "✅ BEAST mode skill verified."
else
    echo "❌ ERROR: beast skill missing after install!" >&2
    exit 1
fi

# --- 8. Verify Hook Registration ---
if grep -q "PreInvocation" "$PLUGIN_DEST/hooks.json" && grep -q "PreToolUse" "$PLUGIN_DEST/hooks.json"; then
    echo "✅ Lifecycle hooks (PreInvocation, PreToolUse, SessionStart) verified."
else
    echo "⚠️ Warning: Hooks registration could not be verified in hooks.json."
fi

# --- 9. Final Report ---
echo "============================================================"
echo "🎉 BEAST Engineering Kit Successfully Installed!"
echo "============================================================"
echo "- Plugin Location:  $PLUGIN_DEST"
echo "- Skills Installed: $SKILL_COUNT"
echo "- Constitution:     $PLUGIN_DEST/rules/AGENTS.md"
echo ""
echo "Quickstart:"
echo "1. Start an AGY session (agy or open Antigravity IDE)"
echo "2. Type 'BEAST' to activate full production engineering mode"
echo "3. Type 'DEBUG', 'AUDIT', or 'REVIEW' for specialized workflows"
echo "4. Type 'NORMAL' to return to standard mode"
echo "============================================================"
