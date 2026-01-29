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
        Injects hormones based on STIMULUS_MAP.
        """
        self.update()
        
        impact = STIMULUS_MAP.get(stimulus_type)
        if impact:
            # Scale impact by intensity
            real_impact = {h: val * intensity for h, val in impact.items()}
            
            # Use CirculatorySystem to inject hormones (triggers heart rate, etc.)
            for hormone, amount in real_impact.items():
                self.circulatory.add_hormone(hormone, amount)
            
            # Publish reaction to bus
            if self.bus:
                self.bus.publish("bus:physical", {
                    "signal_type": "hormone_response",
                    "trigger": stimulus_type,
                    "impact": real_impact,
                    "state_snapshot": self.circulatory.get_state()
                })
            
            return real_impact
        # If unknown stimulus, generic response?
        return {}

    def get_bio_digital_gap(self) -> float:
        """Returns the current pause duration (seconds) required for biological realism."""
        self.update()
        return self.circulatory.calculate_bio_gap()
