"""Verification script for Sensory Memory Schema."""

from msp.schema.sensory import SensoryMemory, Qualia
from pathlib import Path

def verify_sensory():
    print("Verifying Sensory Memory Schema...")

    # 1. Create Qualia
    q = Qualia(
        color_hex="#E6E6FA",  # Lavender
        texture="soft",
        soundscape="white_noise",
        intensity=0.8
    )

    # 2. Create Sensory Memory
    smem = SensoryMemory(
        sensory_id="SMEM_20260129_001",
        episode_id="EP_001",
        data_type="visual_pattern",
        qualia=q,
        extracted_features={"dominant_color": "lavender", "pattern": "fractal"},
        physio_snapshot={"dopamine": 0.7, "serotonin": 0.6}
    )

    assert smem.sensory_id == "SMEM_20260129_001"
    assert smem.qualia.color_hex == "#E6E6FA"
    assert smem.physio_snapshot["dopamine"] == 0.7
    print("[PASS] Creation passed")

    # 3. Check file path
    path = smem.get_file_path("memory")
    assert "turns" in path.as_posix() and "sensory" in path.as_posix()
    print(f"[PASS] File path: {path}")

    # 4. Serialization
    data = smem.to_dict()
    assert data["type"] == "sensory_v1"
    assert data["qualia"]["texture"] == "soft"
    print("[PASS] Serialization passed")

    # 5. Deserialization
    reconstructed = SensoryMemory.from_dict(data)
    assert reconstructed.sensory_id == smem.sensory_id
    assert reconstructed.qualia.soundscape == "white_noise"
    print("[PASS] Deserialization passed")

    print("\n=== All Sensory Memory tests passed! ===")

if __name__ == "__main__":
    verify_sensory()
