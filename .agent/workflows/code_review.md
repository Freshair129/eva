# Workflow: Code Review

> **Purpose:** Standard procedure for reviewing implemented code
> **Audience:** Lead Dev, Reviewers

---

## Review Checklist

### 1. File Location

- [ ] File is at correct path (per task spec)
- [ ] Package has `__init__.py`
- [ ] No files at wrong locations

### 2. Interface Compliance

- [ ] Implements correct ABC (if adapter)
- [ ] All abstract methods defined (if interface)
- [ ] Method signatures match spec

### 3. Type Hints

- [ ] All function parameters have type hints
- [ ] All return types specified
- [ ] Complex types use `typing` module

### 4. Documentation

- [ ] Module docstring present
- [ ] Class docstring explains purpose
- [ ] Public methods have docstrings
- [ ] Docstrings follow Google style

### 5. Code Quality

- [ ] No print statements (use logging)
- [ ] No hardcoded paths
- [ ] No unused imports
- [ ] Follows coding_standards.md

### 6. Constitution Compliance

- [ ] Respects phase_rules.md relaxations
- [ ] No constitutional violations
- [ ] Uses interfaces, not concrete classes

---

## Review Response Format

### Approved

```
✅ APPROVED

Task: P0-002
File: contracts/ports/i_state_provider.py
Reviewer: Lead Dev

All criteria met. Ready for merge.
```

### Changes Requested

```
⚠️ CHANGES REQUESTED

Task: P0-002
File: contracts/ports/i_state_provider.py
Reviewer: Lead Dev

Issues:
1. Missing type hint on line 15
2. Docstring incomplete for get_state_type()

Please fix and resubmit.
```

### Rejected

```
❌ REJECTED

Task: P0-002
File: contracts/ports/i_state_provider.py
Reviewer: Lead Dev

Reason: Does not implement spec correctly.
Required: ABC with 3 abstract methods
Found: Regular class with 2 methods

Please re-read task spec and reimplement.
```
