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
    - **MSP Schema Evolution (v0.0.1 → v0.1.0) [Implemented by Antigravity]**
        - `EpisodicMemory` (P1-002), `SemanticMemory` (P1-003), `SensoryMemory` (P1-004)
        - V2 Alignment: Nested Turns, Enhanced Context, Structured Summary
        - Qualia & Physio Snapshots: Captured in Sensory Memory
        - **File-per-Record Architecture** (v0.0.8): Standalone `turn.py` & referenced episodes
        - **MSP Master Specification** (v0.0.9): Added [msp/README.md](msp/README.md) guide
        - See: [msp/VERSION_HISTORY.md](msp/VERSION_HISTORY.md) for full changelog


### Architecture Decisions
- Walking Skeleton approach
- Dependency Inversion via Ports/Adapters
- Flat anatomy (no nested `systems/` folder)
- Registry-centric configuration

