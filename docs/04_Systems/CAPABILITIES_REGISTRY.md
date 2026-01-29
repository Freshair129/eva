# Capabilities Registry (Tool Definitions)

> **Module:** Capabilities (The "Hands" of EVA)
> **Purpose:** Defines all tools available to the LLM.
> **Status:** ✅ IMPLEMENTED (v0.1.0)
> **Total Tools:** 23

---

## 1. Core Cognitive Tools (L1 - Auto-execute)

Essential tools for the agent to function as a continuous entity.

| Tool | Description | Module |
|------|-------------|--------|
| `recall_memory` | Retrieves episodic/semantic memories | `core.memory_tools` |
| `save_memory` | Saves new memory or fact | `core.memory_tools` |
| `introspect_state` | Returns Bio/Psych/Qualia state | `core.state_tools` |
| `compress_state` | Encodes state to E9 string | `core.state_tools` |
| `get_time` | Returns datetime with timezone | `core.time_tools` |
| `get_timestamp` | Returns Unix timestamp | `core.time_tools` |
| `format_relative_time` | "2 hours ago" format | `core.time_tools` |

---

## 2. Utility Tools (L1 - Auto-execute)

Mathematical and random utilities.

| Tool | Description | Module |
|------|-------------|--------|
| `calculator` | Safe math expressions (sqrt, sin, pi) | `utility.math_tools` |
| `random_number` | Random integer in range | `utility.math_tools` |
| `random_choice` | Pick random from list | `utility.math_tools` |
| `dice_roll` | Simulate dice (e.g., 2d6) | `utility.math_tools` |

---

## 3. File System Tools (L1/L2)

File operations with sandbox protections.

| Tool | Security | Description | Module |
|------|----------|-------------|--------|
| `read_file` | L1 | Read file content | `filesystem.file_ops` |
| `list_files` | L1 | List directory contents | `filesystem.file_ops` |
| `write_file` | **L2** | Create/overwrite file | `filesystem.file_ops` |
| `make_directory` | **L2** | Create folder | `filesystem.file_ops` |
| `delete_file` | **L2** | Delete file | `filesystem.file_ops` |

---

## 4. Agentic Tools (L1/L3)

Advanced operations for autonomous behavior.

| Tool | Security | Description | Module |
|------|----------|-------------|--------|
| `web_search` | **L3** | Search internet (DDG/Serper) | `agentic.web_tools` |
| `fetch_url` | **L3** | Fetch URL content | `agentic.web_tools` |
| `run_python` | **L3** | Execute Python (sandbox) | `agentic.code_tools` |
| `evaluate_expression` | L1 | Safe expression eval | `agentic.code_tools` |
| `plan_task` | L1 | Decompose goal to steps | `agentic.planning_tools` |
| `track_progress` | L1 | Update plan progress | `agentic.planning_tools` |
| `reflect_on_task` | L1 | Record lessons learned | `agentic.planning_tools` |

---

## 5. Security Levels

> [!IMPORTANT]
> L2/L3 tools require `_confirmed=True` to execute.

| Level | Description | Behavior |
|-------|-------------|----------|
| **L1: Safe** | Read-only, internal state | Auto-executed |
| **L2: Destructive** | File writing, deletion | Requires Confirmation |
| **L3: Remote/Code** | Web access, code execution | Requires Confirmation + Sandbox |

---

## 6. Sandbox Protections

```python
# File System
ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".yaml", ".yml", ".py", ".js", ".html", ".css"}
MAX_FILE_SIZE = 1MB
FORBIDDEN_PATHS = {"C:\\Windows", "/etc", "/usr"}

# Code Execution
BLOCKED_IMPORTS = {"os", "sys", "subprocess", "socket", ...}
ALLOWED_MODULES = {"math", "random", "datetime", "json", "re", ...}
```

---

## 7. Implementation Structure

```
e:\eva\capabilities\
├── __init__.py              # Package exports
├── core\
│   ├── memory_tools.py      # [L1] recall/save
│   ├── time_tools.py        # [L1] time utilities
│   └── state_tools.py       # [L1] E9 codec, introspect
├── filesystem\
│   └── file_ops.py          # [L1/L2] file operations
├── utility\
│   └── math_tools.py        # [L1] calculator, dice
└── agentic\
    ├── web_tools.py         # [L3] web search, fetch
    ├── code_tools.py        # [L1/L3] python execution
    └── planning_tools.py    # [L1] task planning
```

---

## 8. Usage Example

```python
from capabilities import (
    get_time, calculator, web_search, 
    introspect_state, compress_state
)

# L1: Auto-execute
print(get_time())  # "2026-01-30 00:48:00 (SE Asia Standard Time)"
print(calculator("sqrt(16) + pi"))  # 7.14...

# L3: Requires confirmation
result = web_search("EVA AI", provider="duckduckgo", _confirmed=True)
```
