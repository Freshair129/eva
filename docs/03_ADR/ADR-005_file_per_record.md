# ADR-005: File-per-Record Architecture

> **Status:** Accepted
> **Date:** 2026-01-28
> **Deciders:** Antigravity

---

## Context

The initial Episodic Memory schema (v0.0.1 - v0.0.7) embedded conversation turns (`turn_user`, `turn_llm`) directly within the Episode object. This created significant overhead:
1. **Token Inefficiency**: Retrieving a single turn (e.g., "What did the user ask?") required loading the entire Episode and all its turns.
2. **Scalability**: JSON files would grow significantly as conversation turns increased, impacting I/O performance.
3. **Granularity**: Difficult to perform targeted RAG (Retrieval-Augmented Generation) on specific turns without pulling unnecessary context.

---

## Decision

Adopt a **File-per-Record** architecture for the Memory & Soul Passport (MSP).

1. **Episode Metadata**: Stored as a lightweight JSON containing summary, context, and references only.
2. **Normalized Turns**: Every `TurnUser` and `TurnLLM` is stored as an individual JSON file.
3. **Linking**: Episodes reference turns via `turn_refs` (List of IDs). Turns reference episodes via `episode_id` (Foreign Key).
4. **Physical Storage**: Use a hierarchical date-based folder structure to prevent filesystem bottleneck (e.g., `memory/episodes/2026/01/EP_xxx.json`).

---

## Consequences

### Positive
- **Extreme Token Efficiency**: AI can fetch exactly what it needs (e.g., only the user's question).
- **Scalability**: No single file grows indefinitely.
- **Git Friendliness**: Diffs show changes at the specific turn level.
- **Improved Retrieval**: Vector search can point to individual turns for higher precision.

### Negative
- **Inode Pressure**: Large number of small files can stress some filesystems (mitigated by subfolders).
- **JOIN Logic Required**: System must handle loading multiple files to reconstruct full context.

### Neutral
- Requires a robust indexing system (e.g., `index.json` or local DB) for performant listings.

---

## Alternatives Considered

### Option 1: Embedded JSONL (Normalized)
- Store all turns in a single `turns.jsonl`.
- **Reason Rejected**: Still requires scanning/parsing large files. Less "human-readable" for browsing individual records.

### Option 2: Full Embedded Episode
- Keep everything in one file.
- **Reason Rejected**: The "Token is Gold" principle made this untenable for long-term growth.

---

## References

- [Episodic Schema (episodic.py)](file:///e:/eva/msp/schema/episodic.py)
- [Turn Schema (turn.py)](file:///e:/eva/msp/schema/turn.py)
- Discussion on "Granularity vs Context" (Step 506-513)
