# Version Control Rule

> **Status:** 🟢 ENFORCED
> **Version:** 1.0.0

---

## Rule

**Every time you modify ANY system module (msp, contracts, adapters, etc.), you MUST:**

1. **Bump the version** in `__init__.py`
2. **Update `VERSION_HISTORY.md`** in that module
3. **Update main `CHANGELOG.md`** with summary
4. **Sync changes to Git** (Commit & Push)

---

## Enforcement

This rule is **AUTOMATIC**. You do not need to call `/version-bump`.

When completing ANY code modification to a tracked module:
- Check if `__init__.py` has `__version__`
- If yes, follow the versioning workflow
- If no, create versioning infrastructure first

---

## Tracked Modules

| Module | Has Versioning |
|--------|----------------|
| `msp/` | ✅ Yes |
| `contracts/` | ⏳ Pending |
| `adapters/` | ⏳ Pending |

---

## Exception

Skip version bump only if:
- Change is documentation-only (README, comments)
- Change is in test files only
- User explicitly says "skip version bump"

---

*This rule is loaded automatically via .agent/rules/*
