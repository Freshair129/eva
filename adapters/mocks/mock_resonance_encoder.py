import hashlib
import json
from datetime import datetime
from typing import Dict, Any
from contracts.ports.i_resonance_encoder import IResonanceEncoder


class MockResonanceEncoder(IResonanceEncoder):
    """
    Mock implementation of resonance encoder for Phase 1.

    Does not perform real resonance calculations.
    Returns neutral gray color and 0.5 intensity for all inputs.
    """

    def encode(self, raw_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simple pass-through encoding.
        Real RMS will do color mapping, intensity calculation, etc.
        """
        # Create hash of input for tracking
        raw_hash = hashlib.md5(
            json.dumps(raw_state, sort_keys=True, default=str).encode()
        ).hexdigest()[:8]

        return {
            "encoded_at": datetime.now().isoformat(),
            "resonance_color": "#808080",  # Gray (neutral)
            "intensity": 0.5,              # Neutral intensity
            "valence_color": "#808080",    # Neutral valence
            "arousal_level": 0.5,          # Neutral arousal
            "raw_hash": raw_hash,
            "encoder_version": "mock_v1",
            "source": "mock_resonance_encoder",
        }

    def get_encoder_id(self) -> str:
        return "mock_resonance_encoder_v1"
