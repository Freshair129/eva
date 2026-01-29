"""MSP Integration - Memory hooks for Orchestrator."""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from msp.msp_engine import MSPEngine
from msp.schema.episodic import EpisodicMemory, SituationContext, StructuredSummary
from msp.schema.semantic import SemanticMemory
from contracts.ports.i_bus import IBus
from orchestrator.integration.bus_integration import BusIntegration
from orchestrator.orchestrator_engine import OrchestratorEngine, OrchestratorResponse

logger = logging.getLogger(__name__)

class MSPIntegration:
    """
    Handles memory operations during conversation.

    Provides hooks to:
    - Store conversations as episodic memories
    - Extract semantic facts from conversations
    """

    def __init__(self, msp: MSPEngine):
        """
        Initialize integration.

        Args:
            msp: MSP engine instance
        """
        self._msp = msp

    def store_turn(
        self,
        user_input: str,
        response: str,
        context_id: str = "sess_default",
        interaction_mode: str = "deep_discussion"
    ) -> str:
        """
        Store a conversation turn as a simplified episodic memory.
        Note: In Phase 2, we store each turn as a mini-episode for simplicity,
        or we could group them. Here we follow the spec's intent.
        """
        
        # Create a structured summary
        summary_text = self._generate_summary(user_input, response)
        summary = StructuredSummary(
            content=summary_text,
            action_taken="Responded to user",
            key_outcome="Information exchanged"
        )
        
        # Setup context
        context = SituationContext(
            context_id=context_id,
            interaction_mode=interaction_mode,
            stakes_level="low",
            time_pressure="low"
        )
        
        # Generate unique ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ep_id = f"EP_{timestamp}"
        
        # Create Episode
        episode = EpisodicMemory(
            episode_id=ep_id,
            situation_context=context,
            summary=summary,
            tags=["conversation", context_id]
        )
        
        # Set raw content if we want full history in the file
        # (Though schemas usually prefer references to turns)
        # For now, we use the store() logic which expects a dict
        m_id = self._msp.store(episode.to_dict())
        
        return m_id

    def _generate_summary(self, user_input: str, response: str) -> str:
        """Generate brief summary of turn."""
        # Simple approach: first sentence of response
        first_sentence = response.split('.')[0] + '.'
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:100] + '...'
        return f"User asked about '{user_input[:30]}...'. EVA replied: {first_sentence}"

    def extract_facts(self, user_input: str, episode_id: Optional[str] = None) -> List[str]:
        """
        Extract semantic facts from user input.
        Detects simple patterns and stores them in Semantic Memory.
        """
        patterns = [
            ("I am ", "is"),
            ("I'm ", "is"),
            ("I like ", "likes"),
            ("I have ", "has"),
            ("My name is ", "has_name"),
            ("I prefer ", "prefers"),
        ]

        user_lower = user_input.lower()
        extracted_ids = []

        for pattern, predicate in patterns:
            if pattern.lower() in user_lower:
                idx = user_lower.find(pattern.lower())
                obj = user_input[idx + len(pattern):].split('.')[0].split(',')[0].strip()
                if obj and len(obj) < 50:
                    fact = SemanticMemory(
                        subject="User",
                        predicate=predicate,
                        object=obj,
                        source="conversation"
                    )
                    if episode_id:
                        fact.episode_refs.append(episode_id)
                    
                    fact_id = self._msp.store(fact.to_dict())
                    extracted_ids.append(fact_id)
                    logger.info(f"Extracted fact: User {predicate} {obj} ({fact_id})")

        return extracted_ids


class IntegratedOrchestrator:
    """
    Orchestrator wrapper that automatically handles memory persistence and bus events.
    """

    def __init__(self, orchestrator: OrchestratorEngine, msp: MSPEngine, bus: Optional[IBus] = None):
        self._orchestrator = orchestrator
        self._integration = MSPIntegration(msp)
        self._bus_integration = BusIntegration(bus) if bus else None
        self._msp = msp

    def process(self, user_input: str) -> OrchestratorResponse:
        """
        Process user input with automatic memory storage, fact extraction, and bus events.
        """
        # 1. Publish turn started
        if self._bus_integration:
            self._bus_integration.publish_turn_started(user_input)

        # 2. Process through core engine (Assemble context -> LLM)
        try:
            response = self._orchestrator.process(user_input)
        except Exception as e:
            if self._bus_integration:
                self._bus_integration.publish_error(str(e))
            raise

        # 3. Extract facts from user input (Semantic)
        fact_ids = self._integration.extract_facts(user_input)

        # 4. Store the interaction (Episodic)
        episode_id = self._integration.store_turn(user_input, response.content)
        
        # 5. Publish turn completed
        if self._bus_integration:
            self._bus_integration.publish_turn_completed(
                user_input, 
                response.content, 
                response.tokens_used
            )

        return response

def create_integrated_orchestrator(
    orchestrator: OrchestratorEngine,
    msp: MSPEngine,
    bus: Optional[IBus] = None
) -> IntegratedOrchestrator:
    """Factory to create integrated orchestrator."""
    return IntegratedOrchestrator(orchestrator, msp, bus)
