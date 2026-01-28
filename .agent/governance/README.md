# .agent/governance — Enforcement Policies

> **Purpose:** Define and enforce project constraints
> **Status:** Active

---

## Documents

| File | Purpose |
|------|---------|
| `root_policy.yaml` | Allowed files/directories at root |

---

## Root Policy

The `root_policy.yaml` defines:

1. **Allowed root files** - Only these files can exist at `E:\eva\`
2. **Allowed root directories** - Only these folders can exist at root
3. **Cleanup destinations** - Where to move violations
4. **Phase requirements** - Which directories for which phase

### Checking Compliance

```bash
# Manual check (future: automated)
ls E:\eva\

# Compare against root_policy.yaml allowed lists
```

### Handling Violations

If you find a file/directory that shouldn't be at root:

1. Check `cleanup_destinations` for where it should go
2. Move it to the appropriate location
3. Update any imports/references

---

## Future Enforcement

When implemented, will include:

- Pre-commit hook to block violations
- CI check for pull requests
- Automated cleanup suggestions
