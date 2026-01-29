"""Orchestrator Engine - Central Nervous System."""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from contracts.ports.i_llm_provider import ILLMProvider, LLMMessage
from contracts.ports.i_bus import IBus
from orchestrator.cim.cim_engine import CIMEngine
from orchestrator.cim.context_builder import ContextBuilder


@dataclass
class ConversationTurn:
    """A single turn in conversation."""
    role: str
    content: str
    timestamp: datetime
    h5_tag: Optional[str] = None


@dataclass
class OrchestratorResponse:
    """Response from orchestrator."""
    content: str
    context_used: Dict[str, Any]
    model: str
    tokens_used: int


class OrchestratorEngine:
    """
    Central Nervous System (CNS) - The Orchestrator.

    Coordinates:
    - CIM for context assembly
    - LLM for reasoning
    - Bus for state events
    - MSP for memory

    This is the main entry point for user interaction.
    """

    def __init__(
        self,
        llm_provider: ILLMProvider,
        cim: CIMEngine,
        bus: Optional[IBus] = None,
        msp: Any = None,
        max_history_turns: int = 20
    ):
        """
        Initialize Orchestrator.

        Args:
            llm_provider: LLM for reasoning
            cim: Context Injection Manager
            bus: Event bus (optional)
            msp: Memory system (optional)
            max_history_turns: Number of turns to keep in context
        """
        self._llm = llm_provider
        self._cim = cim
        self._bus = bus
        self._msp = msp
        self._max_history_turns = max_history_turns
        self._context_builder = ContextBuilder()
        self._conversation_history: List[ConversationTurn] = []
        self._bus = bus
        self._context_builder = ContextBuilder()
        self._conversation_history: List[ConversationTurn] = []

        # Wire up CIM
        if msp:
            self._cim.set_msp(msp)
        if bus:
            self._cim.set_bus(bus)

    def process(self, user_input: str) -> OrchestratorResponse:
        """
        Process user input through cognitive flow.
        """
        # Step 1: Build context
        context_bundle = self._cim.build_context(user_input)

        # Step 2: Format as messages
        history = self._get_history_for_llm()
        messages = self._context_builder.build_messages(
            context_bundle,
            conversation_history=history
        )

        # Step 3: Call LLM
        llm_response = self._llm.chat(messages)
        
        # Step 3.5: Calculate H5 Tag (State Compression)
        # In Phase 3, we would have real values. For now, we simulate or map from state.
        # We try to extract from context_bundle.state_context or use defaults.
        h5_tag = self._generate_h5_tag(context_bundle.state_context)

        # Step 4: Store in history (Attach tag to ASSISTANT response usually, or User?)
        # ADR-007 Example shows BOTH user and AI having tags.
        # For now, we tag the Assistant state (Response state represents state AFTER processing).
        self._add_to_history("user", user_input) # User turn might have pre-state? Keep simple.
        self._add_to_history("assistant", llm_response.content, h5_tag)

        # Step 5: Publish events
        self._publish_turn_event(user_input, llm_response.content)

        # Step 6: Return response
        return OrchestratorResponse(
            content=llm_response.content,
            context_used={
                "memory_count": len(context_bundle.memory_context),
                "has_state": bool(context_bundle.state_context)
            },
            model=llm_response.model,
            tokens_used=llm_response.tokens_used
        )

    def _generate_h5_tag(self, state_context: Dict[str, Any]) -> Optional[str]:
        """Generate H5 tag from gathered state."""
        try:
            from capabilities.core.state_tools import compress_state
            
            # Map/Flatten state structure to flat h5 dict
            # Currently state_context is {"bus:physical": {...}, ...}
            # We need to extract the keys H5 expects.
            
            # Temporary Mapping for Phase 2/3 transition
            # If keys don't exist, they default to 0.0 in codec, 
            # but we want reasonable defaults (e.g. 0.5) if missing 
            # so it doesn't look like "Death" state (000000).
            
            flat_state = {}
            # Logic to extract real values would go here.
            # For now, if we don't have real values, we return None or minimal.
            # Actually, let's look for known keys in the nested dicts
            
            # TODO: Improve mapping logic in Phase 3 actual implementation
            return compress_state(flat_state) 
        except ImportError:
            return None

    def set_system_identity(self, identity: str) -> None:
        """Update system identity prompt."""
        self._cim.set_system_identity(identity)

    def clear_history(self) -> None:
        """Clear conversation history."""
        self._conversation_history.clear()

    def get_history(self) -> List[ConversationTurn]:
        """Get conversation history."""
        return self._conversation_history.copy()

    def _add_to_history(self, role: str, content: str, h5_tag: Optional[str] = None) -> None:
        """Add turn to history."""
        self._conversation_history.append(ConversationTurn(
            role=role,
            content=content,
            timestamp=datetime.now(),
            h5_tag=h5_tag
        ))

    def _get_history_for_llm(self) -> List[Dict[str, str]]:
        """Format history for LLM with sliding window."""
        # Sliding window: keep only last N turns
        recent_history = self._conversation_history[-self._max_history_turns:]
        
        formatted = []
        for turn in recent_history:
            content = turn.content
            # Append H5 tag if present
            if turn.h5_tag:
                content += f" {turn.h5_tag}"
            
            formatted.append({"role": turn.role, "content": content})
            
        return formatted

    def _publish_turn_event(self, user_input: str, response: str) -> None:
        """Publish turn event to bus."""
        if self._bus:
            try:
                self._bus.publish("orchestrator:turn", {
                    "user_input": user_input,
                    "response": response[:200],  # Truncate
                    "timestamp": datetime.now().isoformat()
                })
            except Exception:
                pass
