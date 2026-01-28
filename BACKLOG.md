# EVA Genesis Backlog

> **Purpose:** Tracking future ideas, optimizations, and delayed tasks.
> **Status:** Active

---

## 📌 High Priority (Next in Line)

- [x] **P1-004: Sensory Memory Schema** - Define structure for raw perceptual data (visual patterns, audio snippets, qualia).
- [x] **P1-005: MemoryStore Implementation** - Create the core logic for saving/loading File-per-Record structure.
- [ ] **P1-006: ChromaDB Bridge** - Integrate vector database for semantic retrieval of episodes/turns.
- [ ] **P1-007: MSP Engine Integration** - Orchestrate all memory types into a single service.

---

## 💡 Future Ideas

- [ ] **Image Analysis Support** - Extend Sensory Memory to handle metadata from generated images.
- [ ] **Recall Optimization** - Implement a caching layer for recently accessed turns to further reduce I/O.
- [ ] **Memory Tiering (8-8-8)** - Implementation of the 8-8-8 compression protocol (Phase 7 target).
- [ ] **Cross-Memory Linking** - Automatic linking between Episodic summaries and Semantic facts.

---

## 🛠 Refactoring & Technical Debt

- [ ] **Index System** - Decide between a simple `index.json` or a lightweight SQLite DB for the File-per-Record index.
- [ ] **Validation Layer** - Implement JSON Schema validation for all new MSP v0.0.8+ files.

---

*To add an item: Ask Antigravity to "add to backlog".*
