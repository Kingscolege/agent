# install.ps1 - Windows PowerShell Installer for BEAST Engineering Kit
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "⚡ Installing BEAST Engineering Kit for Antigravity (AGY)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Determine Paths
$RepoRoot = Split-Path -Parent $PSScriptRoot
$PluginSrc = Join-Path $RepoRoot "plugin"
$UserProfile = [Environment]::GetFolderPath("UserProfile")
$AgyConfigDir = Join-Path $UserProfile ".gemini\config"
$PluginsDir = Join-Path $AgyConfigDir "plugins"
$PluginDest = Join-Path $PluginsDir "engineering-agent-kit"

Write-Host "Target Plugin Destination: $PluginDest"

# 2. Check Prerequisites
Write-Host "Checking prerequisites..."
$PythonCmd = Get-Command "python" -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    $PythonCmd = Get-Command "python3" -ErrorAction SilentlyContinue
}

if (-not $PythonCmd) {
    Write-Error "Python 3.8+ is required but not found in PATH. Please install Python."
    exit 1
}
Write-Host "✅ Python detected: $($PythonCmd.Source)" -ForegroundColor Green

$AgyCmd = Get-Command "agy" -ErrorAction SilentlyContinue
if ($AgyCmd) {
    Write-Host "✅ Antigravity CLI detected: $($AgyCmd.Source)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Antigravity CLI ('agy') not found in PATH. Plugin will be configured for Antigravity desktop/IDE." -ForegroundColor Yellow
}

# 3. Validate Source Plugin Structure
Write-Host "Validating plugin source structure..."
if (-not (Test-Path (Join-Path $PluginSrc "plugin.json"))) {
    Write-Error "plugin.json missing from $PluginSrc"
    exit 1
}
if (-not (Test-Path (Join-Path $PluginSrc "hooks.json"))) {
    Write-Error "hooks.json missing from $PluginSrc"
    exit 1
}
if (-not (Test-Path (Join-Path $PluginSrc "rules\AGENTS.md"))) {
    Write-Error "rules\AGENTS.md missing from $PluginSrc"
    exit 1
}
Write-Host "✅ Plugin structure valid." -ForegroundColor Green

# 4. Backup Existing Installation
if (Test-Path $PluginDest) {
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BackupDir = "${PluginDest}.bak.${Timestamp}"
    Write-Host "Backing up existing installation to: $BackupDir" -ForegroundColor Yellow
    Copy-Item -Path $PluginDest -Destination $BackupDir -Recurse -Force
}

# 5. Install Plugin Files
Write-Host "Installing plugin files to $PluginDest..."
if (-not (Test-Path $PluginsDir)) {
    New-Item -ItemType Directory -Path $PluginsDir -Force | Out-Null
}

if (Test-Path $PluginDest) {
    Remove-Item -Path $PluginDest -Recurse -Force
}
Copy-Item -Path $PluginSrc -Destination $PluginDest -Recurse -Force
Write-Host "✅ Files copied successfully." -ForegroundColor Green

# 6. Enable Plugin in AGY
if ($AgyCmd) {
    Write-Host "Enabling plugin via AGY CLI..."
    try {
        & agy plugin enable engineering-agent-kit 2>$null
    } catch {}
}

# 7. Verify Discovery & Skills
$SkillsDir = Join-Path $PluginDest "skills"
$SkillCount = (Get-ChildItem -Path $SkillsDir -Directory).Count
Write-Host "✅ Discovered $SkillCount engineering skills." -ForegroundColor Green

if (Test-Path (Join-Path $SkillsDir "beast\SKILL.md")) {
    Write-Host "✅ BEAST mode skill verified." -ForegroundColor Green
} else {
    Write-Error "beast skill missing after installation!"
    exit 1
}

# 8. Report
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎉 BEAST Engineering Kit Successfully Installed!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "- Plugin Location:  $PluginDest"
Write-Host "- Skills Installed: $SkillCount"
Write-Host "- Constitution:     $PluginDest\rules\AGENTS.md"
Write-Host ""
Write-Host "Quickstart:"
Write-Host "1. Start an AGY session (agy or open Antigravity IDE)"
Write-Host "2. Type 'BEAST' to activate full production engineering mode"
Write-Host "3. Type 'DEBUG', 'AUDIT', or 'REVIEW' for specialized workflows"
Write-Host "4. Type 'NORMAL' to return to standard mode"
Write-Host "============================================================" -ForegroundColor Cyan
