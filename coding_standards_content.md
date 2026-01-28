---
trigger: always_on
priority: high
---

# Coding Standards

> **Status:** 🟡 STABLE
> **Version:** 0.1.0

---

## Python Standards

### Version

- Python 3.11+

### Formatting

- **Formatter:** Black (default settings)
- **Import Sorter:** isort
- **Line Length:** 88 characters (Black default)

### Type Hints

**Required** for all functions:

```python
# Good
def get_state(self, slot: str) -> Optional[Dict[str, Any]]:
    ...

# Bad
def get_state(self, slot):
    ...
```

### Docstrings

**Required** for public functions and classes:

```python
def store_episode(self, episode_data: Dict[str, Any]) -> str:
    """
    Stores an episodic memory record.

    Args:
        episode_data: Dictionary containing episode information

    Returns:
        Unique episode ID

    Raises:
        ValidationError: If episode_data fails schema validation
    """
    ...
```

### Import Order

```python
# 1. Standard library
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 2. Third-party
import yaml
from pydantic import BaseModel

# 3. Local - Contracts (interfaces)
from contracts.ports.i_state_provider import IStateProvider
from contracts.ports.i_bus import IBus

# 4. Local - Implementations
from adapters.mocks.mock_state_providers import MockPhysioProvider
```

---

## File Naming

| Type | Convention | Example |
|------|------------|---------|
| Interface | `i_name.py` | `i_state_provider.py` |
| Implementation | `name.py` | `simple_bus.py` |
| Mock | `mock_name.py` | `mock_state_providers.py` |
| Test | `test_name.py` | `test_simple_bus.py` |
| Config | `name.yaml` | `master_registry.yaml` |

---

## Directory Standards

### Flat Anatomy (ADR-002)

Systems at root level, not nested:

```python
# Good
from msp.msp_engine import MSP
from physio_core.physio_core import PhysioCore

# Bad
from systems.memory.msp.msp_engine import MSP
```

### Package Structure

Every Python package needs `__init__.py`:

```
contracts/
├── __init__.py
└── ports/
    ├── __init__.py
    ├── i_state_provider.py
    └── i_bus.py
```

---

## Code Quality

### No Print Statements

Use logging instead:

```python
# Bad
print(f"Processing {item}")

# Good
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing {item}")
```

### No Hardcoded Paths

Use configuration or Path:

```python
# Bad
path = "E:/eva/config/settings.yaml"

# Good
from pathlib import Path
path = Path(__file__).parent / "config" / "settings.yaml"
```

### Interface-First (ADR-001)

Depend on interfaces, not implementations:

```python
# Bad
from adapters.simple_bus import SimpleBus

class MSP:
    def __init__(self):
        self.bus = SimpleBus()  # Concrete class

# Good
from contracts.ports.i_bus import IBus

class MSP:
    def __init__(self, bus: IBus):  # Interface
        self.bus = bus
```

---

## Testing Standards

### Test Structure

```
tests/
├── unit/           # Isolated unit tests
├── integration/    # Cross-module tests
└── e2e/            # End-to-end tests
```

### Naming

```python
# test_[module]_[function]_[scenario].py
test_simple_bus_publish_stores_latest.py

# Or class-based
class TestSimpleBus:
    def test_publish_stores_latest(self):
        ...
```

### Fixtures

Use pytest fixtures from `conftest.py`:

```python
# tests/conftest.py
@pytest.fixture
def simple_bus():
    bus = SimpleBus()
    yield bus
    bus.clear()

# tests/unit/test_something.py
def test_publish(simple_bus):  # Fixture injected
    simple_bus.publish("channel", {"data": "test"})
```

---

## Git Standards

### Commit Messages

```
[Phase X] Brief description

- Detail 1
- Detail 2
```

Example:
```
[Phase 0] Add IStateProvider interface

- Create contracts/ports/i_state_provider.py
- Define get_current_state, get_state_type, get_provider_id
- Add type hints and docstrings
```

### Branch Naming

```
phase-0/task-002-istate-provider
phase-1/msp-engine
bugfix/memory-leak
```
