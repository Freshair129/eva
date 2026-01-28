# CLAUDE.md

This file provides guidance to Claude Code when working with the EVA codebase.

## Project Overview

**EVA** (Embodied Virtual Agent) - Bio-inspired AI architecture implementing "Resonance Intelligence" framework.

**Version:** 0.1.0 (Genesis)
**Status:** Development Phase 0

## Quick Start

```bash
# Run tests
python -m pytest tests/

# Run MSP standalone (Phase 1+)
python -m msp.cli
```

## Architecture

### Core Principles

1. **Flat Anatomy** - All systems at root level
2. **Registry-Centric** - `config/master_registry.yaml` is SSOT
3. **Ports & Adapters** - Interfaces in `contracts/`, implementations in `adapters/`
4. **Walking Skeleton** - Minimal working system, add features incrementally

### Directory Structure

```
eva/
├── contracts/        # Interfaces (Ports)
├── adapters/         # Implementations (Adapters)
├── msp/              # Memory system
├── orchestrator/     # CNS
├── eva_matrix/       # Psychology
├── physio_core/      # Biology
├── consciousness/    # Runtime state
├── memory/           # Persistent storage
├── config/           # Configuration
└── tests/            # All tests
```

### Development Phases

| Phase | System | Status |
|-------|--------|--------|
| 0 | Foundation | Done |
| 1 | MSP | Current |

| 2 | Orchestrator | Pending |
| 3 | EVA Matrix | Pending |
| 4 | PhysioCore | Pending |

## Coding Standards

### Python

- Python 3.11+
- Type hints required
- Docstrings for public functions
- Black formatting
- isort for imports

### File Naming

```
module_name.py          # Snake case
ModuleName.py           # Only for single-class files
test_module_name.py     # Test files
```

### Import Order

```python
# 1. Standard library
import json
from pathlib import Path

# 2. Third party
import yaml

# 3. Local - Contracts first
from contracts.ports import IStateProvider

# 4. Local - Implementations
from adapters.mocks import MockStateProvider
```

## Task System

Tasks are defined in `.planning/tasks/` as YAML files.

```yaml
# .planning/tasks/TASK_001.yaml
id: TASK_001
title: "Create IStateProvider interface"
phase: 0
status: pending  # pending | in_progress | done | blocked
priority: high
spec: ".planning/specs/SPEC_001_state_provider.md"
```

## Testing

```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Specific test
python -m pytest tests/unit/test_msp.py -v
```

## Important Files

- `PROJECT.md` - Project overview and roadmap
- `VERSION` - Current version number
- `CHANGELOG.md` - Version history
- `config/master_registry.yaml` - System topology SSOT
- `.planning/STATE.md` - Current development state
