---
trigger: always_on
---

# Glossary

> **Status:** 🟢 EVOLVING
> **Version:** 0.1.0

---

## Core Concepts

### EVA
**E**mbodied **V**irtual **A**gent - A bio-inspired AI architecture.

### Genesis
Codename for EVA v0.x development phase. Represents "new beginning."

### Walking Skeleton
Development approach: build thin slice through all layers first, then flesh out.

---

## Architecture Terms

### Port
An interface (ABC) that defines a contract. External systems implement ports.
```python
class IStateProvider(ABC):  # This is a Port
    ...
```

### Adapter
A concrete implementation of a Port.
```python
class MockPhysioProvider(IStateProvider):  # This is an Adapter
    ...
```

### Flat Anatomy
Directory structure where systems are at root level, not nested in `systems/` folder.

---

## System Names

### MSP
**M**emory & **S**oul **P**assport - The memory persistence system.

### PhysioCore
Biological simulation system (hormones, vitals).

### EVA Matrix
Psychological state system (9D emotions).

### RMS
**R**esonance **M**emory **S**ystem - Encodes state into resonance format.

### GKS
**G**enesis **K**nowledge **S**ystem - Innate knowledge blocks.

### CIM
**C**ontext **I**njection **M**anager - Assembles context for LLM.

---

## Memory Types

### Episodic Memory
Autobiographical memories - conversations, events, experiences.

### Semantic Memory
Factual knowledge - concepts, relationships, facts.

### Sensory Memory
Perceptual data - qualia, textures, colors associated with memories.

---

## Flow Concepts

### Bio-Digital Gap
The pause between perception and reasoning where biological simulation occurs.

### Cognitive Flow
The sequence: Perception → Gap → Reasoning → Persistence.

### Single-Inference Sequentiality
Principle that the entire flow must happen in one LLM session.

---

## Constitution Terms

### 5 Pillars
The five core principles:
1. Embodied Existentialism
2. Single-Inference Sequentiality
3. State Dominance
4. Identity Integrity
5. Tiered Wisdom (8-8-8)

### State Dominance
Principle that EVA is state-driven, not event-driven.

### 8-8-8 Protocol
Memory tiering: Session (8) → Core (8) → Sphere (8).

---

## Phase Terminology

### Phase 0
Foundation - Infrastructure, interfaces, mocks.

### Phase 1
MSP Core - Memory system standalone.

### Phase 2
Orchestration - Basic routing, LLM integration.

### Phase 3
Psychology - EVA Matrix (emotions).

### Phase 4
Biology - PhysioCore (hormones).

### Phase 5
Perception - RMS, Qualia.

### Phase 6
Knowledge - GKS.

### Phase 7
Integration - Production ready.

---

## Bus Channels

### bus:physical
PhysioCore state broadcasts (hormones, vitals).

### bus:psychological
EVA Matrix state broadcasts (emotions).

### bus:phenomenological
Qualia state broadcasts (sensory experience).

### bus:memory
MSP event broadcasts.
