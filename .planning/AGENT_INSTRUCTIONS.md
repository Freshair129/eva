# Agent Instructions

> **For:** Antigravity / Gemini Agents
> **Project:** EVA Genesis (v0.1.0)
> **Lead Dev:** Claude Opus 4.5

---

## How to Work on Tasks

### 1. Pick a Task

Look in `.planning/tasks/` for YAML files with `status: pending`

```yaml
# Example task file
id: P0-002
status: pending  # <-- This means it's available
depends_on: []   # <-- Check dependencies are done
```

### 2. Check Dependencies

Before starting, verify that `depends_on` tasks are complete:

```yaml
depends_on: [P0-002]  # P0-002 must be done first
```

### 3. Read the Spec

Each task has a `spec:` section with exact code to implement.

**Follow the spec exactly** - don't add extra features or "improvements".

### 4. Create the File

Output file path is specified in `output_file:` or `output_files:`

```yaml
output_file: "contracts/ports/i_state_provider.py"
```

### 5. Verify Acceptance Criteria

Each task has `acceptance_criteria:` - make sure all are met.

### 6. Update Task Status

After completing, update the task YAML:

```yaml
status: done  # Changed from 'pending'
completed_at: "2026-01-27T15:00:00"
completed_by: "gemini-agent-1"
```

---

## Directory Structure

```
E:\eva\
├── .planning/
│   ├── tasks/           # Task definitions (YAML)
│   ├── specs/           # Detailed specifications
│   └── STATE.md         # Current project state
│
├── contracts/
│   └── ports/           # Interface files go here
│
├── adapters/
│   └── mocks/           # Mock implementations go here
│
├── config/              # Configuration files
├── tests/               # Test files
└── ...
```

---

## Task Priority Order

Execute tasks in this order (respecting dependencies):

### Wave 1 (No Dependencies)
- P0-002: IStateProvider
- P0-003: IResonanceEncoder
- P0-004: IBus
- P0-005: IMemoryStorage

### Wave 2 (Depends on Wave 1)
- P0-006: MockStateProviders (needs P0-002)
- P0-007: MockResonanceEncoder (needs P0-003)
- P0-008: SimpleBus (needs P0-004)
- P0-009: master_registry.yaml

### Wave 3 (Depends on Wave 2)
- P0-010: pytest setup (needs P0-006, P0-007, P0-008)

---

## Code Standards

### Python Files

```python
"""
Module description.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

# Type hints required
# Docstrings required for public functions
# No print statements (use logging if needed)
```

### File Naming

- Interfaces: `i_name.py` (e.g., `i_state_provider.py`)
- Implementations: `name.py` (e.g., `simple_bus.py`)
- Mocks: `mock_name.py` (e.g., `mock_state_providers.py`)

### Imports

```python
# Standard library first
from abc import ABC
from typing import Dict

# Third party
import yaml  # if needed

# Local imports last
from contracts.ports.i_bus import IBus
```

---

## Important Notes

1. **Don't over-engineer** - Implement exactly what the spec says
2. **Don't add features** - Phase 1 will add more, not now
3. **Follow flat structure** - No nested folders beyond what's specified
4. **Create __init__.py** - For all Python packages
5. **Type hints required** - All functions must have type hints

---

## Reporting

After completing a task, you can report:

```
Task P0-002 completed.
- Created: contracts/ports/i_state_provider.py
- Lines: 28
- All acceptance criteria met.
```

---

## Questions?

If spec is unclear:
1. Check existing code in `E:\The Human Algorithm\T2\agent\` for reference
2. Ask Lead Dev (Claude) for clarification
3. Note the question in task file and move to next task
