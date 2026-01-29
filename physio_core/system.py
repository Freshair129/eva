"""
PhysioSystem - The 'Body' Controller.
Implements IStateProvider interface to expose biological state.
Connects Circulatory System to the Event Bus.
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from contracts.ports.i_state_provider import IStateProvider
from .modules.circulatory import CirculatorySystem
from .parameters import STIMULUS_MAP

logger = logging.getLogger(__name__)

class PhysioSystem(IStateProvider):
    """
    The main interface for the Biological Subsystem.
    Manages the 30Hz Simulation Loop and Bus Integration.
    """
    
    def __init__(self, bus=None):
        self.circulatory = CirculatorySystem()
        self.bus = bus
        self._last_update = time.time()
        logger.info("[PhysioCore] System Initialized (12 Hormones, 30Hz Heartbeat)")

    def get_provider_id(self) -> str:
        return "physio_core"

    def get_state_type(self) -> str:
        return "physical"

    def get_current_state(self) -> Dict[str, Any]:
        """
        Implementation of IStateProvider.
        Returns full snapshot of biological state.
        """
        # Ensure state is up-to-date
        self.update()
        
        state = self.circulatory.get_state()
        state["timestamp"] = datetime.now(timezone.utc).isoformat()
        state["bio_gap_seconds"] = self.circulatory.calculate_bio_gap()
        return state

    def update(self):
        """
        Advances the simulation based on real time elapsed.
        Should be called before reading state or processing input.
        """
        now = time.time()
        delta = now - self._last_update
        
        # Limit max delta to avoid huge jumps if system was sleeping
        delta = min(delta, 10.0)
        
        if delta > 0.01: # 10ms minimum step
            self.circulatory.update(delta)
            self._last_update = now
            
            # Publish heartbeat to bus if wired
            # (In production, maybe only publish significant changes)
            if self.bus:
                 # TODO: Optimize to not spam bus at 30Hz
                 pass

    def process_stimulus(self, stimulus_type: str, intensity: float = 1.0) -> Dict[str, float]:
        """
        Reacts to an external stimulus (e.g. 'threat', 'praise').
        Injects hormones based on STIMULUS_MAP and Reflex Configs.
        """
        self.update()
        
        impact = {}
        
        # 1. Check Standard Stimulus Map (Synthesis)
        # Parameters loaded from hormone_spec_ml.yaml
        # exact match check
        if stimulus_type in STIMULUS_MAP:
            for hormone, val in STIMULUS_MAP[stimulus_type].items():
                impact[hormone] = val * intensity

        # 2. Check Reflex Paths (Fast Path)
        # Loaded from PhysioCore_configs.yaml
        from .parameters import SYSTEM_CONFIG
        reflexes = SYSTEM_CONFIG.get("subsystems", {}).get("reflex", {}).get("pathway_mapping", [])
        
        for reflex in reflexes:
            if reflex.get("stimulus_type") == stimulus_type:
                # Target receptor usually ESC_Hxx_NAME, we need the simple name
                target = reflex.get("target_receptor", "")
                # Extract simple name if possible, or use map
                # E.g. ESC_H01_ADRENALINE -> adrenaline
                # We need a map from ESC ID to simple name.
                # For now, let's just crude parse or look it up.
                simple_name = self._resolve_hormone_name(target)
                gain = reflex.get("gain_modifier", 1.0)
                
                if simple_name:
                    current = impact.get(simple_name, 0.0)
                    impact[simple_name] = current + (gain * intensity)

        if impact:
            # Use CirculatorySystem to inject hormones (triggers heart rate, etc.)
            for hormone, amount in impact.items():
                self.circulatory.add_hormone(hormone, amount)
            
                self.bus.publish("bus:physical", {
                    "signal_type": "hormone_response",
                    "trigger": stimulus_type,
                    "impact": impact,
                    "state_snapshot": self.circulatory.get_state()
                })
            
            return impact
        # If unknown stimulus, generic response?
        return {}

    def _resolve_hormone_name(self, esc_id: str) -> Optional[str]:
        """Helper: Maps ESC_H01_ADRENALINE -> adrenaline"""
        # Simple heuristic: Split by underscore and take last part?
        # ESC_H01_ADRENALINE -> ADRENALINE. Lowercase -> adrenaline.
        # ESC_N02_DOPAMINE -> dopamine
        if not esc_id: return None
        parts = esc_id.split("_")
        if len(parts) >= 3:
            return parts[-1].lower()
        return None

    def get_bio_digital_gap(self) -> float:
        """Returns the current pause duration (seconds) required for biological realism."""
        self.update()
        return self.circulatory.calculate_bio_gap()
