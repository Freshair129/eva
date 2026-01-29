"""
Verify Perception - RMS End-to-End Test.
Tests the conversion of Physio-Psych state into Resonance and Qualia.
"""
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.simple_bus import SimpleBus
from rms.system import RMSSystem

def test_perception():
    print("=" * 60)
    print("EVA Genesis - Perception (RMS) Verification")
    print("=" * 60)
    
    # 1. Setup
    bus = SimpleBus()
    rms = RMSSystem(bus=bus)
    
    # Subscribe to output to monitor
    received_qualia = []
    def on_phenom_signal(payload):
        print(f"\n[BUS] Received Phenomenological Update")
        received_qualia.append(payload)
        
    bus.subscribe("bus:phenomenological", on_phenom_signal)
    
    # 2. Inject Physical State (High Adrenaline)
    print("\n[2] Injecting Physical State (High Adrenaline)...")
    bus.publish("bus:physical", {
        "hormones": {"adrenaline": 0.8, "cortisol": 0.5},
        "heart_rate": 120
    })
    
    # 3. Inject Psychological State (High Stress)
    print("\n[3] Injecting Psychological State (High Stress)...")
    bus.publish("bus:psychological", {
        "axes_9d": {
            "stress": 0.9,
            "warmth": 0.2,
            "clarity": 0.3,
            "drive": 0.8,
            "joy": 0.1,
            "stability": 0.4,
            "orientation": 0.5
        }
    })
    
    # RMS processes on receipt. Let's inspect the latest state.
    state = rms.get_current_state()
    res = state.get("resonance", {})
    qualia = state.get("qualia", {})
    
    print("\n[4] Inspecting RMS Output:")
    print(f"   - E9 Code: {res.get('resonance_code')}")
    print(f"   - Intensity: {res.get('intensity')}")
    print(f"   - Coherence: {res.get('coherence')} (Alignment Check)")
    
    print("\n   [Qualia Check]")
    print(f"   - Narrative: \"{qualia.get('narrative')}\"")
    print(f"   - Texture: {qualia.get('texture')}")
    print(f"   - Temperature: {qualia.get('temperature')}")
    
    # Assertions
    # 1. E9 Code should exist
    assert res.get('resonance_code').startswith("[E9-")
    
    # 2. Narrative should reflect Adrenaline/Stress
    narrative = qualia.get('narrative', "")
    assert "Heart pounding" in narrative or "razor point" in narrative
    
    # 3. Texture should be "Jagged" or "Vibrating" due to high stress/drive
    texture = qualia.get('texture', "")
    assert "Jagged" in texture or "Vibrating" in texture
    
    # 4. Bus should have fired
    if len(received_qualia) > 0:
        print(f"\n   [OK] Bus received {len(received_qualia)} updates")
    else:
        print("\n   [FAIL] No signals received on bus")
        return False

    return True

if __name__ == "__main__":
    if test_perception():
        print("\n>>> PERCEPTION TESTS PASSED <<<")
    else:
        print("\n>>> PERCEPTION TESTS FAILED <<<")
        sys.exit(1)
