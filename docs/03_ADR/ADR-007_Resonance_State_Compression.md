# ADR-007: Resonance State Compression Protocol

> **Status:** 🟢 ACCEPTED
> **Date:** 2026-01-29
> **Context:** Token optimization for State History in LLM Context Window.

## Problem
Passing full JSON state objects for every turn in the conversation history consumes excessive tokens (approx 200 tokens/turn). We need a way to preserve emotional history without bloating the context.

## Solution
Implement a **Lossless Semantic Compression Protocol** (Resonance Codec) for history entries.

### Protocol Specification: H5
Format: `[H5-{RI}{Stress}{Social}{Drive}{Clarity}{Joy}]`

**Encoding Rules:**
1. **Precision:** 2 decimal places (0.00 - 1.00).
2. **digits:** Map `0.XX` to `XX`. (e.g., `0.45` -> `45`).
3. **Max Value:** `1.00` is mapped to character `M`.
4. **Delimiters:** None (fixed width 2 chars per value, except M). 
   *Correction:* If M is used, it replaces the 2 digits.
   *Variant:* User example `4555M625750` suggests variable width or M stands for 100?
   User Example: `RI:0.45, St:0.55, So:1.0, Dr:0.62, Cl:0.57, Jo:0.50` -> `4555M625750`
   - 45 (RI)
   - 55 (St)
   - M (So) -> 1 char replacing 2? Or represents "Max"?
   - 62 (Dr)
   - 57 (Cl)
   - 50 (Jo)

**Decoding Key (System Prompt):**
> "State Code [H5]: RI,Stress,Social,Drive,Clarity,Joy. Digits=0.xx, M=1.0."

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
