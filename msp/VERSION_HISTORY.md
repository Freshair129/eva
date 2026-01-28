# MSP Version History

> **Module:** Memory & Soul Passport (MSP)
> **Current Version:** 0.0.8
> **Schema Version:** episodic_v3

---

## [0.0.9] - 2026-01-29

### Added
- **MSP Master Specification** (`msp/README.md`): Detailed guide for all fields, meanings, and examples to prevent agent hallucination.

---

## [0.0.8] - 2026-01-28

### Changed
- **File-per-Record Architecture**
  - Created `turn.py` with standalone `TurnUser`, `TurnLLM` classes
  - Refactored `episodic.py` to use `turn_refs: List[str]` instead of embedded turns
  - Added `get_file_path()` methods for consistent path generation
  - Episode type changed from `episodic_v2` to `episodic_v3`

### File Structure
```
memory/
├── episodes/{year}/{month}/{episode_id}.json
└── turns/
    ├── user/{year}/{month}/{turn_id}.json
    └── llm/{year}/{month}/{turn_id}.json
```

---

## [0.0.7] - 2026-01-28

### Changed
- Renamed `raw_text` to `text_excerpt` in `TurnUser` for consistency with `TurnLLM`

---

## [0.0.6] - 2026-01-28

### Added
- **StructuredSummary** dataclass in `episodic.py`
  - `content`: Main summary text
  - `action_taken`: What was done
  - `key_outcome`: Result or conclusion
  - `future_implication`: Next steps or warnings

---

## [0.0.5] - 2026-01-28

### Added
- Enhanced `SituationContext` fields:
  - `location_context` (local_dev, mobile_ssh, cloud_prod)
  - `domain_area` (coding, music_analysis)
  - `mission_goal` (Macro goal like "Apply for job")
  - `agent_role` (Senior Dev, Friend)

---

## [0.0.4] - 2026-01-28

### Changed
- **Episodic V2 Alignment**
  - Refactored `EpisodicMemory` to match V2 JSON schema
  - Added nested `TurnUser`, `TurnLLM`, `SituationContext` dataclasses
  - Added `episode_id`, `session_id`, `event_id` hierarchy
  - Added `cues` for specific retrieval triggers

---

## [0.0.3] - 2026-01-28

### Added
- **SemanticMemory** schema in `semantic.py`
  - Subject-Predicate-Object (SPO) structure for knowledge graphs
  - `as_triple()` method for readable format
  - `confidence`, `source`, `access_count` tracking

---

## [0.0.2] - 2026-01-28

### Added
- **EpisodicMemory** schema in `episodic.py`
  - Initial implementation with `content`, `summary`, `tags`
  - `to_dict()` and `from_dict()` serialization

---

## [0.0.1] - 2026-01-27

### Added
- Initial MSP directory structure
  - `msp/` root package
  - `msp/schema/` for data schemas
  - `msp/storage/` for storage adapters
  - `msp/tests/` for unit tests
- `__init__.py` with initial version `0.1.0`

---

*Signed: Antigravity*
