# ADR-007: Resonance State Compression Protocol (H9)

> **Status:** 🟢 ACCEPTED
> **Date:** 2026-01-30
> **Context:** Token optimization for State History in LLM Context Window.

## Problem
Passing full JSON state objects consumes excessive tokens. We need a lossless compression for the full 9D Psychological Matrix.

## Solution
Implement **H9 Resonance Codec**.

### Protocol Specification: H9
Format: `[H9-{ResonanceIndex}{Stress}{Warmth}{Drive}{Clarity}{Joy}{Stability}{Orientation}{Momentum}{Urgency}]`

**Fields (10 Total - RI + 9 attributes):**
1. **RI**: Resonance Index (Cognitive Alignment)
2. **Str**: Stress (Core)
3. **War**: Warmth (Core)
4. **Dri**: Drive (Core)
5. **Cla**: Clarity (Core)
6. **Joy**: Joy (Core)
7. **Sta**: Stability (Meta)
8. **Ori**: Orientation (Meta)
9. **Mom**: Momentum Intensity (Physics)
10. **Urg**: Reflex Urgency (System)

**Encoding Rules:**
- Precision: 2 decimal places (0.XX -> XX).
- Max: 1.0 -> M.
- Length: Fixed 20 chars (or 10 chars if using M).
- Example: `[H9-4555M62575080601590]`

### Benefits (Benefit²)
1. **Compression:** Reduces ~100 chars to ~15 chars (~85% saving).
2. **Security:** Obfuscates internal state structure from casual observation.
3. **Continuity:** Allows LLM to see the *flow* of emotions over time (e.g., Rising Stress: `20`->`40`->`60`).

## Implementation Strategy
- **CIM:** Implement `encode_h5(state)` and `decode_h5(string)`.
- **Orchestrator:** Store full JSON in `episodes/` (Archival), but inject `[H5-...]` tag into `conversation_history` sent to LLM.

## Example
```text
User: Hello (Tag: [H5-100550505050])
AI: Hi there! (Tag: [H5-1505506060M])
```
