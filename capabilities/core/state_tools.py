"""
State Tools - Core cognitive utilities.
Includes H5 Resonance Codec for state compression.
"""

from typing import Dict, Any, Union

class H5ResonanceCodec:
    """
    Implements the H5 Resonance Compression Protocol (ADR-007).
    
    Format: [H5-{RI}{Stress}{Social}{Drive}{Clarity}{Joy}]
    Encoding: 0.XX -> XX, 1.0 -> M
    """

    # Keys expected in the input state dictionary
    KEYS = [
        "resonance_index",  # RI
        "stress_load",      # Stress
        "social_warmth",    # Social
        "drive_level",      # Drive
        "cognitive_clarity",# Clarity
        "joy_level"         # Joy
    ]

    @staticmethod
    def encode(state: Dict[str, float]) -> str:
        """
        Encode state dictionary into H5 string.
        
        Args:
            state: Dictionary containing float values (0.0-1.0) for:
                   resonance_index, stress_load, social_warmth, 
                   drive_level, cognitive_clarity, joy_level.
                   
        Returns:
            Formatted string: [H5-4555M625750]
        """
        parts = []
        
        for key in H5ResonanceCodec.KEYS:
            value = state.get(key, 0.0)
            parts.append(H5ResonanceCodec._encode_value(value))
            
        return f"[H5-{''.join(parts)}]"

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
    return H5ResonanceCodec.encode(state)
