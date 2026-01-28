# ADR-004: Version Reset to 0.1.0

> **Status:** Accepted
> **Date:** 2026-01-27
> **Deciders:** Lead Dev (Claude Opus 4.5), Project Owner

---

## Context

EVA v9.x reached version 9.7.x, but the version numbers were not managed properly:

**Problems with v9.x versioning:**
1. No formal changelog between versions
2. Version numbers jumped arbitrarily
3. No clear definition of what constitutes a major/minor/patch
4. Module versions (2.x) disconnected from system version (9.x)
5. High version number implies maturity that doesn't exist

**Additionally:**
- The project is being rebuilt from scratch with new architecture
- This is not an incremental upgrade but a fresh start

---

## Decision

Reset version to **0.1.0** and follow **Semantic Versioning** strictly.

### Version Format

```
MAJOR.MINOR.PATCH

0.x.x = Development/Pre-release (breaking changes allowed)
1.0.0 = First stable release
```

### Version Milestones

| Version | Meaning |
|---------|---------|
| 0.1.0 | Phase 0 complete (Foundation) |
| 0.2.0 | Phase 1 complete (MSP) |
| 0.3.0 | Phase 2 complete (Orchestrator) |
| 0.4.0 | Phase 3 complete (Psychology) |
| 0.5.0 | Phase 4 complete (Biology) |
| 0.6.0 | Phase 5 complete (Perception) |
| 0.7.0 | Phase 6 complete (Knowledge) |
| 1.0.0 | Phase 7 complete (Production) |

### Semantic Versioning Rules

```
Given version MAJOR.MINOR.PATCH:

MAJOR: Incompatible API changes
MINOR: New functionality (backward compatible)
PATCH: Bug fixes (backward compatible)

Pre-release (0.x.x):
- Breaking changes allowed in MINOR bumps
- Used for development phase
```

---

## Consequences

### Positive

1. **Honest Versioning:** 0.x signals "in development"
2. **Clear Milestones:** Each phase = one minor version
3. **SemVer Compliance:** Industry standard
4. **Fresh Start:** No baggage from v9.x confusion
5. **Meaningful 1.0.0:** First stable release is significant

### Negative

1. **Perception:** 0.x may seem "not ready" (which is true)
2. **History Loss:** v9.x history not reflected in version

### Mitigations

1. **Codename:** "EVA Genesis" indicates new beginning
2. **Documentation:** This ADR explains the reset
3. **Changelog:** Maintain proper CHANGELOG.md

---

## Versioning Process

### 1. Version File

```
# VERSION
0.1.0
```

### 2. Changelog Format

```markdown
# CHANGELOG.md

## [Unreleased]
- Current work

## [0.2.0] - YYYY-MM-DD
### Added
- MSP standalone functionality
### Changed
- ...

## [0.1.0] - 2026-01-27
### Added
- Project foundation
- Port interfaces
- Mock adapters
```

### 3. Git Tags

```bash
git tag -a v0.1.0 -m "Phase 0: Foundation"
git tag -a v0.2.0 -m "Phase 1: MSP Core"
```

---

## Alternatives Considered

### 1. Continue from v10.0.0
- Rejected: Implies v9.x → v10.x upgrade path
- This is a rebuild, not an upgrade

### 2. Start from v1.0.0
- Rejected: 1.0 implies stability
- We're in development phase

### 3. Use Date-Based Versioning (CalVer)
- Rejected: SemVer is more appropriate for this project
- CalVer better for continuously deployed services

---

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- EVA v9.x version history (informal)
