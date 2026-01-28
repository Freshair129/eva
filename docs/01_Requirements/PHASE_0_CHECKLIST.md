# Phase 0 Checklist: Foundation

> **Target Version:** 0.1.0
> **Status:** In Progress

---

## Requirements (from SRS)

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-ORG-040 | System → Module → Node hierarchy | ⏳ |
| NFR-ORG-041 | Configuration in YAML | ⏳ |
| NFR-ORG-042 | Systems in master_registry.yaml | ⏳ |

---

## Deliverables Checklist

### Contracts (Interfaces)

- [ ] `contracts/ports/i_state_provider.py`
- [ ] `contracts/ports/i_resonance_encoder.py`
- [ ] `contracts/ports/i_bus.py`
- [ ] `contracts/ports/i_memory_storage.py`

### Adapters (Implementations)

- [ ] `adapters/mocks/mock_state_providers.py`
- [ ] `adapters/mocks/mock_resonance_encoder.py`
- [ ] `adapters/simple_bus.py`

### Configuration

- [ ] `config/master_registry.yaml`

### Testing

- [ ] `pytest.ini`
- [ ] `tests/conftest.py`
- [ ] `tests/unit/test_simple_bus.py`

### Documentation

- [x] `PROJECT.md`
- [x] `VERSION`
- [x] `CHANGELOG.md`
- [x] `CLAUDE.md`
- [x] `.planning/` structure
- [x] `docs/01_Requirements/`

---

## Task Mapping

| Deliverable | Task ID |
|-------------|---------|
| i_state_provider.py | P0-002 |
| i_resonance_encoder.py | P0-003 |
| i_bus.py | P0-004 |
| i_memory_storage.py | P0-005 |
| mock_state_providers.py | P0-006 |
| mock_resonance_encoder.py | P0-007 |
| simple_bus.py | P0-008 |
| master_registry.yaml | P0-009 |
| pytest setup | P0-010 |

---

## Acceptance Criteria

Phase 0 is complete when:

1. ✅ All interface files exist with correct ABC definitions
2. ✅ All mock adapters implement their interfaces
3. ✅ SimpleBus passes all unit tests
4. ✅ master_registry.yaml is valid YAML
5. ✅ `pytest` runs without errors
6. ✅ No imports from future systems (PhysioCore, Matrix, etc.)

---

## Sign-off

| Role | Name | Date | Approved |
|------|------|------|----------|
| Lead Dev | Claude Opus 4.5 | 2026-01-27 | ⏳ |
| Reviewer | - | - | ⏳ |
