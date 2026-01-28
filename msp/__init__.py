"""
Memory & Soul Passport (MSP)

The unified memory system for EVA.
Handles episodic, semantic, and sensory memories.

Version History:
- 0.0.1: Initial structure (P1-001)
- 0.0.2: EpisodicMemory schema (P1-002)
- 0.0.3: SemanticMemory schema (P1-003)
- 0.0.4: Episodic V2 alignment (turn_user, turn_llm, situation_context)
- 0.0.5: Enhanced context (location_context, domain_area, mission_goal, agent_role)
- 0.0.6: StructuredSummary (action_taken, key_outcome, future_implication)
- 0.0.7: Renamed raw_text to text_excerpt
- 0.1.0: SensoryMemory schema (P1-004)
- 0.1.1: Bidirectional Memory Crosslinks (Episodic <-> Sensory <-> Semantic)
- 0.2.0: FileMemoryStore implementation (P1-005)
"""

__version__ = "0.2.0"
__schema_version__ = "episodic_v3"  # Sensory is SMEM_v1

