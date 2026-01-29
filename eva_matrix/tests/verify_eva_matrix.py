"""Verification script for EVA Matrix (P3-004)."""

import sys
import os
import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from eva_matrix.system import EVAMatrixSystem
from contracts.ports.i_bus import IBus

class MockBus(IBus):
    def __init__(self):
        self.published = []
        self.subscribers = {}

    def publish(self, channel: str, payload: dict) -> None:
        print(f"[Bus] Published to {channel}: {payload.keys()}")
        self.published.append((channel, payload))
        # Trigger subscribers
        if channel in self.subscribers:
            for handler in self.subscribers[channel]:
                handler(payload)

    def subscribe(self, channel: str, handler) -> None:
        print(f"[Bus] Subscribed to {channel}")
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(handler)
        
    def get_latest(self, channel: str):
        return None
        
    def list_channels(self):
        return list(self.subscribers.keys())
        
    def unsubscribe(self, channel: str, handler) -> None:
        pass

def verify_eva_matrix():
    print("Verifying EVA Matrix System...\n")
    
    # 1. Setup Test Environment
    test_dir = Path("test_eva_matrix_env")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    # Copy configs to test dir
    config_dir = test_dir / "eva_matrix/configs"
    config_dir.mkdir(parents=True)
    src_config = Path("eva_matrix/configs/EVA_Matrix_configs.yaml")
    shutil.copy(src_config, config_dir / "EVA_Matrix_configs.yaml")
    
    # 2. Initialize System
    mock_bus = MockBus()
    matrix = EVAMatrixSystem(base_path=test_dir, bus=mock_bus)
    
    # Check Initial State
    print(f"Initial Stress: {matrix.axes_9d['stress']}")
    assert matrix.axes_9d['stress'] == 0.5, "Initial stress should be 0.5"
    
    # 3. Simulate Physical Stimulus (Adrenaline Surge)
    print("\nSimulating Adrenaline Surge...")
    payload = {
        "hormones": {
            "ESC_H01_ADRENALINE": 0.9,
            "ESC_H02_CORTISOL": 0.8
        }
    }
    # Direct inject to mock bus flow
    mock_bus.publish("bus:physical", payload)
    
    # 4. Verify State Update
    # Adrenaline should increase Stress
    # Stress positive factors: ["ESC_H01_ADRENALINE", "ESC_H02_CORTISOL", ...]
    # Matrix uses inertia (0.7) and learning_rate (0.3)
    # Target = 1.0 (approximated from high inputs)
    # New = (1.0 * 0.3) + (0.5 * 0.7) = 0.3 + 0.35 = 0.65
    
    new_stress = matrix.axes_9d['stress']
    print(f"New Stress: {new_stress}")
    assert new_stress > 0.5, "Stress should increase"
    assert new_stress >= 0.6, "Stress should be roughly 0.65"
    
    # 5. Verify Bus Publication
    # Expect publication to bus:psychological
    published = [p for p in mock_bus.published if p[0] == "bus:psychological"]
    assert len(published) > 0, "Should publish psychological state"
    
    last_pub = published[-1][1]
    print(f"Published Mood: {last_pub['mood']}")
    
    # 6. Verify Persistence
    state_file = test_dir / "consciousness/state/psychological/current.json"
    assert state_file.exists(), "State file should be created"
    
    content = json.loads(state_file.read_text())
    assert content["axes_9d"]["stress"] == new_stress, "Persisted state should match memory"
    
    # Cleanup
    shutil.rmtree(test_dir)
    print("\n[PASS] EVA Matrix verification successful!")

if __name__ == "__main__":
    verify_eva_matrix()
