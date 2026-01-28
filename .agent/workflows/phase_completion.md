# Workflow: Phase Completion

> **Purpose:** Procedure for completing a development phase
> **Audience:** Lead Dev

---

## Prerequisites

Before declaring a phase complete:

1. All tasks in the phase are `status: done`
2. All code has been reviewed
3. All tests pass
4. Documentation is updated

---

## Step 1: Verify All Tasks Complete

Check `.planning/tasks/`:

```bash
# All phase tasks should be done
grep "status:" .planning/tasks/P0-*.yaml
```

Expected: All show `status: done`

---

## Step 2: Run Tests

```bash
cd E:\eva
python -m pytest tests/ -v
```

Expected: All tests pass (100%)

---

## Step 3: Verify Deliverables

Check against phase checklist:

For Phase 0:
- [ ] `contracts/ports/i_state_provider.py` exists
- [ ] `contracts/ports/i_resonance_encoder.py` exists
- [ ] `contracts/ports/i_bus.py` exists
- [ ] `contracts/ports/i_memory_storage.py` exists
- [ ] `adapters/mocks/mock_state_providers.py` exists
- [ ] `adapters/mocks/mock_resonance_encoder.py` exists
- [ ] `adapters/simple_bus.py` exists
- [ ] `config/master_registry.yaml` exists
- [ ] `pytest.ini` exists
- [ ] `tests/conftest.py` exists

---

## Step 4: Update Documentation

1. Update `VERSION` file
2. Update `CHANGELOG.md`
3. Update `.planning/STATE.md`
4. Update `docs/01_Requirements/PHASE_X_CHECKLIST.md`

---

## Step 5: Version Bump

```bash
# Update VERSION
echo "0.2.0" > VERSION

# Update CHANGELOG.md
# Add entry for new version
```

---

## Step 6: Create Git Tag

```bash
git add .
git commit -m "[Phase 0] Foundation complete"
git tag -a v0.1.0 -m "Phase 0: Foundation"
```

---

## Step 7: Announce Completion

Report to project owner:

```
Phase 0 Complete ✅

Version: 0.1.0
Deliverables:
- 4 port interfaces
- 3 mock adapters
- 1 simple bus
- 1 master registry
- Test infrastructure

Tests: 100% pass
Ready for: Phase 1 (MSP Core)
```

---

## Step 8: Prepare Next Phase

1. Create `docs/01_Requirements/PHASE_1_CHECKLIST.md`
2. Create tasks in `.planning/tasks/P1-*.yaml`
3. Update `.planning/STATE.md` with new focus

---

## Phase Completion Criteria

| Phase | Key Criteria |
|-------|--------------|
| 0 | All interfaces + mocks + tests pass |
| 1 | MSP stores/retrieves memories |
| 2 | Basic conversation works |
| 3 | Emotions affect responses |
| 4 | Biology drives emotions |
| 5 | Full resonance encoding |
| 6 | Knowledge accessible |
| 7 | Production ready, all NFRs met |
