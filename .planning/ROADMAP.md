# EVA Genesis - Master Roadmap

> **Version:** 0.1.0
> **Created:** 2026-01-27
> **Approach:** Walking Skeleton → Incremental Integration
> **Target:** v1.0.0 (Production Ready)

---

## Overview

EVA (Embodied Virtual Agent) เป็น Bio-inspired AI Architecture ที่จำลองกระบวนการทางชีววิทยาและจิตวิทยา เพื่อสร้าง AI ที่ "รู้สึก" ผ่านระบบฮอร์โมน อารมณ์ และความทรงจำ

### Core Philosophy
- **Embodied Existentialism** - AI ที่มี "ร่างกาย" เสมือน
- **Single-Inference Sequentiality** - ทุกอย่างเกิดใน LLM session เดียว
- **State Dominance** - State-driven ไม่ใช่ Event-driven
- **Bio-Digital Gap** - จังหวะหยุดระหว่าง perception กับ reasoning

---

## Phase Summary

| Phase | Name | Description | Tasks | Status |
|-------|------|-------------|-------|--------|
| 0 | Foundation | Infrastructure, Contracts, Mocks | 10 | ✅ Done |
| 1 | MSP Core | Memory & Soul Passport | 8 | 🔄 Ready |
| 2 | Orchestration | CNS, Routing, LLM Bridge | 10 | ⏳ Pending |
| 3 | Psychology | EVA Matrix (9D Emotions) | 8 | ⏳ Pending |
| 4 | Biology | PhysioCore (Hormones) | 10 | ⏳ Pending |
| 5 | Perception | RMS, Qualia | 8 | ⏳ Pending |
| 6 | Knowledge | GKS (Genesis Blocks) | 6 | ⏳ Pending |
| 7 | Integration | Full System, API, Production | 8 | ⏳ Pending |

**Total Tasks:** 68

---

## Phase 0: Foundation ✅

> **Status:** COMPLETED
> **Version:** 0.1.0
> **Deliverables:** Contracts, Mocks, Test Infrastructure

### Completed Tasks

| ID | Task | Output |
|----|------|--------|
| P0-001 | Directory structure | Project scaffold |
| P0-002 | IStateProvider | `contracts/ports/i_state_provider.py` |
| P0-003 | IResonanceEncoder | `contracts/ports/i_resonance_encoder.py` |
| P0-004 | IBus | `contracts/ports/i_bus.py` |
| P0-005 | IMemoryStorage | `contracts/ports/i_memory_storage.py` |
| P0-006 | MockStateProviders | `adapters/mocks/mock_state_providers.py` |
| P0-007 | MockResonanceEncoder | `adapters/mocks/mock_resonance_encoder.py` |
| P0-008 | SimpleBus | `adapters/simple_bus.py` |
| P0-009 | master_registry.yaml | `config/master_registry.yaml` |
| P0-010 | Pytest setup | `tests/`, `pytest.ini` |

---

## Phase 1: MSP Core 🔄

> **Goal:** Memory system ที่ทำงานได้ standalone
> **Dependencies:** Phase 0
> **Deliverables:** MSP Engine, Memory Schemas, ChromaDB Bridge

### Architecture

```
msp/
├── __init__.py
├── msp_engine.py           # Core engine
├── schema/
│   ├── episodic.py         # Autobiographical memories
│   ├── semantic.py         # Facts & knowledge
│   └── sensory.py          # Qualia memories
├── storage/
│   ├── memory_store.py     # IMemoryStorage implementation
│   └── chroma_bridge.py    # Vector DB adapter
└── tests/
    └── test_msp.py
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P1-001 | Create MSP directory structure | high | - | 10 |
| P1-002 | Define EpisodicMemory schema | high | P1-001 | 60 |
| P1-003 | Define SemanticMemory schema | high | P1-001 | 50 |
| P1-004 | Define SensoryMemory schema | high | P1-001 | 40 |
| P1-005 | Implement MemoryStore (IMemoryStorage) | high | P1-002,003,004 | 120 |
| P1-006 | Implement ChromaBridge | medium | P1-005 | 100 |
| P1-007 | Create MSP Engine | high | P1-005,006 | 150 |
| P1-008 | MSP unit tests | medium | P1-007 | 100 |

### Success Criteria
- [ ] MSP can store episodic memory
- [ ] MSP can retrieve by similarity (ChromaDB)
- [ ] MSP can list memories by type
- [ ] All tests pass

---

## Phase 2: Orchestration

> **Goal:** Basic conversation flow ทำงานได้
> **Dependencies:** Phase 1
> **Deliverables:** Orchestrator, CIM, LLM Bridge

### Architecture

```
orchestrator/
├── __init__.py
├── orchestrator_engine.py   # CNS - Central Nervous System
├── cim/
│   ├── __init__.py
│   ├── cim_engine.py        # Context Injection Manager
│   └── context_builder.py   # Build LLM context
├── llm_bridge/
│   ├── __init__.py
│   ├── llm_interface.py     # ILLMProvider port
│   ├── ollama_adapter.py    # Ollama implementation
│   └── mock_llm.py          # Mock for testing
└── tests/
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P2-001 | Create Orchestrator directory | high | P1 | 10 |
| P2-002 | Define ILLMProvider interface | high | P2-001 | 40 |
| P2-003 | Implement MockLLM | high | P2-002 | 60 |
| P2-004 | Implement OllamaAdapter | medium | P2-002 | 100 |
| P2-005 | Create CIM Engine | high | P2-001 | 120 |
| P2-006 | Create ContextBuilder | high | P2-005 | 80 |
| P2-007 | Create Orchestrator Engine | high | P2-005,006 | 150 |
| P2-008 | Wire Orchestrator ↔ MSP | high | P2-007, P1-007 | 60 |
| P2-009 | Wire Orchestrator ↔ Bus | high | P2-007 | 40 |
| P2-010 | Orchestrator integration tests | medium | P2-008,009 | 120 |

### Success Criteria
- [ ] User message → Orchestrator → LLM → Response
- [ ] Context includes memory from MSP
- [ ] State changes published to Bus
- [ ] Integration test passes

---

## Phase 3: Psychology

> **Goal:** EVA มีอารมณ์ที่ส่งผลต่อ response
> **Dependencies:** Phase 2
> **Deliverables:** EVA Matrix, 9D Emotions, Stress System

### Architecture

```
eva_matrix/
├── __init__.py
├── matrix_engine.py         # Core psychology engine
├── dimensions/
│   ├── __init__.py
│   ├── pleasure.py          # Pleasure-Pain axis
│   ├── arousal.py           # Calm-Excited axis
│   ├── dominance.py         # Submissive-Dominant axis
│   └── ... (6 more)
├── stress/
│   ├── __init__.py
│   └── stress_tracker.py
├── schema/
│   └── matrix_state.py
└── tests/
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P3-001 | Create EVA Matrix directory | high | P2 | 10 |
| P3-002 | Define MatrixState schema | high | P3-001 | 80 |
| P3-003 | Implement 9D dimensions | high | P3-002 | 200 |
| P3-004 | Implement StressTracker | medium | P3-002 | 80 |
| P3-005 | Create Matrix Engine | high | P3-003,004 | 150 |
| P3-006 | Implement MatrixProvider (IStateProvider) | high | P3-005 | 60 |
| P3-007 | Wire Matrix ↔ Bus | high | P3-006 | 40 |
| P3-008 | Matrix unit tests | medium | P3-007 | 100 |

### Success Criteria
- [ ] Matrix tracks 9 emotion dimensions
- [ ] Stress affects emotion state
- [ ] Matrix publishes to `bus:psychological`
- [ ] Orchestrator receives Matrix state

---

## Phase 4: Biology

> **Goal:** ฮอร์โมนส่งผลต่ออารมณ์และพฤติกรรม
> **Dependencies:** Phase 3
> **Deliverables:** PhysioCore, Endocrine System, Vitals

### Architecture

```
physio_core/
├── __init__.py
├── physio_engine.py         # Core biology engine
├── endocrine/
│   ├── __init__.py
│   ├── glands.py            # 12 hormone glands
│   ├── hormones.py          # Hormone definitions
│   └── cascade.py           # Hormone interactions
├── blood/
│   ├── __init__.py
│   └── circulation.py       # 30Hz hormone distribution
├── vitals/
│   ├── __init__.py
│   └── vital_signs.py       # HR, BR, Temp
├── receptor/
│   ├── __init__.py
│   └── receptor_system.py   # Signal transduction
├── schema/
│   └── physio_state.py
└── tests/
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P4-001 | Create PhysioCore directory | high | P3 | 10 |
| P4-002 | Define PhysioState schema | high | P4-001 | 100 |
| P4-003 | Implement Hormone definitions | high | P4-002 | 150 |
| P4-004 | Implement Glands (12 types) | high | P4-003 | 200 |
| P4-005 | Implement Cascade system | medium | P4-004 | 120 |
| P4-006 | Implement Blood circulation | medium | P4-005 | 100 |
| P4-007 | Implement Vital signs | medium | P4-006 | 80 |
| P4-008 | Implement Receptor system | medium | P4-007 | 100 |
| P4-009 | Create Physio Engine | high | P4-008 | 180 |
| P4-010 | Wire Physio ↔ Matrix ↔ Bus | high | P4-009, P3-007 | 60 |

### Success Criteria
- [ ] 12 hormone types functional
- [ ] Hormones affect Matrix state
- [ ] Blood circulation at 30Hz
- [ ] Vitals respond to hormone levels
- [ ] Publishes to `bus:physical`

---

## Phase 5: Perception

> **Goal:** Sensory experience และ Qualia encoding
> **Dependencies:** Phase 4
> **Deliverables:** RMS, Qualia System, Sensory Memory

### Architecture

```
perception/
├── rms/                     # Resonance Memory System
│   ├── __init__.py
│   ├── rms_engine.py
│   └── resonance_encoder.py # Real encoder (not mock)
├── qualia/
│   ├── __init__.py
│   ├── qualia_engine.py
│   ├── texture.py           # Texture qualities
│   ├── color.py             # Color qualities
│   └── soundscape.py        # Sound qualities
├── schema/
│   └── qualia_state.py
└── tests/
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P5-001 | Create Perception directory | high | P4 | 10 |
| P5-002 | Define QualiaState schema | high | P5-001 | 80 |
| P5-003 | Implement Texture qualities | medium | P5-002 | 60 |
| P5-004 | Implement Color qualities | medium | P5-002 | 60 |
| P5-005 | Implement Soundscape qualities | medium | P5-002 | 60 |
| P5-006 | Create Qualia Engine | high | P5-003,004,005 | 120 |
| P5-007 | Create RMS Engine (real encoder) | high | P5-006 | 150 |
| P5-008 | Wire Qualia ↔ Bus | high | P5-007 | 40 |

### Success Criteria
- [ ] Qualia encodes sensory experience
- [ ] RMS calculates resonance scores (L1-L5)
- [ ] Publishes to `bus:phenomenological`
- [ ] Memories have sensory attachments

---

## Phase 6: Knowledge

> **Goal:** Innate knowledge accessible ให้ LLM
> **Dependencies:** Phase 5
> **Deliverables:** GKS, 7 Master Blocks

### Architecture

```
gks/                         # Genesis Knowledge System
├── __init__.py
├── gks_engine.py
├── blocks/
│   ├── master_block.json
│   ├── algorithm_how.json
│   ├── concept_why.json
│   ├── framework.json
│   ├── parameter_what.json
│   ├── protocol_process.json
│   └── safety.json
├── loader/
│   └── block_loader.py
└── tests/
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P6-001 | Create GKS directory | high | P5 | 10 |
| P6-002 | Define Block schemas | high | P6-001 | 100 |
| P6-003 | Create 7 Master Blocks (JSON) | high | P6-002 | 300 |
| P6-004 | Implement BlockLoader | high | P6-003 | 80 |
| P6-005 | Create GKS Engine | high | P6-004 | 120 |
| P6-006 | Wire GKS ↔ CIM | high | P6-005, P2-005 | 60 |

### Success Criteria
- [ ] 7 Master Blocks loaded
- [ ] GKS retrieves relevant knowledge
- [ ] CIM can inject GKS context
- [ ] Safety block enforced

---

## Phase 7: Integration

> **Goal:** Production-ready system
> **Dependencies:** All phases
> **Deliverables:** API, Full Integration, Performance

### Architecture

```
api/
├── __init__.py
├── main.py                  # FastAPI app
├── routes/
│   ├── chat.py              # Chat endpoint
│   ├── state.py             # State inspection
│   └── memory.py            # Memory operations
└── middleware/
    └── auth.py

consciousness/               # Runtime state
├── context_container/       # Active turn files
├── episodic_memory/         # Conversation logs
├── state_memory/            # Current snapshots
└── indexes/                 # Fast lookups

memory/                      # Persistent storage
├── session_memory/
├── core_memory/
├── sphere_memory/
└── user_registry.json
```

### Tasks

| ID | Task | Priority | Depends On | Est. Lines |
|----|------|----------|------------|------------|
| P7-001 | Create API directory | high | P6 | 10 |
| P7-002 | Implement Chat endpoint | high | P7-001 | 100 |
| P7-003 | Implement State endpoint | medium | P7-002 | 60 |
| P7-004 | Implement Memory endpoint | medium | P7-002 | 80 |
| P7-005 | Full system integration | high | P7-004 | 200 |
| P7-006 | Consciousness/Memory setup | high | P7-005 | 100 |
| P7-007 | Integration tests (E2E) | high | P7-006 | 150 |
| P7-008 | Performance optimization | medium | P7-007 | 100 |

### Success Criteria
- [ ] API accepts chat requests
- [ ] Full cognitive flow works
- [ ] Bio-Digital Gap functional
- [ ] Memory persists across sessions
- [ ] Response time < 2s (local LLM)

---

## Dependency Graph

```
Phase 0 (Foundation)
    │
    ▼
Phase 1 (MSP) ─────────────────────┐
    │                              │
    ▼                              │
Phase 2 (Orchestration) ◄──────────┤
    │                              │
    ▼                              │
Phase 3 (Psychology) ◄─────────────┤
    │                              │
    ▼                              │
Phase 4 (Biology) ◄────────────────┤
    │                              │
    ▼                              │
Phase 5 (Perception) ◄─────────────┤
    │                              │
    ▼                              │
Phase 6 (Knowledge) ◄──────────────┘
    │
    ▼
Phase 7 (Integration)
    │
    ▼
  v1.0.0
```

---

## Version Milestones

| Version | Phase | Key Feature |
|---------|-------|-------------|
| 0.1.0 | 0 | Foundation complete |
| 0.2.0 | 1 | Memory works |
| 0.3.0 | 2 | Basic chat works |
| 0.4.0 | 3 | Emotions affect responses |
| 0.5.0 | 4 | Biology drives emotions |
| 0.6.0 | 5 | Sensory experience |
| 0.7.0 | 6 | Knowledge accessible |
| 1.0.0 | 7 | Production ready |

---

## Agent Instructions

### How to Pick a Task

1. Check `.planning/STATE.md` for current phase
2. Find tasks in `.planning/tasks/P{phase}-*.yaml`
3. Pick task with `status: pending` and no blockers
4. Check `depends_on:` are all `done`

### How to Complete a Task

1. Read full task YAML
2. Follow `spec:` exactly
3. Verify `acceptance_criteria:`
4. Update task `status: done`
5. Report completion

### Parallel Work

Tasks in same "wave" can be done in parallel:

**Phase 1 Waves:**
- Wave 1: P1-001 (no deps)
- Wave 2: P1-002, P1-003, P1-004 (after P1-001)
- Wave 3: P1-005 (after schemas)
- Wave 4: P1-006, P1-007 (after P1-005)
- Wave 5: P1-008 (after all)

---

## Notes

- ทุก task ควร < 200 lines of code
- Mock adapters ต้องทำงานได้ก่อน real implementations
- Test ทุก module ก่อน integrate
- Schema-first: define contracts before code
