"""Verification script for H5 Resonance Codec (P3-002)."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from capabilities.core.state_tools import compress_state, H5ResonanceCodec

def verify_h5_codec():
    print("Verifying H5 Resonance Codec...\n")
    
    # Test Case 1: Standard Values
    state1 = {
        "resonance_index": 0.45,
        "stress_load": 0.55,
        "social_warmth": 1.0,  # Should become M
        "drive_level": 0.62,
        "cognitive_clarity": 0.57,
        "joy_level": 0.50
    }
    encoded1 = compress_state(state1)
    print(f"Case 1 (Standard): {state1} -> {encoded1}")
    expected1 = "[H5-4555M625750]"
    assert encoded1 == expected1, f"Expected {expected1}, got {encoded1}"

    # Test Case 2: Clamping and Routing
    state2 = {
        "resonance_index": 1.5,   # Should cap to M
        "stress_load": -0.5,      # Should clamp to 00
        "social_warmth": 0.9999,  # Should be M
        "drive_level": 0.001,     # Should be 00
        # Missing keys should default to 0.0
    }
    encoded2 = compress_state(state2)
    print(f"Case 2 (Edge/Default): {state2} -> {encoded2}")
    # RI=M, Stress=00, Social=M, Drive=00, Clarity=00, Joy=00
    expected2 = "[H5-M00M000000]" 
    assert encoded2 == expected2, f"Expected {expected2}, got {encoded2}"
    
    # Test Case 3: Exact values
    state3 = {
        "resonance_index": 0.12,
        "stress_load": 0.34,
        "social_warmth": 0.56,
        "drive_level": 0.78,
        "cognitive_clarity": 0.90,
        "joy_level": 0.00
    }
    encoded3 = compress_state(state3)
    print(f"Case 3 (Exact): {state3} -> {encoded3}")
    expected3 = "[H5-123456789000]"
    assert encoded3 == expected3, f"Expected {expected3}, got {encoded3}"

    print("\n[PASS] H5 Codec verification successful!")

if __name__ == "__main__":
    verify_h5_codec()
