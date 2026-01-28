---
description: Standard workflow for version bumping when modifying any system module
---

# Version Control Workflow

## When to Use
Every time you **modify ANY system module** (msp, orchestrator, eva_matrix, etc.), you MUST follow this workflow.

---

## Versioning Standard (Semantic Versioning)

```
MAJOR.MINOR.PATCH
  │      │     └─ Bug fixes, typos, small tweaks
  │      └─────── New features, schema additions
  └────────────── Breaking changes, architecture changes
```

**Example:** `0.0.8` → `0.0.9` (patch) → `0.1.0` (minor) → `1.0.0` (major)

---

## Required Files Per Module

Every system module MUST have:

1. **`__init__.py`** with:
   ```python
   __version__ = "X.Y.Z"
   __schema_version__ = "schema_name_vN"  # if applicable
   ```

2. **`VERSION_HISTORY.md`** with:
   - Version number and date
   - What changed (Added/Changed/Removed/Fixed)
   - Breaking changes highlighted

---

## Workflow Steps

### Step 1: Before Making Changes
// turbo
```bash
# Check current version
python -c "import {module}; print({module}.__version__)"
```

### Step 2: Make Your Changes
- Implement the feature/fix
- Run tests to verify

### Step 3: Bump Version in `__init__.py`
- Increment version number according to change type:
  - **PATCH** (0.0.X): Bug fixes, renames, small tweaks
  - **MINOR** (0.X.0): New features, new fields, new files
  - **MAJOR** (X.0.0): Breaking changes, architecture refactors

### Step 4: Update `VERSION_HISTORY.md`
Add entry at TOP of file:
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description

### Breaking
- ⚠️ Breaking change description
```

### Step 5: Update Main `CHANGELOG.md`
Add summary entry under the appropriate section with link to module's VERSION_HISTORY.

### Step 6: Commit Message Format
```
[{Module}] v{X.Y.Z}: Brief description

- Detail 1
- Detail 2
```

### Step 7: Sync with Remote Repository
// turbo
```bash
git add -A
git commit -m "[{Module}] v{X.Y.Z}: {Brief description}"
git push origin main
```

**Example:**
```
[MSP] v0.0.8: File-per-Record Architecture

- Created turn.py with standalone Turn classes
- Refactored episodic.py to use turn_refs
- Added get_file_path() methods
```

---

## Quick Reference

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Typo fix | PATCH | 0.0.8 → 0.0.9 |
| Rename field | PATCH | 0.0.9 → 0.0.10 |
| Add new field | MINOR | 0.0.10 → 0.1.0 |
| Add new class | MINOR | 0.1.0 → 0.2.0 |
| Change storage format | MAJOR | 0.2.0 → 1.0.0 |
| Break backward compat | MAJOR | 1.0.0 → 2.0.0 |

---

## Modules to Track

| Module | Path | Status |
|--------|------|--------|
| MSP | `msp/` | ✅ Tracked |
| Contracts | `contracts/` | ⏳ Pending |
| Adapters | `adapters/` | ⏳ Pending |
| Orchestrator | `orchestrator/` | ⏳ Not Created |
| EVA Matrix | `eva_matrix/` | ⏳ Not Created |
| PhysioCore | `physio_core/` | ⏳ Not Created |

---

*Signed: Antigravity*
