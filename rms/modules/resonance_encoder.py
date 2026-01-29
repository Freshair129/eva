"""
Resonance Encoder - State Compression Logic.
Wraps the E9 Protocol and calculates additional resonance metadata.
"""

from typing import Dict, Any, Tuple
from capabilities.core.state_tools import E9ResonanceCodec

class ResonanceEncoder:
    """
    Responsible for converting raw state dictionaries into
    Standardized Resonance Objects.
    """
    
    def __init__(self):
        self.codec = E9ResonanceCodec()

    def encode(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encodes full state into a resonance object.
        
        Input state expected to contain:
        - psychological (axes_9d)
        - physical (hormones)
        
        Returns:
            {
                "resonance_code": "[E9-...]",
                "intensity": float,
                "coherence": float,
                "timestamp": str
            }
        """
        psych = state.get("psychological", {})
        physio = state.get("physical", {})
        hormones = physio.get("hormones", {})
        axes = psych.get("axes_9d", {})
        
        # 1. Flatten for E9 Codec
        # We need to map available state to E9 keys
        # E9 Keys: resonance_index, stress_load, social_warmth, drive_level, 
        #          cognitive_clarity, joy_level, stability, orientation, 
        #          momentum_intensity, reflex_urgency
        
        flat_state = {
            # Direct mapping from Psych Axes
            "stress_load": axes.get("stress", 0.5),
            "social_warmth": axes.get("warmth", 0.5),
            "drive_level": axes.get("drive", 0.5),
            "cognitive_clarity": axes.get("clarity", 0.5),
            "joy_level": axes.get("joy", 0.5),
            "stability": axes.get("stability", 0.5),
            "orientation": axes.get("orientation", 0.5),
            
            # Derived from Physio/Psych
            "momentum_intensity": psych.get("momentum", {}).get("intensity", 0.1),
            "reflex_urgency": hormones.get("adrenaline", 0.2), # Adrenaline drives urgency
            
            # Resonance Index (RI) - The "Vibe"
            # Calculated as average of high-arousal axes
            "resonance_index": (axes.get("joy", 0.5) + axes.get("stress", 0.5) + axes.get("drive", 0.5)) / 3.0
        }
        
        # 2. Generate Code
        code = self.codec.encode(flat_state)
        
        # 3. Calculate Metadata
        intensity = self._calculate_intensity(flat_state)
        coherence = self._calculate_coherence(axes, hormones)
        
        return {
            "resonance_code": code,
            "intensity": round(intensity, 2),
            "coherence": round(coherence, 2),
            "source_snapshot": {
                "psych": flat_state,
                # Keep full hormone list for qualia engine if needed
                "hormones": hormones
            }
        }

    def _calculate_intensity(self, state: Dict[str, float]) -> float:
        """Calculates global intensity (how 'strong' is the feeling)."""
        # RMS of deviations from neutral (0.5)
        sum_sq = 0.0
        count = 0
        for k, v in state.items():
            diff = v - 0.5
            sum_sq += diff * diff
            count += 1
        return (sum_sq / count) ** 0.5 * 2.0 # Scale to roughly 0-1

    def _calculate_coherence(self, axes: Dict[str, float], hormones: Dict[str, float]) -> float:
        """
        Calculates body-mind alignment (Coherence).
        e.g. High Stress (Psych) should match High Cortisol (Body).
        """
        # Simple heuristic: Check Stress vs Cortisol
        psych_stress = axes.get("stress", 0.5)
        bio_stress = hormones.get("cortisol", 0.3) # Baseline 0.3
        
        # Normalize bio_stress to 0-1 range approx (0.3 -> 0.0, 1.0 -> 1.0)
        norm_bio = (bio_stress - 0.3) / 0.7
        norm_bio = max(0.0, min(1.0, norm_bio))
        
        diff = abs(psych_stress - norm_bio)
        return 1.0 - diff # 1.0 = Perfect alignment
