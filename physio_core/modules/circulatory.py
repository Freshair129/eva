"""
Circulatory System - The Heartbeat of EVA.
Manages the update loop (30Hz), distribution of metabolic resources,
and the 'Bio-Digital Gap' calculation.
"""

import time
import threading
import logging
from typing import Dict, Any, Callable
from .hormone_glands import HormoneGlands
from ..parameters import TICK_RATE_HZ, SEC_PER_TICK

logger = logging.getLogger(__name__)

class CirculatorySystem:
    """
    Simulates the bloodstream and heartbeat.
    Owns the HormoneGlands and manages their update cycle.
    """
    
    def __init__(self):
        self.hormones = HormoneGlands()
        self.heart_rate = 60  # BPM (Basal)
        self.metabolic_rate = 1.0  # Multiplier for energy usage
        self._stop_event = threading.Event()
        self._callbacks = []
        
    def add_hormone(self, name: str, amount: float):
        """Injects hormone into bloodstream."""
        self.hormones.secrete(name, amount)
        # Adrenaline spikes increase heart rate immediately
        if name == "adrenaline":
            self.heart_rate = min(180, self.heart_rate + (amount * 50))
            
    def get_state(self) -> Dict[str, Any]:
        """Returns snapshot of circulatory state."""
        return {
            "heart_rate": int(self.heart_rate),
            "metabolic_rate": round(self.metabolic_rate, 2),
            "hormones": self.hormones.get_levels()
        }

    def calculate_bio_gap(self) -> float:
        """
        Calculates the Bio-Digital Gap (latency in seconds).
        High arousal/adrenaline = Lower gap (Quick reaction)
        Low arousal/groggy = Higher gap (Slow reaction)
        """
        levels = self.hormones.get_levels()
        adrenaline = levels.get("adrenaline", 0.2)
        cortisol = levels.get("cortisol", 0.3)
        acetylcholine = levels.get("acetylcholine", 0.5)
        
        # Base latency: 100ms
        gap_ms = 100.0
        
        # Modifiers
        # High adrenaline reduces gap (Fast twitch) - up to 40ms reduction
        gap_ms -= (adrenaline * 40)
        
        # High acetylcholine optimizes gap (Focus) - up to 20ms reduction
        gap_ms -= (acetylcholine * 20)
        
        # High cortisol increases gap (Scatterbrained/Frozen) - up to 50ms penalty
        if cortisol > 0.7:
            gap_ms += ((cortisol - 0.7) * 100)
            
        return max(10.0, gap_ms) / 1000.0  # Return in seconds

    def update(self, delta_seconds: float = 1.0):
        """
        Main update method (Tick).
        delta_seconds: How much virtual time to simulate
        """
        # Calculate ticks to process based on TICK_RATE_HZ
        # e.g. delta 1.0 sec = 30 ticks
        ticks = int(delta_seconds * TICK_RATE_HZ)
        if ticks > 0:
            self.hormones.metabolize(ticks)
            
            # Decay heart rate back to 60
            if self.heart_rate > 60:
                # Decay 1 BPM per second approx
                self.heart_rate = max(60, self.heart_rate - (1.0 * delta_seconds))
            elif self.heart_rate < 60:
                self.heart_rate = min(60, self.heart_rate + (0.5 * delta_seconds))
