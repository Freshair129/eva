# ADR-002: Flat Anatomy Structure

> **Status:** Accepted
> **Date:** 2026-01-27
> **Deciders:** Lead Dev, Project Owner, LLM Consensus (Opus, Sonnet, Gemini)

---

## Context

During EVA v9.x development, there was debate about directory structure:

**Option A: Nested (Semantic Grouping)**
```
eva/
├── systems/
│   ├── physio_core/
│   ├── eva_matrix/
│   └── msp/
├── infrastructure/
│   ├── bus/
│   └── identity/
└── ...
```

**Option B: Flat (Organism Anatomy)**
```
eva/
├── physio_core/
├── eva_matrix/
├── msp/
├── orchestrator/
└── ...
```

A formal debate was conducted with 5 LLM models (documented in `LLM Structure Debate.md`).

---

## Decision

Adopt **Flat Anatomy** structure.

**Final Structure:**
```
eva/
├── contracts/           # Interfaces (Ports)
├── adapters/            # Implementations
├── msp/                 # Memory system
├── orchestrator/        # CNS
├── eva_matrix/          # Psychology
├── physio_core/         # Biology
├── rms/                 # Resonance
├── qualia/              # Phenomenology
├── gks/                 # Knowledge
├── consciousness/       # Runtime state
├── memory/              # Persistent storage
├── config/              # Configuration
├── tests/               # All tests
└── docs/                # Documentation
```

**Key Principle:**
> "Keep the Organs Flat. Enforce the Whitelist. Trust the Registry."

---

## Rationale

### 1. Embodied Organism Metaphor

EVA is designed as a "digital organism." The directory structure should reflect anatomy:

```
Human Body          EVA Project
───────────         ───────────
Heart        →      physio_core/
Brain        →      orchestrator/
Memory       →      msp/
Emotions     →      eva_matrix/
```

Organs are not stored in boxes labeled "organ_systems/". They exist as first-class parts of the body.

### 2. Token Economy (AI Agent Efficiency)

Shorter paths = fewer tokens in LLM context:

```python
# Nested (more tokens)
from systems.biological.physio_core.physio_core import PhysioCore

# Flat (fewer tokens)
from physio_core.physio_core import PhysioCore
```

For AI agents working on the codebase, this matters.

### 3. Discoverability

```bash
# Flat: One command shows all systems
ls eva/
# → msp/ orchestrator/ eva_matrix/ physio_core/ ...

# Nested: Must drill down
ls eva/systems/
# → biological/ psychological/ ...
ls eva/systems/biological/
# → physio_core/
```

### 4. Registry-Centric Organization

Logical grouping is handled by `config/master_registry.yaml`, not folder structure:

```yaml
systems:
  - id: PhysioCore
    type: organ
    domain: biological

  - id: EVAMatrix
    type: organ
    domain: psychological
```

Physical location stays flat. Logical type is in registry.

---

## Consequences

### Positive

1. **Immediate Visibility:** All systems visible at root
2. **Shorter Imports:** Less typing, fewer tokens
3. **Philosophy Aligned:** Matches "embodied organism" concept
4. **Registry Authority:** Single source of truth for organization
5. **LLM Debate Consensus:** 5 out of 6 models agreed

### Negative

1. **More Root Items:** ~15 folders at root level
2. **Requires Discipline:** Must not pollute root with random files
3. **Pre-commit Hook Needed:** To enforce whitelist

### Mitigation

```yaml
# .agent/governance/root_policy.yaml
allowed_root_dirs:
  - contracts
  - adapters
  - msp
  - orchestrator
  - eva_matrix
  - physio_core
  - ... (from registry)

enforcement:
  pre_commit_hook: true
```

---

## Alternatives Considered

### 1. Semantic Grouping (`systems/`, `infrastructure/`)
- Proposed by: GPT-4
- Rejected by: 5 other models
- Reason: Breaks organism metaphor, longer paths

### 2. Domain-Driven Design (Bounded Contexts)
- Considered but deemed over-engineering for current scale
- May revisit at v2.0.0

---

## References

- `LLM Structure Debate.md` - Full debate transcript
- Kubernetes project structure (flat)
- Linux kernel structure (flat domains)
