"""
RMS System - The Perception Controller.
Aggregates Physical and Psychological state into Phenomenological Experience.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from contracts.ports.i_state_provider import IStateProvider
from .modules.resonance_encoder import ResonanceEncoder
from .modules.qualia_engine import QualiaEngine

logger = logging.getLogger(__name__)

class RMSSystem(IStateProvider):
    """
    The Authority for Phenomenological State (Qualia).
    Listens to Body/Mind updates and synthesizes the 'Subjective Experience'.
    """
    
    def __init__(self, bus=None):
        self.bus = bus
        self.encoder = ResonanceEncoder()
        self.qualia_engine = QualiaEngine()
        
        # Local cache of inputs
        self.current_inputs = {
            "physical": {},
            "psychological": {}
        }
        
        # Current output state
        self.current_state = {
            "resonance": {},
            "qualia": {}
        }
        
        # Wire up bus listeners
        if self.bus:
            self.bus.subscribe("bus:physical", self._on_physical_update)
            self.bus.subscribe("bus:psychological", self._on_psychological_update)
            
        logger.info("[RMS] System Initialized (Resonance & Qualia)")

    def get_provider_id(self) -> str:
        return "rms_perception"

    def get_state_type(self) -> str:
        return "phenomenological"

    def get_current_state(self) -> Dict[str, Any]:
        """Returns the current subjective experience."""
        # Ensure we have a timestamp
        self.current_state["timestamp"] = datetime.now(timezone.utc).isoformat()
        return self.current_state

    def _on_physical_update(self, payload: Dict[str, Any]):
        """Handler for body state updates."""
        # Merge or replace? For now, replace relevant sections.
        # Payload might be partial (e.g. stimulus response) or full state.
        # If it has hormonal impact, we update our View of the Body.
        
        # Strategy: Keep latest known state of body
        if "state_snapshot" in payload:
            self.current_inputs["physical"] = payload["state_snapshot"]
        elif "hormones" in payload: # Direct hormone update
             # Try to merge into existing
             if "hormones" not in self.current_inputs["physical"]:
                 self.current_inputs["physical"]["hormones"] = {}
             self.current_inputs["physical"]["hormones"].update(payload["hormones"])
             
        self._process_perceptual_frame()

    def _on_psychological_update(self, payload: Dict[str, Any]):
        """Handler for mind state updates."""
        # Typically full state broadcast
        if "axes_9d" in payload:
             self.current_inputs["psychological"] = payload
        elif "emotions" in payload:
             self.current_inputs["psychological"] = payload.get("emotions", {})
             
        self._process_perceptual_frame()

    def _process_perceptual_frame(self):
        """
        Synthesizes the current inputs into a new Phenomenological Frame.
        Called whenever inputs change.
        """
        # 1. Prepare combined state for encoder
        state_for_encoding = {
            "physical": self.current_inputs.get("physical", {}),
            "psychological": self.current_inputs.get("psychological", {})
        }
        
        # 2. Encode Resonance
        try:
            resonance_obj = self.encoder.encode(state_for_encoding)
            
            # 3. Generate Qualia
            qualia_obj = self.qualia_engine.generate_qualia(resonance_obj)
            
            # 4. Update Current State
            self.current_state = {
                "resonance": resonance_obj,
                "qualia": qualia_obj,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # 5. Publish to Bus
            if self.bus:
                self.bus.publish("bus:phenomenological", self.current_state)
                
        except Exception as e:
            logger.error(f"[RMS] Error processing frame: {e}")
            # Don't crash, just log.
