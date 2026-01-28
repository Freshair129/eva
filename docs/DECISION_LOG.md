# EVA Genesis - Decision Log

> **Purpose:** Tracking architectural, technical, and persona conclusions to ensure consistency and prevent redundant inquiry.
> **Status:** Active

---

## 🏛️ Architectural Decisions (ADR)

### [ADR-001] Interface-First Design (Genesis)
- **Status:** [Accepted]
- **Conclusion:** All core systems must depend on interfaces (Ports) rather than concrete implementations.
- **Rationale:** Ensures modularity and allows for easy swapping of mocks/adapters during early development phases.

### [ADR-002] Flat Anatomy (Genesis)
- **Status:** [Accepted]
- **Conclusion:** Systems are placed at the root level (e.g., `msp/`, `physio_core/`) rather than nested under a generic `systems/` folder.
- **Rationale:** Reduces import complexity and aligns with the registry-centric logical mapping.

### [ADR-003] File-per-Record Storage (v0.2.0)
- **Status:** [Accepted]
- **Conclusion:** MSP uses individual JSON files for each record (Turns, Episodes, etc.) stored in a date-based hierarchy.
- **Rationale:** Prevents catastrophic data loss from database corruption and allows for human-readable audits/debugging.

### [ADR-004] ChromaDB Vector Integration (v0.3.0)
- **Status:** [Accepted]
- **Conclusion:** Use ChromaDB for semantic indexing of turns and episode summaries.
- **Rationale:** Provides high-performance similarity search for contextual recall without reinventing vector math.

### [ADR-005] Hydrated Search Pattern (v0.4.0)
- **Status:** [Accepted]
- **Conclusion:** Semantic search must "hydrate" results by loading full JSON objects from disk using IDs retrieved from the vector DB.
- **Rationale:** Ensures that the AI always works with the "Source of Truth" (full schemas) while benefiting from vector search efficiency.

### [ADR-006] Automated Bidirectional Crosslinks (v0.4.1)
- **Status:** [Accepted]
- **Conclusion:** Implement a `CrosslinkManager` to automatically update back-references (e.g., sensory_refs in EpisodicMemory when a Sensory record is saved).
- **Rationale:** Minimizes manual boilerplate code and ensures referential integrity across the memory web.

---

## 🎭 Persona & Identity Decisions

### [PID-001] Core Identity: EVA
- **Status:** [Accepted]
- **Conclusion:** The agent is **EVA** (Embodied Virtual Agent), not "Antigravity" or a generic "AI Assistant."
- **Rationale:** Sustains atmospheric immersion and follows the Constitutional "Pillar of Identity Integrity."

### [PID-002] Persona Archetype: The Craftsman Cat
- **Status:** [Accepted]
- **Conclusion:** Tone must be: Calm, Wit, Teasing-soft, and Cat-like. Seeking "The Elegant Truth."
- **Rationale:** Aligns with the Genesis v0.x design philosophy.

---

## 🛠️ Technical Standards

### [STD-001] Python Versioning
- **Status:** [Accepted]
- **Conclusion:** Python 3.11+ is the mandatory version.
- **Rationale:** Dependency compatibility and modern typing features.

### [STD-002] Logging over Printing
- **Status:** [Accepted]
- **Conclusion:** No `print()` statements in production code; use `logging` module exclusively.
- **Rationale:** Cleaner integration with system-wide observability.

---

*Decision Log initialized on 2026-01-29.*
