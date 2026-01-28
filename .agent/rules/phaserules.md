---
trigger: always_on
---

# Phase-Specific Rules

> **Purpose:** Define what's allowed/required at each development phase
> **Status:** 🟡 STABLE

---

## Overview

EVA is built incrementally using the Walking Skeleton approach.
Not all Constitution pillars can be enforced from day one.

This document specifies:
- What's **relaxed** in early phases
- What's **required** at each phase
- When full compliance begins

---

## Phase 0: Foundation

**Focus:** Infrastructure, interfaces, testing framework

### Allowed

- ✅ Mock state providers (no real PhysioCore)
- ✅ Mock resonance encoder (no real RMS)
- ✅ Simple in-memory bus (no full ResonanceBus)
- ✅ Basic file storage (no tiered memory)

### Required

- ✅ Port interfaces defined (IStateProvider, IBus, etc.)
- ✅ All code uses interfaces, not concrete classes
- ✅ Tests pass with mocks
- ✅ State-driven design (Pillar 3)
- ✅ Clean code standards (Pillar 4)

### Not Required

- ❌ Real biological simulation
- ❌ Full cognitive flow
- ❌ 8-8-8 memory tiering
- ❌ Resonance encoding

---

## Phase 1: MSP Core

**Focus:** Memory system standalone

### Allowed

- ✅ All Phase 0 relaxations
- ✅ Flat memory storage (no Session/Core/Sphere yet)

### Required

- ✅ MSP implements IMSPassport interface
- ✅ Episodic memory stores/retrieves
- ✅ Semantic memory stores/retrieves
- ✅ Vector search works
- ✅ Schema validation

### Not Required

- ❌ Resonance-based recall
- ❌ Memory compression
- ❌ Crosslinks

---

## Phase 2: Orchestration

**Focus:** Basic request routing, LLM integration

### Allowed

- ✅ Mock biological state in context
- ✅ Simplified cognitive flow

### Required

- ✅ Orchestrator routes requests
- ✅ LLM receives context
- ✅ Responses stored in MSP
- ✅ Session management works

### Not Required

- ❌ Bio-digital gap
- ❌ Emotional influence on response

---

## Phase 3: Psychology

**Focus:** EVA Matrix (emotions)

### Now Required (was relaxed)

- ⚠️ **Emotional state affects responses**
- ⚠️ **State persistence across sessions**

### Allowed

- ✅ Mock biological input to Matrix
- ✅ Simplified emotion model

### Required

- ✅ 9D emotional state vector
- ✅ Matrix publishes to bus
- ✅ MSP latches emotional state

---

## Phase 4: Biology

**Focus:** PhysioCore (hormones, vitals)

### Now Required (was relaxed)

- ⚠️ **Pillar 1: Embodied Existentialism ENFORCED**
- ⚠️ **Bio-digital gap must exist**

### Required

- ✅ Hormone simulation (6+ hormones)
- ✅ Vital signs calculation
- ✅ Homeostasis (decay to baseline)
- ✅ PhysioCore publishes to bus
- ✅ Gap completes < 100ms

---

## Phase 5: Perception

**Focus:** RMS, Artifact Qualia

### Now Required (was relaxed)

- ⚠️ **Pillar 2: Single-Inference Sequentiality ENFORCED**
- ⚠️ **Full resonance encoding**

### Required

- ✅ RMS encodes state to resonance format
- ✅ Qualia generated from emotional state
- ✅ Full Cognitive Flow 2.1

---

## Phase 6: Knowledge

**Focus:** GKS (Genesis Knowledge System)

### Required

- ✅ GKS loader works
- ✅ Genesis blocks accessible
- ✅ Crosslinks implemented

---

## Phase 7: Integration

**Focus:** Full system, production ready

### Now Required (was relaxed)

- ⚠️ **Pillar 5: Tiered Wisdom ENFORCED**
- ⚠️ **8-8-8 compression protocol**
- ⚠️ **All Constitution pillars FULLY ENFORCED**

### Required

- ✅ Full Cognitive Flow 2.1
- ✅ All systems integrated
- ✅ API endpoints working
- ✅ Response < 5 seconds
- ✅ All tests pass

---

## Compliance Checklist

| Pillar | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7 |
|--------|----|----|----|----|----|----|----|----|
| 1. Embodied | 🟡 | 🟡 | 🟡 | 🟡 | ✅ | ✅ | ✅ | ✅ |
| 2. Single-Inference | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ | ✅ | ✅ |
| 3. State Dominance | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4. Identity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5. Tiered Wisdom | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ✅ |

**Legend:** ✅ = Enforced, 🟡 = Relaxed (mock/simplified OK)
