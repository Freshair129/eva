from abc import ABC, abstractmethod
from typing import Dict, Any

class IResonanceEncoder(ABC):
    """
    Port interface for resonance encoding.

    Converts raw system state into resonance-formatted data
    with color mapping, intensity calculation, etc.

    Implementors:
    - MockResonanceEncoder (Phase 1)
    - RMSEngine (Phase 5)
    """

    @abstractmethod
    def encode(self, raw_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encodes raw state into resonance format.

        Args:
            raw_state: Raw state from any IStateProvider

        Returns:
            Dict containing:
            - encoded_at: ISO timestamp
            - resonance_color: Hex color string
            - intensity: Float 0.0-1.0
            - raw_hash: Short hash of input
        """
        pass

    @abstractmethod
    def get_encoder_id(self) -> str:
        """Returns unique identifier for this encoder."""
        pass
