# CIM Payload Specification (v0.1.0)

> **Module:** Orchestrator (CIM)
> **Purpose:** Defines the data contract between internal state/memory and the LLM Bridge.
> **Status:** 🟢 STABLE

---

## 1. Context Bundle Structure

The `ContextBundle` is the internal container that aggregates all necessary data for a single cognitive turn.

### Schema (JSON Representation)
```json
{
  "user_input": "String: The raw message from user",
  "system_identity": "String: Core persona instructions",
  "timestamp": "ISO8601: When the bundle was assembled",
  "memory_context": [
    {
      "type": "episodic|semantic",
      "content": "String: Formatted text or excerpt",
      "relevance_score": "Float: 0.0-1.0",
      "metadata": {}
    }
  ],
  "state_context": {
    "bus:physical": {
      "hormones": { "oxytocin": 0.8, "cortisol": 0.2 },
      "vitals": { "heart_rate": 72 }
    },
    "bus:psychological": {
      "emotions": { "valence": 0.7, "arousal": 0.3 },
      "mood": "calm"
    },
    "bus:phenomenological": {
      "qualia": "Warm sunlight texture"
    }
  }
}
```

---

## 2. LLM Message Formation

The `ContextBuilder` transforms the `ContextBundle` into a `List[LLMMessage]`.

### System Message Template
The system message is dynamically constructed at runtime:

```markdown
# Identity
{{system_identity}}

You are EVA. Respond naturally and authentically.

## Current State
- **Physical:** {{state_context.bus:physical}}
- **Psychological:** {{state_context.bus:psychological}}

## Relevant Memories
- {{memory_context[0].content}}
- {{memory_context[1].content}}
```

---

## 3. Future Expansion (Phase 3 & 4)

| Data Type | Source Channel | CIM Hook | Description |
|-----------|----------------|----------|-------------|
| **Emotional Vector** | `bus:psychological` | `_gather_state` | 9D vector affecting word choice |
| **Hormone Levels** | `bus:physical` | `_gather_state` | Affects arousal and response speed |
| **Qualia Tag** | `bus:phenomenological`| `_gather_state` | Adds "sensory texture" to response |

---

## 4. Validation Rules

1. **Token Constraint**: The total system message + history + user input must not exceed the provider's limit (default: 4000 tokens).
2. **Memory Limit**: Maximum 5 most relevant memories are injected by default to prevent context dilution.
3. **State Freshness**: Only state messages published within the last 300 seconds are considered "Active State".

---

## 5. Resonance Compression Protocol (H9)

To optimize token usage for **State History**, we use the `H9` codec.

### Format
`[H9-{RI}{Str}{War}{Dri}{Cla}{Joy}{Sta}{Ori}{Mom}]`

### Fields
1. RI (Resonance Index)
2. Stress
3. Warmth
4. Drive
5. Clarity
6. Joy
7. Stability
8. Orientation
9. Momentum

### Example
Raw: `RI:0.45, Str:0.55, War:1.0, Dri:0.62, Cla:0.57, Joy:0.50, Sta:0.80, Ori:0.60, Mom:0.15`
Encoded: `[H9-4555M625750806015]`

This tag is appended to historical turns in the LLM context.
