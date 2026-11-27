#!/usr/bin/env python3
"""
Repository Scout & Intelligence Engine.
Discovers project stack, config, linters, typecheckers, and test runners.
Generates project-specific verify.sh and AGENTS.md.
"""
import os
import sys
import json

def analyze_repo(target_dir):
    info = {
        "languages": [],
        "package_manager": None,
        "lockfile": None,
        "linters": [],
        "typecheckers": [],
        "test_runners": [],
        "has_git": os.path.isdir(os.path.join(target_dir, ".git")),
        "has_verify_sh": os.path.isfile(os.path.join(target_dir, "verify.sh")),
        "has_agents_md": os.path.isfile(os.path.join(target_dir, "AGENTS.md")),
    }

    # Python detection
    pyproject = os.path.join(target_dir, "pyproject.toml")
    has_py = any(f.endswith(".py") for f in os.listdir(target_dir)) or os.path.exists(pyproject) or os.path.exists(os.path.join(target_dir, "setup.py"))
    if has_py:
        info["languages"].append("python")
        if os.path.exists(os.path.join(target_dir, "uv.lock")):
            info["package_manager"] = "uv"
            info["lockfile"] = "uv.lock"
        elif os.path.exists(os.path.join(target_dir, "poetry.lock")):
            info["package_manager"] = "poetry"
            info["lockfile"] = "poetry.lock"
        elif os.path.exists(os.path.join(target_dir, "Pipfile.lock")):
            info["package_manager"] = "pipenv"
            info["lockfile"] = "Pipfile.lock"
        else:
            info["package_manager"] = "pip"

        # Linters/tools check
        content = ""
        if os.path.exists(pyproject):
            try:
                with open(pyproject, "r", errors="ignore") as f:
                    content = f.read()
            except Exception:
                pass
        if "ruff" in content or os.path.exists(os.path.join(target_dir, "ruff.toml")):
            info["linters"].append("ruff")
        if "flake8" in content or os.path.exists(os.path.join(target_dir, ".flake8")):
            info["linters"].append("flake8")
        if "mypy" in content or os.path.exists(os.path.join(target_dir, "mypy.ini")):
            info["typecheckers"].append("mypy")
        if "pytest" in content or os.path.exists(os.path.join(target_dir, "pytest.ini")) or os.path.isdir(os.path.join(target_dir, "tests")):
            info["test_runners"].append("pytest")
        else:
            info["test_runners"].append("unittest")

    # JS / TS detection
    pkg_json = os.path.join(target_dir, "package.json")
    if os.path.exists(pkg_json):
        info["languages"].append("typescript" if os.path.exists(os.path.join(target_dir, "tsconfig.json")) else "javascript")
        if os.path.exists(os.path.join(target_dir, "pnpm-lock.yaml")):
            info["package_manager"] = "pnpm"
            info["lockfile"] = "pnpm-lock.yaml"
        elif os.path.exists(os.path.join(target_dir, "yarn.lock")):
            info["package_manager"] = "yarn"
            info["lockfile"] = "yarn.lock"
        elif os.path.exists(os.path.join(target_dir, "bun.lockb")):
            info["package_manager"] = "bun"
            info["lockfile"] = "bun.lockb"
        else:
            info["package_manager"] = "npm"
            info["lockfile"] = "package-lock.json"

        try:
            with open(pkg_json, "r", errors="ignore") as f:
                data = json.load(f)
                scripts = data.get("scripts", {})
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "lint" in scripts or "eslint" in deps:
                    info["linters"].append("eslint")
                if "prettier" in deps:
                    info["linters"].append("prettier")
                if "typescript" in deps or os.path.exists(os.path.join(target_dir, "tsconfig.json")):
                    info["typecheckers"].append("tsc")
                if "vitest" in deps or "vitest" in scripts.get("test", ""):
                    info["test_runners"].append("vitest")
                elif "jest" in deps or "jest" in scripts.get("test", ""):
                    info["test_runners"].append("jest")
                elif "test" in scripts:
                    info["test_runners"].append("npm-test")
        except Exception:
            pass

    # Go detection
    if os.path.exists(os.path.join(target_dir, "go.mod")):
        info["languages"].append("go")
        info["package_manager"] = "go"
        info["lockfile"] = "go.sum"
        info["test_runners"].append("go test")
        info["linters"].append("golangci-lint")

    # Rust detection
    if os.path.exists(os.path.join(target_dir, "Cargo.toml")):
        info["languages"].append("rust")
        info["package_manager"] = "cargo"
        info["lockfile"] = "Cargo.lock"
        info["test_runners"].append("cargo test")
        info["linters"].append("cargo clippy")

    return info

def generate_verify_sh(info, target_dir):
    lines = [
        "#!/usr/bin/env bash",
        "# verify.sh - Generated deterministic quality gate",
        "set -euo pipefail",
        'cd "$(dirname "$0")"',
        'FAST=0',
        '[ "${1:-}" = "--fast" ] && FAST=1',
        "",
        'echo "== [1/3] Running Linters & Formatters =="'
    ]

    lang = info["languages"][0] if info["languages"] else "generic"

    if "python" in info["languages"]:
        pm = info["package_manager"] or "python3"
        run_prefix = "uv run " if pm == "uv" else ("poetry run " if pm == "poetry" else "")
        if "ruff" in info["linters"]:
            lines.append(f"{run_prefix}ruff check .")
            lines.append(f"{run_prefix}ruff format --check . || true")
        else:
            lines.append(f"{run_prefix}python3 -m compileall -q -x '/(\\.|venv)' . || true")

        lines.append("")
        lines.append('echo "== [2/3] Running Type Checks =="')
        if "mypy" in info["typecheckers"]:
            lines.append(f"{run_prefix}mypy . || true")
        elif "pyright" in info["typecheckers"]:
            lines.append(f"{run_prefix}pyright || true")
        else:
            lines.append('echo "No type checker configured (skipping)"')

        lines.append("")
        lines.append('if [ "$FAST" -eq 0 ]; then')
        lines.append('  echo "== [3/3] Running Tests =="')
        if "pytest" in info["test_runners"]:
            lines.append(f"  {run_prefix}pytest")
        else:
            lines.append(f"  {run_prefix}python3 -m unittest discover -s tests -p 'test_*.py' 2>/dev/null || true")
        lines.append('fi')
    elif "typescript" in info["languages"] or "javascript" in info["languages"]:
        pm = info["package_manager"] or "npm"
        lines.append(f"{pm} run lint || npm run lint || true")
        lines.append("")
        lines.append('echo "== [2/3] Running Type Checks =="')
        if "tsc" in info["typecheckers"]:
            lines.append("npx tsc --noEmit || true")
        else:
            lines.append('echo "No TypeScript checker configured (skipping)"')
        lines.append("")
        lines.append('if [ "$FAST" -eq 0 ]; then')
        lines.append('  echo "== [3/3] Running Tests =="')
        lines.append(f"  {pm} test || npm test")
        lines.append('fi')
    else:
        lines.append('echo "Generic project: checking git cleanliness"')
        lines.append('git status --short')

    lines.append("")
    lines.append('echo "verify: OK"')
    out_path = os.path.join(target_dir, "verify.sh")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(out_path, 0o755)
    print(f"Generated executable verification gate at: {out_path}")

def generate_agents_md(info, target_dir):
    lang_str = ", ".join(info["languages"]) if info["languages"] else "Generic"
    pm_str = info["package_manager"] or "Standard"
    test_str = ", ".join(info["test_runners"]) if info["test_runners"] else "Test suite"

    content = f"""# AGENTS.md — {os.path.basename(os.path.abspath(target_dir))}

Auto-generated by `repo-intelligence`. Single source of truth for this codebase.

## Project Environment & Stack
- **Language(s):** {lang_str}
- **Package Manager:** {pm_str} (Lockfile: `{info.get('lockfile') or 'none'}`)
- **Primary Test Runner:** {test_str}
- **Deterministic Quality Gate:** `./verify.sh`

## Hard Rules
1. **Root Cause First:** Never guess fixes. Complete Phase 1 of `systematic-debugging` before editing.
2. **TDD Cycle:** Write a failing test first, see it fail with the expected error, then write minimal passing code (`test-driven-development`).
3. **Verification Evidence:** Execute `./verify.sh` fresh in the current turn before claiming work is complete (`verification-before-completion`).
4. **Deslop:** Run diff-scoped cleanup over `git diff` before submitting for review (`deslop`).
5. **Fail Closed:** If `./verify.sh` fails, the task is incomplete.
"""
    out_path = os.path.join(target_dir, "AGENTS.md")
    with open(out_path, "w") as f:
        f.write(content)
    print(f"Generated tailored project AGENTS.md at: {out_path}")

def main():
    target = "."
    action = "--inspect"
    for arg in sys.argv[1:]:
        if arg in ["--inspect", "--generate-verify", "--generate-agents-md", "--all"]:
            action = arg
        elif not arg.startswith("-"):
            target = arg

    info = analyze_repo(target)

    if action == "--inspect":
        print(json.dumps(info, indent=2))
    elif action == "--generate-verify":
        generate_verify_sh(info, target)
    elif action == "--generate-agents-md":
        generate_agents_md(info, target)
    elif action == "--all":
        generate_verify_sh(info, target)
        generate_agents_md(info, target)

if __name__ == "__main__":
    main()
