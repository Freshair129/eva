"""ContextBuilder - Formats context for LLM consumption."""

from typing import List, Dict, Any
from contracts.ports.i_llm_provider import LLMMessage
from orchestrator.cim.cim_engine import ContextBundle


class ContextBuilder:
    """
    Converts ContextBundle to LLM message format.

    Takes assembled context and produces a list of
    LLMMessage objects ready for the LLM provider.
    """

    def __init__(self, persona_name: str = "EVA"):
        """
        Initialize builder.

        Args:
            persona_name: Name for assistant persona
        """
        self._persona_name = persona_name

    def build_messages(
        self,
        bundle: ContextBundle,
        conversation_history: List[Dict[str, Any]] = None
    ) -> List[LLMMessage]:
        """
        Build LLM messages from context bundle.

        Args:
            bundle: Assembled context
            conversation_history: Previous turns (optional)

        Returns:
            List of LLMMessage ready for LLM
        """
        messages = []

        # System message with context
        system_content = self._build_system_message(bundle)
        messages.append(LLMMessage(role="system", content=system_content))

        # Add conversation history if provided
        if conversation_history:
            for turn in conversation_history:
                messages.append(LLMMessage(
                    role=turn.get("role", "user"),
                    content=turn.get("content", "")
                ))

        # Add current user message
        messages.append(LLMMessage(role="user", content=bundle.user_input))

        return messages

    def _build_system_message(self, bundle: ContextBundle) -> str:
        """
        Build the system message content.

        Combines:
        - Core identity
        - Current state
        - Relevant memories
        """
        parts = []

        # Core identity
        if bundle.system_identity:
            parts.append(bundle.system_identity)

        # Add persona instruction
        parts.append(f"\nYou are {self._persona_name}. Respond naturally and authentically.")

        # Current state
        if bundle.state_context:
            state_str = self._format_state(bundle.state_context)
            parts.append(f"\n## Current State\n{state_str}")

        # Relevant memories
        if bundle.memory_context:
            mem_str = self._format_memories(bundle.memory_context)
            parts.append(f"\n## Relevant Memories\n{mem_str}")

        return "\n".join(parts)

    def _format_state(self, state: Dict[str, Any]) -> str:
        """Format state dict as readable text."""
        lines = []
        for channel, data in state.items():
            channel_name = channel.replace("bus:", "").capitalize()
            lines.append(f"**{channel_name}:** {data}")
        return "\n".join(lines)

    def _format_memories(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories as readable list."""
        lines = []
        for mem in memories:
            if not isinstance(mem, dict):
                lines.append(f"- {mem}")
                continue

            # Check for episodic memory structure
            summary = mem.get("summary", {})
            if isinstance(summary, dict) and summary.get("content"):
                lines.append(f"- {summary['content']}")
            elif isinstance(summary, str) and summary:
                lines.append(f"- {summary}")
            elif mem.get("content"):
                content = mem["content"]
                excerpt = content[:200] + "..." if len(content) > 200 else content
                lines.append(f"- {excerpt}")
            else:
                # Fallback to subject-predicate-object if semantic
                subj = mem.get("subject")
                pred = mem.get("predicate")
                obj = mem.get("object")
                if subj and pred and obj:
                    lines.append(f"- Recall: {subj} {pred} {obj}")
                else:
                    lines.append(f"- {mem}")

        return "\n".join(lines) if lines else "No relevant memories."
