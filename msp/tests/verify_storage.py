"""Verification script for MemoryStore (P1-005)."""

import os
import shutil
from msp.storage.file_memory_store import FileMemoryStore
from msp.schema.episodic import EpisodicMemory, SituationContext
from msp.schema.turn import TurnUser, TurnLLM
from msp.schema.sensory import SensoryMemory, Qualia

def verify_storage():
    print("Verifying MemoryStore Implementation...")
    
    # Setup temp storage
    test_dir = "test_memory"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        
    store = FileMemoryStore(base_dir=test_dir)

    # 1. Create a Turn
    t_user = TurnUser(
        turn_id="TU_STORE_001",
        episode_id="EP_STORE_001",
        text_excerpt="Testing storage"
    )
    
    # 2. Store Turn
    id_stored = store.store(t_user.to_dict())
    assert id_stored == "TU_STORE_001"
    
    # Verify file exists
    expected_path = store.base_dir / "turns" / "user" / str(t_user.created_at.year) / f"{t_user.created_at.month:02d}" / "TU_STORE_001.json"
    assert expected_path.exists()
    print(f"[PASS] Turn file created at: {expected_path}")

    # 3. Retrieve
    retrieved = store.retrieve("TU_STORE_001")
    assert retrieved is not None
    assert retrieved["text_excerpt"] == "Testing storage"
    print("[PASS] Retrieval successful")

    # 4. Create Sensory
    smem = SensoryMemory(
        sensory_id="SMEM_STORE_001",
        episode_id="EP_STORE_001",
        data_type="visual",
        qualia=Qualia(color_hex="#00FF00")
    )
    store.store(smem.to_dict())
    
    # 5. Create Episode
    ep = EpisodicMemory(
        episode_id="EP_STORE_001",
        turn_refs=["TU_STORE_001"],
        sensory_refs=["SMEM_STORE_001"],
        situation_context=SituationContext(
            context_id="ctx_001",
            interaction_mode="testing",
            stakes_level="low",
            time_pressure="low"
        )
    )
    store.store(ep.to_dict())
    print("[PASS] All components stored")

    # 6. Query
    eps = store.query({"type": "episodic"})
    assert len(eps) >= 1
    assert eps[0]["episode_id"] == "EP_STORE_001"
    print("[PASS] Query successful")

    # Clean up
    # shutil.rmtree(test_dir)
    print("\n=== MemoryStore verification passed! ===")

if __name__ == "__main__":
    verify_storage()
