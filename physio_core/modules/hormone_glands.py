"""
Hormone Glands - Endocrine System Logic.
Handles the secretion and regulation of 12 key simulated hormones.
"""

import math
from typing import Dict, Any
from ..parameters import BASELINES, HALF_LIVES, TICK_RATE_HZ

class HormoneGlands:
    """
    Simulates the synthesis and release of horomones.
    Manages the 'chemical soup' of the bot.
    """
    
    def __init__(self):
        # Initialize current values to baseline
        self.current_levels = BASELINES.copy()
        
        # Precompute decay factors per tick
        # Formula: N(t) = N0 * (1/2)^(t/t_half)
        # Factor = (0.5)^(1 / (t_half * HZ))
        self.decay_factors = {}
        for hormone, half_life_sec in HALF_LIVES.items():
            # Ensure half_life is not zero to avoid division error
            hl = max(half_life_sec, 1.0)
            self.decay_factors[hormone] = math.pow(0.5, 1.0 / (hl * TICK_RATE_HZ))

    def secrete(self, hormone: str, amount: float):
        """
        Releases a hormone into the system (spike).
        Value is clamped to max 1.0.
        """
        if hormone in self.current_levels:
            self.current_levels[hormone] = min(1.0, self.current_levels[hormone] + amount)

    def metabolize(self, ticks: int = 1):
        """
        Applies decay (homeostasis) for N ticks.
        Hormones decay towards their BASELINE, not zero.
        """
        for _ in range(ticks):
            for h, current in self.current_levels.items():
                baseline = BASELINES.get(h, 0.5)
                decay = self.decay_factors.get(h, 0.99)
                
                if current > baseline:
                    # Decay down to baseline
                    new_val = baseline + (current - baseline) * decay
                    self.current_levels[h] = max(baseline, new_val)
                elif current < baseline:
                    # Recover up to baseline (inverse decay)
                    # We treat recovery same speed as decay for simplicity
                    new_val = baseline - (baseline - current) * decay
                    self.current_levels[h] = min(baseline, new_val)

    def get_levels(self) -> Dict[str, float]:
        """Returns current hormone levels."""
        return self.current_levels.copy()

    def process_stimulus_impact(self, impact: Dict[str, float]):
        """
        Applies a dictionary of hormone impacts.
        e.g. {"dopamine": 0.1, "cortisol": 0.05}
        """
        for hormone, amount in impact.items():
            self.secrete(hormone, amount)
