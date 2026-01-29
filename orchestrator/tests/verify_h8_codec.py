"""Verification script for H9 Resonance Codec (P3-002)."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from capabilities.core.state_tools import compress_state

def verify_h8_codec():
    print("Verifying H8 Resonance Codec...\n")
    
    # Test Case 1: Standard 9D Vector
    state1 = {
        "resonance_index": 0.45,
        "stress_load": 0.55,
        "social_warmth": 1.0,  # M
        "drive_level": 0.62,
        "cognitive_clarity": 0.57,
        "joy_level": 0.50,
        "stability": 0.80,
        "orientation": 0.60,
        "momentum_intensity": 0.15
    }
    encoded1 = compress_state(state1)
    print(f"Case 1 (Standard): {state1} -> {encoded1}")
    expected1 = "[H8-4555M625750806015]"
    assert encoded1 == expected1, f"Expected {expected1}, got {encoded1}"

    # Test Case 2: Defaults
    state2 = {} # All zero
    encoded2 = compress_state(state2)
    print(f"Case 2 (Empty): -> {encoded2}")
    expected2 = "[H8-000000000000000000]"
    assert encoded2 == expected2, f"Expected {expected2}, got {encoded2}"

    print("\n[PASS] H8 Codec verification successful!")

if __name__ == "__main__":
    verify_h8_codec()
