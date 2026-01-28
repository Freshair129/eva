---
trigger: always_on
---

# .agent/rules — Constitutional Documents

> **Purpose:** Immutable principles governing EVA Genesis
> **Status:** Foundation (v0.1.0)

---

## Rule Hierarchy

### Tier 1: Foundation (IMMUTABLE)

| Document | Description |
|----------|-------------|
| `constitution.md` | The 5 Pillars of EVA |

### Tier 2: Architecture (STABLE)

| Document | Description |
|----------|-------------|
| `phaserules.md` | Phase-specific relaxations |
| `codingstandards.md` | Code quality rules |

### Tier 3: Operational (EVOLVING)

| Document | Description |
|----------|-------------|
| `glossary.md` | Term definitions |
| `versioning.md` | Version control enforcement |
| `backlog.md` | Future task tracking |

---

## Rule Status Legend

| Icon | Status | Update Policy |
|------|--------|---------------|
| 🔒 | IMMUTABLE | Requires ADR + major version bump |
| 🟡 | STABLE | Requires ADR + minor version bump |
| 🟢 | EVOLVING | Standard review process |

---

## Important Note

During **Phase 0-2**, some Constitution pillars are **relaxed** because the required systems don't exist yet. See `phase_rules.md` for details.
