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
        msp: Any = None
    ):
        """
        Initialize Orchestrator.

        Args:
            llm_provider: LLM for reasoning
            cim: Context Injection Manager
            bus: Event bus (optional)
            msp: Memory system (optional)
        """
        self._llm = llm_provider
        self._cim = cim
        self._bus = bus
        self._msp = msp
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

        Steps:
        1. Build context (CIM)
        2. Format for LLM
        3. Call LLM
        4. Store in history
        5. Publish events
        6. Return response

        Args:
            user_input: User's message

        Returns:
            OrchestratorResponse with LLM output and metadata
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

        # Step 4: Store in history
        self._add_to_history("user", user_input)
        self._add_to_history("assistant", llm_response.content)

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

    def set_system_identity(self, identity: str) -> None:
        """Update system identity prompt."""
        self._cim.set_system_identity(identity)

    def clear_history(self) -> None:
        """Clear conversation history."""
        self._conversation_history.clear()

    def get_history(self) -> List[ConversationTurn]:
        """Get conversation history."""
        return self._conversation_history.copy()

    def _add_to_history(self, role: str, content: str) -> None:
        """Add turn to history."""
        self._conversation_history.append(ConversationTurn(
            role=role,
            content=content,
            timestamp=datetime.now()
        ))

    def _get_history_for_llm(self) -> List[Dict[str, str]]:
        """Format history for LLM."""
        return [
            {"role": turn.role, "content": turn.content}
            for turn in self._conversation_history
        ]

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
