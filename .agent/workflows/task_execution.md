# Workflow: Task Execution

> **Purpose:** Standard procedure for executing tasks
> **Audience:** Antigravity agents

---

## Prerequisites

Before starting any task:

1. ✅ Read `.agent/rules/constitution.md`
2. ✅ Read `.agent/rules/phase_rules.md`
3. ✅ Read `.agent/rules/coding_standards.md`

---

## Step 1: Pick a Task

1. Go to `.planning/tasks/`
2. Find a task with `status: pending`
3. Check `depends_on:` - all dependencies must be `done`
4. Read the full task YAML file

---

## Step 2: Understand the Spec

Each task has a `spec:` section containing:
- Exact code to implement
- File path for output
- Interface definitions

**Important:** Follow the spec exactly. Don't add extra features.

---

## Step 3: Create the File

1. Create the file at the specified `output_file:` path
2. Copy the code from `spec:` section
3. Ensure proper formatting (Black, isort)
4. Add `__init__.py` if creating a new package

---

## Step 4: Verify

Check all `acceptance_criteria:`:

```yaml
acceptance_criteria:
  - File exists at specified path
  - Class implements correct ABC
  - All methods are abstract
  - Type hints are complete
  - Docstrings explain purpose
```

---

## Step 5: Update Task Status

Edit the task YAML file:

```yaml
# Before
status: pending

# After
status: done
completed_at: "2026-01-27T15:00:00"
completed_by: "agent-name"
```

---

## Step 6: Report

Send completion report:

```
Task P0-002 completed.
- Created: contracts/ports/i_state_provider.py
- Lines: 28
- All acceptance criteria met.
```

---

## Common Mistakes to Avoid

### ❌ Don't Over-Engineer

```python
# Bad: Adding features not in spec
class IStateProvider(ABC):
    @abstractmethod
    def get_current_state(self) -> Dict: ...

    @abstractmethod
    def get_history(self) -> List[Dict]: ...  # Not in spec!
```

### ❌ Don't Skip Type Hints

```python
# Bad
def get_state(self, slot):
    ...

# Good
def get_state(self, slot: str) -> Optional[Dict[str, Any]]:
    ...
```

### ❌ Don't Forget __init__.py

```
contracts/
├── ports/
│   ├── i_state_provider.py
│   └── (missing __init__.py!)  # ❌
```

---

## Handling Blockers

If you encounter a blocker:

1. Document the issue in the task file
2. Set `status: blocked`
3. Add `blocked_reason:` field
4. Move to next available task
5. Report the blocker

```yaml
status: blocked
blocked_reason: "Depends on P0-002 which has unclear spec"
```

---

## Task Dependencies

```
Wave 1 (No deps):     P0-002, P0-003, P0-004, P0-005, P0-009
                           ↓
Wave 2 (After Wave 1): P0-006, P0-007, P0-008
                           ↓
Wave 3 (After Wave 2): P0-010
```

Multiple agents can work on Wave 1 tasks in parallel.
