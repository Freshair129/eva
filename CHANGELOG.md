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
    - **MSP Schema Evolution (v0.0.1 → v0.0.8) [Implemented by Antigravity]**
        - `EpisodicMemory` (P1-002): Initial schema with content, summary, tags
        - `SemanticMemory` (P1-003): SPO structure for knowledge graphs
        - V2 Alignment: Nested `TurnUser`, `TurnLLM`, `SituationContext`
        - Enhanced Context: `location_context`, `domain_area`, `mission_goal`, `agent_role`
        - `StructuredSummary`: action_taken, key_outcome, future_implication
        - **File-per-Record Architecture** (v0.0.8):
            - Created `turn.py` with standalone Turn classes
            - Episodes now use `turn_refs` (references only)
            - Added `get_file_path()` for consistent storage paths
        - See: [msp/VERSION_HISTORY.md](msp/VERSION_HISTORY.md) for full changelog


### Architecture Decisions
- Walking Skeleton approach
- Dependency Inversion via Ports/Adapters
- Flat anatomy (no nested `systems/` folder)
- Registry-centric configuration

