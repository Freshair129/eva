# ADR-006: Module-level Versioning & Enforcement

> **Status:** Accepted
> **Date:** 2026-01-28
> **Deciders:** Antigravity

---

## Context

As the EVA project grows, multiple independent systems (MSP, Orchestrator, Matrix) are developed in parallel. Tracking changes across the entire repo via a single version number (e.g., `0.1.0`) is insufficient because:
1. **Schema Evolution**: Different modules change their data formats at different rates.
2. **Traceability**: Hard for the user (or the AI) to know if a specific bug fix or feature is included in a specific module.
3. **Consistency**: Manual documentation of changes is prone to being forgotten during fast-paced development.

---

## Decision

Implement a **Semantic Versioning (SemVer)** system at the **Module Level** with automatic enforcement rules.

1. **Module Versions**: Every major system (e.g., `msp/`) must have its own `__version__` in `__init__.py`.
2. **Local History**: Every module must maintain a `VERSION_HISTORY.md` file documenting changes for that specific scope.
3. **Automated Rule**: A Tier-3 Agent Rule (`.agent/rules/versioning.md`) mandates that the AI agent MUST bump the version and update the history whenever a module is modified.
4. **Git Integration**: Version increments must be synchronized with the remote repository (Commit & Push) as part of the atomic update.

---

## Consequences

### Positive
- **Clear Traceability**: Every module's state is explicitly labeled.
- **Improved Alignment**: AI can check `__version__` to know which schema/protocol to use.
- **Standardized Process**: Prevents "knowledge drift" where changes happen but are undocumented.

### Negative
- **Minor Overhead**: Every code change requires updating 2-3 extra internal documentation files.
- **Commit Noise**: More meta-commits for versioning (mitigated by grouping).

---

## Alternatives Considered

### Option 1: Global Repository Versioning
- Only update `CHANGELOG.md` at the root.
- **Reason Rejected**: Too coarse-grained for a modular architecture like EVA.

### Option 2: Manual Versioning
- Only version when the user asks.
- **Reason Rejected**: Human error (forgetting) is highly likely in agentic development.

---

## References

- [Versioning Rule](file:///e:/eva/.agent/rules/versioning.md)
- [Versioning Workflow](file:///e:/eva/.agent/workflows/version-bump.md)
- [MSP VERSION_HISTORY.md](file:///e:/eva/msp/VERSION_HISTORY.md)
