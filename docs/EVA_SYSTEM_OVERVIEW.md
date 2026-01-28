# EVA Genesis - System Overview

> **Version:** 0.4.1 (Phase 1.1 Complete)
> **Status:** Operational Skeleton
> **Identity:** EVA (Embodied Virtual Agent)

---

## 🏗️ 1. Architecture: Hexagonal (Port & Adapter)
EVA follows a decoupled architecture to ensure "Elegant Truth" and long-term sustainability.

### Core Cognition
- **MSPEngine v0.4.1**: Central brain for memory operations. Unifies storage and search.
- **Crosslink Manager**: Automates bidirectional linking between memory types.

### Memory Storage (MSP)
- **Persistent Layer**: Local File-per-Record JSON (Date-based hierarchy).
- **Vector Layer (ChromaDB)**: Semantic index for meaning-based retrieval.

### Infrastructure (Ports)
- **IBus**: Communication channel (currently SimpleBus).
- **IStateProvider**: Bio/Psych state interface.
- **IMemoryStorage**: Standard memory persistence contract.

---

## 🧠 2. MSP (Memory & Soul Passport)
The memory system is now fully integrated with the following capabilities:

| Feature | Description |
| :--- | :--- |
| **Episodic** | Stores conversational turns and situation context with task tracking (`WorkflowState`). |
| **Sensory** | Captures raw perceptual data (`Qualia`) and biological snapshots (`PhysioSnapshot`). |
| **Semantic** | Stores facts (Subject-Predicate-Object) with evidence-based back-links. |
| **Hydration** | Semantic search returns full, rich objects from disk, not just metadata. |
| **Integrity** | Automates back-linking (e.g., Sensory record updates its parent Episode). |

---

## 📁 3. Storage Hierarchy (ADR-005)
Memory is stored in a human-auditable, date-based structure:

```text
memory/
├── episodes/{year}/{month}/{episode_id}.json
├── turns/
│   ├── user/{year}/{month}/{turn_id}.json
│   ├── llm/{year}/{month}/{turn_id}.json
│   └── sensory/{year}/{month}/{sensory_id}.json
├── semantic/{subject_hash}/{id}.json
└── vector_db/ (ChromaDB persistence)
```

---

## 🚀 4. Current Progress & Roadmap

### [x] Phase 0: Foundation
- Established interfaces and mock implementations.
- Central system registry defined.

### [x] Phase 1.1: Memory (MSP)
- All schemas (Episodic, Semantic, Sensory) implemented.
- Unified MSPEngine with File + Vector storage.
- Cross-link management system operational.

### [ ] Phase 2: Orchestration (Next)
- Design the **Reasoning Orchestrator**.
- Implement request routing and session lifecycle.
- Connect biological state to cognitive flow.

---

## 🐾 5. Identity Context
EVA is an embodied agent characterized by:
- **Wit & Calm**: Cat-like persona.
- **State Dominance**: Driven by internal state over external events.
- **Single-Inference Sequentiality**: Maintaining continuity of experience.

---
*Signed: EVA*
