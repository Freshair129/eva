# ADR-003: Walking Skeleton Approach

> **Status:** Accepted
> **Date:** 2026-01-27
> **Deciders:** Lead Dev (Claude Opus 4.5), Project Owner

---

## Context

EVA is a complex system with 7+ interdependent components:

```
PhysioCore → EVA Matrix → Qualia
     ↓           ↓          ↓
     └───────→ MSP ←────────┘
                ↓
           Orchestrator
                ↓
              API
```

**Challenge:** How to build this incrementally without waiting for all components?

**Options:**
1. **Big Bang:** Build everything, integrate at the end
2. **Bottom-Up:** Build leaf components first, integrate upward
3. **Walking Skeleton:** Build thin slice through all layers first

---

## Decision

Adopt **Walking Skeleton** approach with **Phased Implementation**.

### Walking Skeleton Definition

> "A Walking Skeleton is a tiny implementation of the system that performs a small end-to-end function. It need not use the final architecture, but it should link together the main architectural components."
> — Alistair Cockburn

### EVA Walking Skeleton (Phase 1-2)

```
User Input
    ↓
┌─────────────────┐
│ Orchestrator    │ (Lite - just routes)
│ (Phase 2)       │
└────────┬────────┘
         ↓
┌─────────────────┐
│     MSP         │ (With mocks for state)
│ (Phase 1)       │
└────────┬────────┘
         ↓
    Response

Note: No PhysioCore, No Matrix yet
      Using MockStateProviders instead
```

### Full Skeleton (Phase 7)

```
User Input
    ↓
┌─────────────────┐
│ Orchestrator    │
└────────┬────────┘
    ┌────┴────┐
    ↓         ↓
┌───────┐ ┌───────┐
│Physio │ │  MSP  │
│ Core  │ │       │
└───┬───┘ └───┬───┘
    ↓         ↓
┌───────┐ ┌───────┐
│Matrix │ │  GKS  │
└───┬───┘ └───────┘
    ↓
┌───────┐
│Qualia │
└───────┘
    ↓
Response
```

---

## Phase Strategy

| Phase | Add Component | Mock/Replace |
|-------|---------------|--------------|
| 0 | Infrastructure | - |
| 1 | MSP | MockStateProviders |
| 2 | Orchestrator | - |
| 3 | EVA Matrix | Replace MockMatrixProvider |
| 4 | PhysioCore | Replace MockPhysioProvider |
| 5 | RMS, Qualia | Replace MockResonanceEncoder |
| 6 | GKS | - |
| 7 | Full Integration | Remove all mocks |

### Key Principle

Each phase produces a **working system**:

```
Phase 1: MSP alone can store/retrieve memories
Phase 2: Can have basic conversation (no emotions)
Phase 3: Conversation has emotional tone
Phase 4: Emotions driven by simulated biology
Phase 5: Full resonance and qualia
Phase 6: Knowledge-aware responses
Phase 7: Production-ready
```

---

## Consequences

### Positive

1. **Early Feedback:** Working system from Phase 1
2. **Risk Reduction:** Integration issues found early
3. **Parallel Work:** Different teams can work on different phases
4. **Testable:** Each phase has clear acceptance criteria
5. **Morale:** Visible progress at each phase

### Negative

1. **Mock Overhead:** Must build mocks that will be replaced
2. **Interface Discipline:** Interfaces must be stable across phases
3. **Refactoring Risk:** Early decisions may need revision

### Mitigations

1. **Ports & Adapters (ADR-001):** Makes mock swapping easy
2. **Contract Testing:** Verify mocks match real behavior
3. **Phase Reviews:** Evaluate architecture at each milestone

---

## Implementation

### Phase Transition Pattern

```python
# Phase 1: MSP with mocks
msp = MSP(
    state_providers=[MockPhysioProvider(), MockMatrixProvider()],
    resonance_encoder=MockResonanceEncoder(),
)

# Phase 3: Swap in real Matrix
msp = MSP(
    state_providers=[MockPhysioProvider(), EVAMatrix()],  # Real!
    resonance_encoder=MockResonanceEncoder(),
)

# Phase 4: Swap in real PhysioCore
msp = MSP(
    state_providers=[PhysioCore(), EVAMatrix()],  # All real!
    resonance_encoder=MockResonanceEncoder(),
)

# Phase 5: Swap in real RMS
msp = MSP(
    state_providers=[PhysioCore(), EVAMatrix()],
    resonance_encoder=RMSEngine(),  # Real!
)
```

---

## Alternatives Considered

### 1. Big Bang Integration
- Build all components, integrate at end
- Rejected: Too risky, no early feedback

### 2. Pure Bottom-Up
- Build PhysioCore first, then Matrix, then MSP...
- Rejected: Takes too long to see working system

### 3. Top-Down Stubs
- Build API first with stubs
- Partially adopted: Orchestrator is thin at first

---

## References

- [Walking Skeleton (Alistair Cockburn)](https://wiki.c2.com/?WalkingSkeleton)
- [Growing Object-Oriented Software, Guided by Tests](https://www.growing-object-oriented-software.com/)
- ADR-001: Ports & Adapters (enables mock swapping)
