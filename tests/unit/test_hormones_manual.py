"""
Verify Hormone Logic - Spikes and Decay.
"""
import sys
import os
sys.path.append(os.getcwd())

from physio_core.modules.hormone_glands import HormoneGlands

def test_hormones():
    print("Testing Hormone Glands...")
    glands = HormoneGlands()
    
    # 1. Check Baselines
    levels = glands.get_levels()
    print(f"Initial Dopamine: {levels['dopamine']} (Expected 0.5)")
    assert levels['dopamine'] == 0.5
    
    # 2. Test Secretion
    print("\nSecreting 0.3 Dopamine...")
    glands.secrete("dopamine", 0.3)
    levels = glands.get_levels()
    print(f"New Dopamine: {levels['dopamine']} (Expected 0.8)")
    assert abs(levels['dopamine'] - 0.8) < 0.001
    
    # 3. Test Decay (10 ticks)
    # Half-life of dopamine is 300 ticks (5 mins at 1Hz, but we assume 30Hz in parameters)
    # Wait, parameters say 300 seconds * 30 Hz = 9000 ticks.
    # Let's check parameters.py.
    # HALF_LIVES["dopamine"] = 300 (which is seconds).
    # Tick rate = 30.
    # Decay factor per tick = 0.5 ^ (1 / (300*30)) ~= 0.99992
    # So 1 tick decay is tiny.
    
    print("\nSimulating 9000 ticks (5 mins - One half-life)...")
    glands.metabolize(ticks=30 * 300) # 300 seconds
    
    levels = glands.get_levels()
    # Baseline is 0.5. Started at 0.8. Excess is 0.3.
    # After half-life, excess should be 0.15. Total should be 0.65.
    print(f"Decayed Dopamine: {levels['dopamine']:.4f} (Expected approx 0.65)")
    assert 0.64 < levels['dopamine'] < 0.66
    
    print("\n>>> Hormone Tests Passed <<<")

if __name__ == "__main__":
    test_hormones()
