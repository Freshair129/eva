"""
Verify PhysioCore - End-to-End Biological Test.
Tests the PhysioSystem, Bus Integration, and Bio-Digital Gap.
"""
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.simple_bus import SimpleBus
from physio_core.system import PhysioSystem

def test_physio_core():
    print("=" * 60)
    print("EVA Genesis - PhysioCore Verification")
    print("=" * 60)
    
    # 1. Setup
    bus = SimpleBus()
    physio = PhysioSystem(bus=bus)
    
    # Subscribe to bus to monitor output
    received_signals = []
    def on_physical_signal(payload):
        print(f"\n[BUS] Received {payload.get('signal_type')} from {payload.get('trigger', 'unknown')}")
        received_signals.append(payload)
        
    bus.subscribe("bus:physical", on_physical_signal)
    
    print("\n[1] Initial State:")
    state = physio.get_current_state()
    # Updated to print hormone levels nicely
    hormones = state['hormones']
    for h in ['dopamine', 'cortisol', 'adrenaline']:
         print(f"   - {h}: {hormones.get(h, 0.0):.2f}")
    
    print(f"   - Heart Rate: {state['heart_rate']} bpm")
    print(f"   - Bio Gap: {state['bio_gap_seconds'] * 1000:.1f} ms")
    
    # 2. Inject Stimulus: THREAT
    print("\n[2] Injecting Stimulus: 'threat' (Adrenaline Spike)...")
    physio.process_stimulus("threat", intensity=1.0)
    
    # Check immediate reaction
    state = physio.get_current_state()
    print(f"   - Adrenaline: {state['hormones']['adrenaline']:.2f} (Expected spike)")
    print(f"   - Heart Rate: {state['heart_rate']} bpm (Expected increase)")
    print(f"   - Bio Gap: {state['bio_gap_seconds'] * 1000:.1f} ms (Expected decrease due to adrenaline)")
    
    assert state['hormones']['adrenaline'] > 0.4
    assert state['heart_rate'] > 70
    assert state['bio_gap_seconds'] < 0.1 # < 100ms
    
    # 3. Time Decay (Metabolism)
    print("\n[3] Simulating Time Decay (10 Seconds)...")
    # Simulate 10 seconds of updates
    # We call update manually with delta to simulate time passing faster than real time for test
    physio.circulatory.update(delta_seconds=10.0)
    
    state = physio.get_current_state()
    print(f"   - Adrenaline: {state['hormones']['adrenaline']:.2f} (Expected decay)")
    print(f"   - Heart Rate: {state['heart_rate']} bpm (Expected decay towards 60)")
    
    assert state['hormones']['adrenaline'] < 0.6 # Should have decayed somewhat
    assert state['heart_rate'] < 150 # Should have dropped
    
    # 4. Bus Verification
    print("\n[4] verifying Bus Signals...")
    if len(received_signals) > 0:
        print(f"   [OK] Bus received {len(received_signals)} signals")
        last = received_signals[-1]
        print(f"   Last Signal: {last.get('trigger')} -> {last.get('impact')}")
    else:
        print("   [FAIL] No signals received on bus")
        return False
        
    return True

if __name__ == "__main__":
    if test_physio_core():
        print("\n>>> PHYSIO CORE TESTS PASSED <<<")
    else:
        print("\n>>> PHYSIO CORE TESTS FAILED <<<")
        sys.exit(1)
