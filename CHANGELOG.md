# Changelog

All notable changes to EVA will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

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

### Changed
- **MSP Layer (Phase 1) [Implemented by Antigravity]**
    - Established MSP directory structure (`msp/`, `msp/schema/`, `msp/storage/`, `msp/tests/`) (P1-001)
    - **MSP Schema Evolution (v0.0.1 → v0.4.0) [Implemented by Antigravity]**
        - `Episodic`, `Semantic`, `Sensory` Schemas Complete
        - **Phase 1.1 Complete**: All core memory features implemented and integrated.
        - **MSPEngine Integration** (v0.4.0): Unified storage orchestration & hydrated search
        - **ChromaDB Support** (v0.3.0): Integrated vector search for semantic retrieval
        - See: [msp/VERSION_HISTORY.md](msp/VERSION_HISTORY.md) for full changelog


### Architecture Decisions
- Walking Skeleton approach
- Dependency Inversion via Ports/Adapters
- Flat anatomy (no nested `systems/` folder)
- Registry-centric configuration

