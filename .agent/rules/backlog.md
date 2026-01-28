# Backlog Management Rule

> **Status:** 🟢 EVOLVING
> **Version:** 1.0.0

---

## Purpose
To ensure no idea or future task is lost during development by using the central `BACKLOG.md`.

---

## Rule

1. **Identification**: Whenever a new idea, potential optimization, or technical debt is identified but not part of the active task, the agent MUST suggest adding it to `BACKLOG.md`.
2. **Organization**: The `BACKLOG.md` at the root directory is the single source of truth for future work.
3. **Usage**: Before completing a major phase, the agent should review the backlog with the user to prioritize remaining items.

---

## Maintenance

- **Adding Items**: Simply append to the relevant category (High Priority, Future Ideas, Refactoring).
- **Moving to Tasks**: When a backlog item becomes active, it should be moved to the appropriate task specification and marked as "In Progress" or removed from the backlog.

---

*Keep the vision alive, one entry at a time.*
