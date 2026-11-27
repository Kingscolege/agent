#!/usr/bin/env bash
# uninstall.sh - Safe uninstaller for BEAST Engineering Kit
set -euo pipefail

echo "============================================================"
echo "Uninstalling BEAST Engineering Kit"
echo "============================================================"

# Detect AGY config directory
OS="$(uname -s)"
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
        AGY_CONFIG_DIR="${HOME}/.gemini/config"
        ;;
esac

PLUGIN_DIR="$AGY_CONFIG_DIR/plugins/engineering-agent-kit"

if [ ! -d "$PLUGIN_DIR" ]; then
    echo "ℹ️  BEAST Engineering Kit is not installed at $PLUGIN_DIR."
    exit 0
fi

# Disable plugin if agy CLI is available
if command -v agy >/dev/null 2>&1; then
    echo "Disabling plugin in AGY..."
    agy plugin disable engineering-agent-kit 2>/dev/null || true
fi

# Create safety backup before removing
BACKUP_DIR="${PLUGIN_DIR}.uninstalled.$(date +%Y%m%d_%H%M%S)"
echo "Archiving installation to: $BACKUP_DIR"
mv "$PLUGIN_DIR" "$BACKUP_DIR"

echo "✅ BEAST Engineering Kit uninstalled successfully."
echo "Unrelated plugins, user settings, and conversation histories were preserved."
echo "============================================================"
