# EVA Project

> **Version:** 0.1.0 (Genesis)
> **Start Date:** 2026-01-27
> **Approach:** Walking Skeleton / Incremental Integration
> **Lead Dev:** Claude Opus 4.5

---

## Vision

EVA (Embodied Virtual Agent) - Bio-inspired AI architecture implementing "Resonance Intelligence" framework.

**Philosophy:** Embodied Existentialism - AI that "feels" through simulated biological processes.

---

## Architecture Principles

1. **Flat Anatomy** - Systems at root level, not nested in `systems/` folder
2. **Registry-Centric** - `master_registry.yaml` as Single Source of Truth
3. **Dependency Inversion** - Interfaces (Ports) over concrete implementations
4. **Walking Skeleton** - Build minimal working system, add features incrementally

---

## Phase Roadmap

| Phase | Name | Description | Status |
|-------|------|-------------|--------|
| 0 | Foundation | Project setup, contracts, infrastructure | ✅ Done |
| 1 | MSP Core | Memory system standalone | 🔄 Current |

| 2 | Orchestration | Basic routing, LLM bridge | ⏳ Pending |
| 3 | Psychology | EVA Matrix (emotions) | ⏳ Pending |
| 4 | Biology | PhysioCore (hormones) | ⏳ Pending |
| 5 | Perception | RMS, Qualia | ⏳ Pending |
| 6 | Knowledge | GKS (Genesis blocks) | ⏳ Pending |
| 7 | Integration | Full system, API | ⏳ Pending |

---

## Directory Structure (Target)

```
eva/
├── CLAUDE.md              # AI assistant instructions
├── VERSION                 # Current version
├── CHANGELOG.md           # Version history
│
├── .planning/             # Planning & task management
│   ├── tasks/             # Task definitions for agents
│   ├── specs/             # Technical specifications
│   └── STATE.md           # Current project state
│
├── contracts/             # Interface definitions (Ports)
│   ├── ports/             # External system interfaces
│   └── schemas/           # Data schemas
│
├── adapters/              # Interface implementations
│   ├── mocks/             # Mock adapters for testing
│   └── real/              # Production adapters
│
├── msp/                   # Memory & Soul Passport
├── orchestrator/          # Central Nervous System
├── eva_matrix/            # Psychology system
├── physio_core/           # Biology system
├── rms/                   # Resonance Memory System
├── qualia/                # Phenomenology system
├── gks/                   # Genesis Knowledge System
│
├── consciousness/         # Runtime state (RAM)
├── memory/                # Persistent storage
├── config/                # Centralized configuration
├── tests/                 # All tests
└── docs/                  # Documentation
```

---

## Task Workflow

1. **Lead Dev (Claude)** creates task specs in `.planning/tasks/`
2. **Agents (Antigravity)** pick up and execute tasks
3. **Lead Dev** reviews and integrates
4. **Repeat** until phase complete

---

## Current Focus

**Phase 0: Foundation [COMPLETED]**
- [x] Create base structure
- [x] Define core contracts
- [x] Setup testing framework
- [x] Create mock adapters

**Phase 1: MSP Core [IN PROGRESS]**
- [x] Create MSP Directory Structure (P1-001)
- [x] Define EpisodicMemory Schema (P1-002)
- [ ] Define Semantic & Sensory Schemas
- [ ] Implement MSP Engine
- [ ] Connect to SimpleBus
- [ ] Integrate ChromaDB vector bridge


