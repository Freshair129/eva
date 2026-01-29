# Memory Access

> **Status:** Managed by MSP

---

Memory is not stored as static files here. Instead, the CIM queries the **Memory System Passport (MSP)** for relevant memories based on semantic similarity.

## Access Pattern

```python
# CIM calls MSP for memory retrieval
memories = msp.semantic_search(user_input, limit=5)
```

## Memory Types

- **Episodic:** Autobiographical (conversations, events)
- **Semantic:** Facts (user preferences, learned knowledge)
- **Sensory:** Perceptual data (qualia, textures)

---

*See `msp/` for implementation details.*
