# Installation Guide

## Prerequisites
- **Git**
- **Python 3.8+** (available as `python3` or `python`)
- **Google Antigravity (AGY)** CLI, IDE, or desktop app

## Installation Steps

### 1. Clone the Repository
```bash
git clone git@github.com:Kingscolege/agent.git beast-engineering-kit
cd beast-engineering-kit
```

### 2. Run the Platform Installer

**macOS / Linux:**
```bash
bash installers/install.sh
```

**Windows (PowerShell 5.1+ or Core):**
```powershell
.\installers\install.ps1
```

### 3. Verify the Installation
Run:
```bash
agy plugin list
```
You should see:
```text
- engineering-agent-kit (enabled, 1.0.0)
    Components: 12 skills, 1 rule, 3 hooks
```

## Uninstallation
To remove the plugin:
```bash
bash installers/uninstall.sh
```
Unrelated plugins and user configurations will remain intact.
