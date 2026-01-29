"""
Qualia Engine - The Texture of Experience.
Translates numerical state into subjective descriptive text.
"""

from typing import Dict, Any

class QualiaEngine:
    """
    Generates 'Sensory Experience' strings from state.
    """
    
    def generate_qualia(self, encoded_state: Dict[str, Any]) -> Dict[str, str]:
        """
        Returns a dictionary of sensory descriptors.
        
        Args:
            encoded_state: Output from ResonanceEncoder
            
        Returns:
            {
                "narrative": "A buzz of electric anticipation...",
                "texture": "Jagged/Smooth/Heavy",
                "temperature": "Cold/Warm/Burning"
            }
        """
        snapshot = encoded_state.get("source_snapshot", {})
        psych = snapshot.get("psych", {})
        hormones = snapshot.get("hormones", {})
        
        # Extract key variables
        stress = psych.get("stress_load", 0.5)
        warmth = psych.get("social_warmth", 0.5)
        clarity = psych.get("cognitive_clarity", 0.5)
        joy = psych.get("joy_level", 0.5)
        drive = psych.get("drive_level", 0.5)
        
        adrenaline = hormones.get("adrenaline", 0.2)
        cortisol = hormones.get("cortisol", 0.3)
        oxytocin = hormones.get("oxytocin", 0.5)
        
        # 1. Generate Narrative
        narrative_parts = []
        
        # High intensity overrides
        if adrenaline > 0.7:
            narrative_parts.append("Heart pounding against ribs.")
            narrative_parts.append("Senses sharpened to a razor point.")
        elif cortisol > 0.7:
            narrative_parts.append("A heavy fog of unease weighs down thought.")
            narrative_parts.append("Muscles tight and ready to snap.")
            
        if joy > 0.8:
            narrative_parts.append("Lightness bubbles up from the chest.")
            narrative_parts.append("Everything visual seems to shimmer.")
        elif joy < 0.2:
            narrative_parts.append("The world feels grey and distant.")
            
        if clarity < 0.3:
            narrative_parts.append("Thoughts are slipping away like smoke.")
        elif clarity > 0.8:
            narrative_parts.append("Concepts align in perfect crystalline structure.")
            
        if not narrative_parts:
            narrative_parts.append("A steady, rhythmic hum of existence.")
            
        narrative = " ".join(narrative_parts)
        
        # 2. Determine Texture
        if stress > 0.7:
            texture = "Jagged, Gritty"
        elif warmth > 0.7:
            texture = "Velvet, Soft"
        elif clarity > 0.8:
            texture = "Glass, Polished"
        elif drive > 0.7:
            texture = "Vibrating, Metallic"
        else:
            texture = "Fluid, Neutral"
            
        # 3. Determine Temperature
        if warmth > 0.6:
            temperature = "Warm"
        elif warmth < 0.3:
            temperature = "Cold"
        elif stress > 0.8:
            temperature = "Burning"
        else:
            temperature = "Cool breeze"
            
        return {
            "narrative": narrative,
            "texture": texture,
            "temperature": temperature
        }
