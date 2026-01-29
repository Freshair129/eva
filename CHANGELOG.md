# Changelog

All notable changes to EVA will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Phase 5: Perception
- **RMS v0.1.0**: Resonance Memory System
- **Resonance Encoder**: Wraps E9 Protocol for state compression
- **Qualia Engine**: Generates subjective sensory experience (Narrative, Texture, Temperature)
- **PhenomProvider**: Bus integration for phenomenological state (`bus:phenomenological`)

### Phase 4: Biology
- **PhysioCore v0.1.0**: Biological Subsystem
- **Hormone System**: 12 key hormones (Dopamine, Cortisol, etc.) with decay logic
- **Circulatory System**: 30Hz Simulation Loop & Heartbeat
- **Bio-Digital Gap**: Dynamic latency based on physiological state
- **PhysioProvider**: Bus integration for biological signals (`bus:physical`)

### Phase 3: Psychology
- **E9 Resonance Codec**: State compression (10 fields: RI + 9 psychological variables)
- **EVA Matrix v0.1.0**: 5+2+2 emotional model with state persistence
- **Capabilities System v0.1.0**: 23 tools across 4 tiers
  - Core: time, memory, state (7 tools)
  - File System: read, write, list (5 tools)
  - Utility: calculator, dice (4 tools)
  - Agentic: web_search, run_python, plan_task (7 tools)
- **Web Search Integration**: DuckDuckGo (free) + Serper.dev support

### Phase 0: Foundation
- Project structure setup
- Core contracts definition
- Mock adapters
- Testing framework

---

## [0.1.0] - 2026-01-27

### Added
- Initial project structure
- PROJECT.md with roadmap
- Planning directory structure
- Task workflow for agent collaboration
- **Foundation Layer (Phase 0) [Implemented by Antigravity]**
    - Core Ports: `IStateProvider`, `IResonanceEncoder`, `IBus`, `IMemoryStorage`
    - Mock Adapters: `MockPhysioProvider`, `MockMatrixProvider`, `MockResonanceEncoder`
    - Infrastructure: `SimpleBus` (in-memory pub/sub)
    - Configuration: `master_registry.yaml` (SSOT)
    - Testing: `pytest` framework with fixtures and unit tests
    - **Decision Log** (P0-011): Central repository for tracking architectural and persona conclusions.

### Changed
- **MSP Layer (Phase 1) [Implemented by Antigravity]**
    - Established MSP directory structure (`msp/`, `msp/schema/`, `msp/storage/`, `msp/tests/`) (P1-001)
    - **MSP Schema Evolution (v0.0.1 → v0.4.1) [Implemented by Antigravity]**
        - `Episodic`, `Semantic`, `Sensory` Schemas Complete
        - **Crosslink Manager** (v0.4.1): Automated bidirectional linking between memory types
        - **Phase 1.1 Complete**: All core memory features implemented and integrated.
        - **MSPEngine Integration** (v0.4.0): Unified storage orchestration & hydrated search
        - **ChromaDB Support** (v0.3.0): Integrated vector search for semantic retrieval
        - See: [msp/VERSION_HISTORY.md](msp/VERSION_HISTORY.md) for full changelog
- **Orchestration Layer (Phase 2) [Implemented by Antigravity]**
    - Established Orchestrator directory structure (`orchestrator/`, `orchestrator/cim/`, `orchestrator/llm_bridge/`) (P2-001)
    - **LLM Bridge** (v0.1.0): Support for MockLLM and local Ollama inference (P2-002, P2-003, P2-004)
    - **CIM Engine** (v0.1.0): Context Injection Manager for gathering MSP and Bus context (P2-005, P2-006)
    - **Orchestrator Engine** (v0.1.0): Central Nervous System coordinating the cognitive loop (P2-007)
    - **MSP & Bus Integration**: Automated memory persistence and event publishing (P2-008, P2-009)
    - See: [orchestrator/VERSION_HISTORY.md](orchestrator/VERSION_HISTORY.md) and [orchestrator/cim/VERSION_HISTORY.md](orchestrator/cim/VERSION_HISTORY.md) for details.


### Architecture Decisions
- Walking Skeleton approach
- Dependency Inversion via Ports/Adapters
- Flat anatomy (no nested `systems/` folder)
- Registry-centric configuration

