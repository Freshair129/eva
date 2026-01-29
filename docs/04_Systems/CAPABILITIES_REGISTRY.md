# Capabilities Registry (Tool Definitions)

> **Module:** Capabilities (The "Hands" of EVA)
> **Purpose:** Defines all tools available to the LLM.
> **Status:** ⚠️ DRAFT

---

## 1. Core Cognitive Tools (Survival Tier)

These tools are essential for the agent to function as a continuous entity.

| Tool Name | Description | Python Signature |
|-----------|-------------|------------------|
| `recall_memory` | Retrieves relevant episodic or semantic memories. | `recall_memory(query: str, type: str = "all", limit: int = 5) -> List[Dict]` |
| `save_memory` | Explicitly saves a new memory or fact. | `save_memory(content: str, type: str = "episodic", importance: float = 0.5) -> str` |
| `introspect_state` | Returns the detailed internal state (Bio/Psych/Qualia). | `introspect_state() -> Dict` |
| `get_time` | Returns current date, time, and timezone. | `get_time() -> str` |
| `compress_state` | Encodes state dict to H5 string. | `compress_state(state: Dict) -> str` |

---

## 2. Interaction & Utility Tools (Functional Tier)

Basic utilities to enhance accuracy and capability.

| Tool Name | Description | Python Signature |
|-----------|-------------|------------------|
| `calculator` | Performs mathematical calculations safely. | `calculator(expression: str) -> float` |
| `calendar_check` | Checks usage of time/appointments (if implemented). | `calendar_check(date: str) -> List[Event]` |
| `random_number` | Generates randomness (for decisions/games). | `random_number(min: int, max: int) -> int` |

---

## 3. File System Tools (The "Hands")

Allows the agent to read/write files. **Requires careful permission handling.**

| Tool Name | Description | Python Signature |
|-----------|-------------|------------------|
| `read_file` | Reads content of a file (text/code). | `read_file(path: str) -> str` |
| `write_file` | Creates or overwrites a file. | `write_file(path: str, content: str) -> bool` |
| `list_files` | Lists files in a directory. | `list_files(path: str) -> List[str]` |
| `make_directory` | Creates a new folder. | `make_directory(path: str) -> bool` |

---

## 4. Advanced/Agentic Tools (Growth Tier)

Tools for high-level operations.

| Tool Name | Description | Python Signature |
|-----------|-------------|------------------|
| `web_search` | Searches the internet (via Serper/Google). | `web_search(query: str) -> List[Result]` |
| `plan_task` | Decomposes a goal into subtasks. | `plan_task(goal: str) -> List[Step]` |
| `generate_image` | Creates images from descriptions. | `generate_image(prompt: str) -> ImageURL` |
| `run_python` | Executes Python code in a sandbox. | `run_python(code: str) -> str` |

---

## 5. Security & Permissions

> [!IMPORTANT]
> **Sandboxing Policy:** Dangerous tools MUST require explicit user confirmation before execution.

| Security Level | Description | Behavior |
|----------------|-------------|----------|
| **L1: Safe** | Read-only, internal state | Auto-executed |
| **L2: Destructive** | File writing, deletion | **Requires Confirmation** |
| **L3: Remote/Code** | Web access, Python execution | **Requires Confirmation + Sandbox** |

---

## Implementation Structure

Each tool will be implemented as a class in `e:\eva\capabilities\`:

```
e:\eva\capabilities\
├── core\
│   ├── memory_tools.py      # [L1] recall_memory, save_memory
│   ├── time_tools.py        # [L1] get_time
│   └── state_tools.py       # [L1] introspect_state
├── filesystem\
│   └── file_ops.py          # [L1] read/list, [L2] write/mkdir
├── utility\
│   └── math_tools.py        # [L1] calculator
└── ...
```
