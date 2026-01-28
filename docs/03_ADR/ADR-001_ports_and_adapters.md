# ADR-001: Ports & Adapters Pattern

> **Status:** Accepted
> **Date:** 2026-01-27
> **Deciders:** Lead Dev (Claude Opus 4.5), Project Owner

---

## Context

EVA is a complex system with multiple interdependent components:
- MSP (Memory) depends on PhysioCore state
- PhysioCore depends on Orchestrator stimuli
- EVA Matrix depends on PhysioCore hormones

In the original EVA v9.x, components were tightly coupled:

```python
# Tight coupling (v9.x problem)
from physio_core.physio_core import PhysioCore
from eva_matrix.eva_matrix import EVAMatrix

class MSP:
    def __init__(self):
        self.physio = PhysioCore()  # Direct dependency
        self.matrix = EVAMatrix()   # Direct dependency
```

**Problems:**
1. Cannot test MSP without running PhysioCore
2. Cannot develop MSP before PhysioCore exists
3. Circular dependency risks
4. Difficult to mock for testing

---

## Decision

Adopt the **Ports & Adapters** (Hexagonal Architecture) pattern:

```
┌─────────────────────────────────────────────────┐
│                    MSP Core                      │
│                                                  │
│  ┌──────────────┐         ┌──────────────┐      │
│  │    Port:     │         │    Port:     │      │
│  │ IStateProvider│        │ IResonance   │      │
│  │              │         │   Encoder    │      │
│  └──────┬───────┘         └──────┬───────┘      │
└─────────┼────────────────────────┼──────────────┘
          │                        │
          │ Implements             │ Implements
          │                        │
    ┌─────▼─────┐            ┌─────▼─────┐
    │  Adapter  │            │  Adapter  │
    │ MockPhysio│            │ MockRMS   │
    └───────────┘            └───────────┘
         OR                       OR
    ┌───────────┐            ┌───────────┐
    │  Adapter  │            │  Adapter  │
    │ PhysioCore│            │ RMSEngine │
    └───────────┘            └───────────┘
```

**Implementation:**

```python
# Port (Interface)
class IStateProvider(ABC):
    @abstractmethod
    def get_current_state(self) -> Dict[str, Any]: ...

# Adapter (Mock - Phase 1)
class MockPhysioProvider(IStateProvider):
    def get_current_state(self):
        return {"dopamine": 0.5, ...}

# Adapter (Real - Phase 4)
class PhysioCore(IStateProvider):
    def get_current_state(self):
        return self._calculate_real_hormones()

# Core (depends on Port, not Adapter)
class MSP:
    def __init__(self, state_provider: IStateProvider):
        self.state_provider = state_provider
```

---

## Consequences

### Positive

1. **Testability:** MSP can be tested with mocks
2. **Parallel Development:** Teams can work on different systems
3. **Incremental Build:** Phase 1 uses mocks, Phase 4 swaps in real
4. **Clear Contracts:** Interfaces define expectations
5. **Flexibility:** Can swap implementations without changing core

### Negative

1. **More Files:** Need interface + mock + real for each
2. **Indirection:** One more layer to understand
3. **Discipline Required:** Must program to interface, not implementation

### Neutral

1. **Learning Curve:** Team needs to understand pattern
2. **Boilerplate:** Some repetitive code in adapters

---

## Alternatives Considered

### 1. Direct Coupling (Status Quo)
- Rejected: Cannot build incrementally

### 2. Event-Driven Only
- Partially adopted: Bus handles some communication
- But interfaces still needed for synchronous calls

### 3. Dependency Injection Framework
- Rejected: Too heavy for current scale
- Manual DI is sufficient

---

## References

- [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Ports & Adapters Pattern](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
- Original EVA v9.x coupling issues
