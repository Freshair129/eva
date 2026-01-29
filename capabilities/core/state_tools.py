"""
State Tools - Core cognitive utilities.
Includes H5 Resonance Codec for state compression.
"""

from typing import Dict, Any, Union

class H9ResonanceCodec:
    """
    Implements the H9 Resonance Compression Protocol (ADR-007).
    
    Format: [H9-{RI}{Str}{War}{Dri}{Cla}{Joy}{Sta}{Ori}{Mom}]
    Encoding: 0.XX -> XX, 1.0 -> M
    """

    # Keys expected in the input state dictionary
    KEYS = [
        "resonance_index",  # RI
        "stress_load",      # Stress
        "social_warmth",    # Warmth
        "drive_level",      # Drive
        "cognitive_clarity",# Clarity
        "joy_level",        # Joy
        "stability",        # Stability (Meta)
        "orientation",      # Orientation (Meta)
        "momentum_intensity"# Momentum
    ]

    @staticmethod
    def encode(state: Dict[str, float]) -> str:
        """
        Encode state dictionary into H9 string.
        
        Args:
            state: Dictionary containing float values (0.0-1.0) for 9 keys.
                   
        Returns:
            Formatted string: [H9-4555M625750806015]
        """
        parts = []
        
        for key in H9ResonanceCodec.KEYS:
            value = state.get(key, 0.0)
            parts.append(H9ResonanceCodec._encode_value(value))
            
        return f"[H9-{''.join(parts)}]"

    @staticmethod
    def _encode_value(value: Union[float, int]) -> str:
        """Encode a single float value to 2-char string or 'M'."""
        # Clamp to 0.0 - 1.0
        val = max(0.0, min(1.0, float(value)))
        
        # Handle Max case
        if val >= 0.999: # Allow small epsilon
            return "M"
            
        # Convert to 2 digits
        # 0.45 -> 45
        digits = int(round(val * 100))
        return f"{digits:02d}"

def compress_state(state: Dict[str, float]) -> str:
    """Public tool function to compress state."""
    return H9ResonanceCodec.encode(state)
