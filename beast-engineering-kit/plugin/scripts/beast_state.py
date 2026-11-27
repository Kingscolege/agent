#!/usr/bin/env python3
"""
BEAST Mode State & Trigger Recognition Engine.
Provides persistent conversation state tracking and trigger parsing for
BEAST, DEBUG, AUDIT, REVIEW, and NORMAL workflows.
"""
import os
import sys
import json
import re
import time

def get_state_file_path() -> str:
    plugin_data = os.environ.get("PLUGIN_DATA")
    if plugin_data and os.path.isdir(plugin_data):
        return os.path.join(plugin_data, "beast_state.json")

    home = os.path.expanduser("~")
    gemini_data = os.path.join(home, ".gemini", "antigravity-cli", "plugin_data", "engineering-agent-kit")
    try:
        os.makedirs(gemini_data, exist_ok=True)
        return os.path.join(gemini_data, "beast_state.json")
    except Exception:
        return os.path.join(os.path.expanduser("~"), ".beast_state.json")

def load_all_states() -> dict:
    path = get_state_file_path()
    if os.path.exists(path):
        try:
            with open(path, "r", errors="ignore") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_all_states(states: dict):
    path = get_state_file_path()
    temp_path = f"{path}.tmp.{os.getpid()}"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(temp_path, "w") as f:
            json.dump(states, f, indent=2)
        os.replace(temp_path, path)
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

def get_active_mode(conversation_id: str) -> str:
    """Returns 'beast', 'debug', 'audit', 'review', or ''."""
    if not conversation_id:
        return ""
    states = load_all_states()
    entry = states.get(conversation_id)
    if entry and entry.get("active"):
        return entry.get("mode", "beast")
    return ""

def is_beast_active(conversation_id: str) -> bool:
    mode = get_active_mode(conversation_id)
    return mode != ""

def activate_mode(conversation_id: str, mode: str, task: str = "") -> dict:
    states = load_all_states()
    entry = {
        "active": True,
        "mode": mode.lower(),
        "activated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "task": task.strip() if task else ""
    }
    states[conversation_id] = entry
    save_all_states(states)
    return entry

def activate_beast(conversation_id: str, task: str = "") -> dict:
    return activate_mode(conversation_id, "beast", task)

def deactivate_beast(conversation_id: str) -> bool:
    states = load_all_states()
    if conversation_id in states:
        states[conversation_id]["active"] = False
        states[conversation_id]["deactivated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        save_all_states(states)
        return True
    return False

def parse_trigger(user_input: str) -> dict:
    """
    Parses user input for BEAST / DEBUG / AUDIT / REVIEW / NORMAL triggers.
    Recognizes:
      - BEAST, beast, /beast -> action: 'activate_beast'
      - DEBUG, debug, /debug -> action: 'activate_debug'
      - AUDIT, audit, /audit -> action: 'activate_audit'
      - REVIEW, review, /review -> action: 'activate_review'
      - NORMAL, normal, /normal -> action: 'deactivate'
    Returns dict:
      {"action": str, "task": str, "mode": str}
    """
    if not user_input or not isinstance(user_input, str):
        return {"action": "none", "task": "", "mode": ""}

    text = user_input.strip()

    # Pattern for BEAST trigger
    m = re.match(r"^(?:/)?beast(?:\b\s*[:\-]?\s*(.*))?$", text, re.IGNORECASE | re.DOTALL)
    if m:
        task = (m.group(1) or "").strip()
        return {"action": "activate", "task": task, "mode": "beast"}

    # Pattern for DEBUG trigger
    m = re.match(r"^(?:/)?debug(?:\b\s*[:\-]?\s*(.*))?$", text, re.IGNORECASE | re.DOTALL)
    if m:
        task = (m.group(1) or "").strip()
        return {"action": "activate", "task": task, "mode": "debug"}

    # Pattern for AUDIT trigger
    m = re.match(r"^(?:/)?audit(?:\b\s*[:\-]?\s*(.*))?$", text, re.IGNORECASE | re.DOTALL)
    if m:
        task = (m.group(1) or "").strip()
        return {"action": "activate", "task": task, "mode": "audit"}

    # Pattern for REVIEW trigger
    m = re.match(r"^(?:/)?review(?:\b\s*[:\-]?\s*(.*))?$", text, re.IGNORECASE | re.DOTALL)
    if m:
        task = (m.group(1) or "").strip()
        return {"action": "activate", "task": task, "mode": "review"}

    # Pattern for NORMAL deactivation trigger
    m = re.match(r"^(?:/)?normal(?:\b\s*[:\-]?\s*(.*))?$", text, re.IGNORECASE | re.DOTALL)
    if m:
        return {"action": "deactivate", "task": (m.group(1) or "").strip(), "mode": "normal"}

    return {"action": "none", "task": "", "mode": ""}

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--parse":
        print(json.dumps(parse_trigger(sys.argv[2])))
