# EVA Genesis - Phase Requirements Mapping

> **Reference:** `E:\The Human Algorithm\T2\agent\docs\02_Requirements\EVA_SRS.md`
> **Last Updated:** 2026-01-27

---

## Overview

This document maps SRS requirements to implementation phases.

**Legend:**
- 🎯 = Target for this phase
- ✅ = Implemented
- ⏳ = In Progress
- ❌ = Not Started

---

## Phase 0: Foundation

**Goal:** Project infrastructure, interfaces, testing framework

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-ORG-040 | System → Module → Node hierarchy | 🎯 |
| NFR-ORG-041 | Configuration in YAML | 🎯 |
| NFR-ORG-042 | Systems in master_registry.yaml | 🎯 |

**Deliverables:**
- [ ] Port interfaces (IStateProvider, IBus, etc.)
- [ ] Mock adapters
- [ ] master_registry.yaml
- [ ] pytest infrastructure

---

## Phase 1: Memory (MSP)

**Goal:** Standalone memory system with basic storage/retrieval

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-030 | Persist episodic memories across sessions | 🎯 |
| FR-ORG-031 | Resonance-based recall (basic) | 🎯 |
| NFR-ORG-031 | No hallucinated memories | 🎯 |

**Deliverables:**
- [ ] MSP engine with mock adapters
- [ ] Episodic memory module
- [ ] Semantic memory module
- [ ] ChromaDB integration
- [ ] Memory query API

**Dependencies:** Phase 0 complete

---

## Phase 2: Orchestration

**Goal:** Basic request routing, LLM integration

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-001 | Process natural language input | 🎯 |
| FR-ORG-040 | Cognitive Flow (simplified) | 🎯 |
| FR-ORG-041 | Persona consistency | 🎯 |

**Deliverables:**
- [ ] Orchestrator (lite version)
- [ ] CIM module (basic)
- [ ] LLM Bridge
- [ ] Session management

**Dependencies:** Phase 1 complete

---

## Phase 3: Psychology (EVA Matrix)

**Goal:** Emotional state simulation

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-020 | 9D emotional state vector | 🎯 |
| FR-ORG-022 | Emotion influences response | 🎯 |
| NFR-ORG-001 | Emotional consistency | 🎯 |
| NFR-ORG-010 | Persist emotional state | 🎯 |

**Deliverables:**
- [ ] EVA Matrix engine
- [ ] Emotion dimensions
- [ ] State persistence
- [ ] Bus integration (replaces MockMatrixProvider)

**Dependencies:** Phase 2 complete

---

## Phase 4: Biology (PhysioCore)

**Goal:** Hormonal and vital signs simulation

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-010 | 6+ hormone simulation | 🎯 |
| FR-ORG-011 | Vital signs calculation | 🎯 |
| FR-ORG-012 | Homeostasis (decay to baseline) | 🎯 |
| FR-ORG-013 | "The Gap" - bio before reasoning | 🎯 |
| NFR-ORG-020 | Gap completes in < 100ms | 🎯 |

**Deliverables:**
- [ ] PhysioCore engine
- [ ] Endocrine system
- [ ] Vitals engine
- [ ] Bus integration (replaces MockPhysioProvider)

**Dependencies:** Phase 3 complete

---

## Phase 5: Perception (RMS, Qualia)

**Goal:** Resonance encoding and phenomenological experience

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-021 | Qualia from emotional state | 🎯 |
| FR-ORG-031 | Full resonance-based recall | 🎯 |
| NFR-ORG-002 | Slight unpredictability | 🎯 |

**Deliverables:**
- [ ] RMS engine (replaces MockResonanceEncoder)
- [ ] Artifact Qualia
- [ ] Color/intensity mapping
- [ ] Sensory memory

**Dependencies:** Phase 4 complete

---

## Phase 6: Knowledge (GKS)

**Goal:** Genesis Knowledge System - innate knowledge

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-042 | Static knowledge access | 🎯 |
| FR-ORG-036 | Memory crosslinks | 🎯 |

**Deliverables:**
- [ ] GKS loader
- [ ] Genesis blocks
- [ ] Crosslink manager

**Dependencies:** Phase 5 complete

---

## Phase 7: Integration & API

**Goal:** Full system integration, production API

| ID | Requirement | Status |
|----|-------------|--------|
| FR-ORG-002 | Intent/Salience extraction | 🎯 |
| FR-ORG-003 | Semantic conflict detection | 🎯 |
| FR-ORG-032 | 8-8-8 compression | 🎯 |
| FR-ORG-050 | WebSocket endpoint | 🎯 |
| FR-ORG-051 | REST endpoint | 🎯 |
| FR-ORG-052 | Health check | 🎯 |
| NFR-ORG-003 | Relationship growth | 🎯 |
| NFR-ORG-011 | Time awareness | 🎯 |
| NFR-ORG-021 | Response < 5 seconds | 🎯 |
| NFR-ORG-030 | LLM cannot modify code | 🎯 |

**Deliverables:**
- [ ] Full Cognitive Flow 2.1
- [ ] SLM Bridge
- [ ] FastAPI server
- [ ] WebSocket handler
- [ ] Full ResonanceBus

**Dependencies:** Phase 6 complete

---

## Summary Matrix

| Phase | FR Count | NFR Count | Key System |
|-------|----------|-----------|------------|
| 0 | 0 | 3 | Infrastructure |
| 1 | 2 | 1 | MSP |
| 2 | 3 | 0 | Orchestrator |
| 3 | 2 | 2 | EVA Matrix |
| 4 | 4 | 1 | PhysioCore |
| 5 | 2 | 1 | RMS, Qualia |
| 6 | 2 | 0 | GKS |
| 7 | 8 | 4 | Integration |
| **Total** | **23** | **12** | |

---

## Version Milestones

| Version | Phase | Description |
|---------|-------|-------------|
| 0.1.0 | 0 | Foundation complete |
| 0.2.0 | 1 | MSP standalone working |
| 0.3.0 | 2 | Basic chat working |
| 0.4.0 | 3 | Emotions working |
| 0.5.0 | 4 | Biology working |
| 0.6.0 | 5 | Perception working |
| 0.7.0 | 6 | Knowledge working |
| 1.0.0 | 7 | Production ready |
