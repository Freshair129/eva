"""CIM Engine - Context Injection Manager."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from orchestrator.cim.context_library_loader import ContextLibraryLoader


@dataclass
class ContextBundle:
    """
    Bundle of context to inject into LLM.

    Attributes:
        user_input: The user's message
        system_identity: Core identity prompt
        memory_context: Retrieved memories
        state_context: Current bio/psych state
        timestamp: When bundle was created
    """
    user_input: str
    system_identity: str = ""
    memory_context: List[Any] = field(default_factory=list)
    state_context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class CIMEngine:
    """
    Context Injection Manager.

    Assembles context from multiple sources into a coherent
    bundle for LLM consumption.

    Responsibilities:
    - Gather context from sources
    - Format for LLM consumption
    - Manage context size limits
    """

    def __init__(
        self,
        system_identity: str = "",
        max_memory_items: int = 5,
        max_context_tokens: int = 4000,
        library_path: str = "consciousness"
    ):
        """
        Initialize CIM.

        Args:
            system_identity: Core system prompt (if not using library)
            max_memory_items: Max memories to include
            max_context_tokens: Token budget for context
            library_path: Path to context_library folder
        """
        self._max_memory_items = max_memory_items
        self._max_context_tokens = max_context_tokens
        self._msp = None
        self._bus = None

        # Initialize context library loader
        self._library = ContextLibraryLoader(library_path)

        # Load identity from library or use provided string
        if system_identity:
            self._system_identity = system_identity
        else:
            self._system_identity = self._library.load_identity()

        # Load prompt fragments
        self._prompts = self._library.load_prompts()

    def set_msp(self, msp) -> None:
        """Set MSP reference for memory retrieval."""
        self._msp = msp

    def set_bus(self, bus) -> None:
        """Set Bus reference for state retrieval."""
        self._bus = bus

    def set_system_identity(self, identity: str) -> None:
        """Update system identity prompt."""
        self._system_identity = identity

    def set_gks(self, gks) -> None:
        """Set GKS reference for wisdom retrieval."""
        self._gks = gks

    def build_context(self, user_input: str) -> ContextBundle:
        """
        Build context bundle for given user input.
        Now includes Knowledge (GKS) and Experience (RMS).
        """
        # Start with user input
        bundle = ContextBundle(
            user_input=user_input,
            system_identity=self._system_identity
        )

        # 1. Add Memories (Personal)
        if self._msp:
            try:
                memories = self._msp.semantic_search(user_input, limit=self._max_memory_items)
                bundle.memory_context = [self._format_memory(m) for m in memories]
            except Exception:
                pass

        # 2. Add Knowledge (Wisdom)
        if hasattr(self, "_gks") and self._gks:
             try:
                 knowledge = self._gks.query(user_input)
                 # Inject into state context for now, or new field?
                 # Let's put it in state for generic handling in format_for_llm
                 bundle.state_context["knowledge"] = knowledge
             except Exception:
                 pass

        # 3. Add State (Body, Mind, Perception)
        if self._bus:
            bundle.state_context.update(self._gather_state())
        
        return bundle

    def _format_memory(self, memory: Any) -> Dict[str, Any]:
        """Format a memory for context injection."""
        if hasattr(memory, 'to_dict'):
            return memory.to_dict()
        if isinstance(memory, dict):
            return memory
        return {"content": str(memory)}

    def _gather_state(self) -> Dict[str, Any]:
        """
        Gather current state from bus channels.
        Includes Phase 5 (Qualia) and Phase 4 (Physio).
        """
        state = {}
        if not self._bus:
            return state

        # Get latest from known channels
        channels = ["bus:physical", "bus:psychological", "bus:phenomenological"]
        for channel in channels:
            try:
                latest = self._bus.get_latest(channel)
                if latest:
                    state[channel] = latest
            except Exception:
                pass

        return state

    def format_for_llm(self, bundle: ContextBundle) -> str:
        """
        Format bundle as text for LLM.

        Args:
            bundle: The context bundle

        Returns:
            Formatted string for LLM system prompt
        """
        parts = []

        # System identity
        if bundle.system_identity:
            parts.append(f"# Identity\n{bundle.system_identity}")

        # State context
        if bundle.state_context:
            parts.append("# Current State")
            for channel, data in bundle.state_context.items():
                parts.append(f"## {channel}\n{data}")

        # Memory context
        if bundle.memory_context:
            parts.append("# Relevant Memories")
            for mem in bundle.memory_context:
                # Try to get a summary or content
                content = ""
                if isinstance(mem, dict):
                    # Episodic has summary.content
                    summary = mem.get("summary", {})
                    if isinstance(summary, dict):
                        content = summary.get("content", "")
                    else:
                        content = str(summary)
                    
                    if not content:
                        content = mem.get("content", "")
                
                if not content:
                    content = str(mem)
                
                # Limit length for context
                excerpt = content[:200] + "..." if len(content) > 200 else content
                parts.append(f"- {excerpt}")

        return "\n\n".join(parts)
