"""Verification script for Crosslink Manager (P1-008)."""

import os
import shutil
import time
from msp.msp_engine import MSPEngine
from msp.schema.episodic import EpisodicMemory, SituationContext
from msp.schema.sensory import SensoryMemory, Qualia
from msp.schema.semantic import SemanticMemory

def verify_crosslinks():
    print("Verifying Crosslink Manager...")
    
    # Setup test environment
    test_repo = "test_crosslink_repo"
    if os.path.exists(test_repo):
        shutil.rmtree(test_repo)
        
    engine = MSPEngine(base_dir=test_repo)

    # 1. Store an Episode
    print("Step 1: Storing Episode EP_001...")
    ep = EpisodicMemory(
        episode_id="EP_001",
        situation_context=SituationContext(
            context_id="ctx_01",
            interaction_mode="testing",
            stakes_level="low",
            time_pressure="low"
        )
    )
    engine.store(ep.to_dict())

    # 2. Store Sensory Memory pointing to EP_001
    print("Step 2: Storing Sensory SM_001 pointing to EP_001...")
    sensory = SensoryMemory(
        sensory_id="SM_001",
        episode_id="EP_001",
        data_type="visual",
        qualia=Qualia(color_hex="#FFEE00")
    )
    engine.store(sensory.to_dict())

    # 3. Verify Episode back-link (Sensory)
    print("Step 3: Verifying Episode EP_001 has SM_001 in sensory_refs...")
    time.sleep(1) # Ensure file I/O is stable
    updated_ep = engine.retrieve("EP_001")
    assert "SM_001" in updated_ep.get("sensory_refs", [])
    print("[PASS] Sensory back-link verified")

    # 4. Store Semantic Memory pointing to EP_001
    print("Step 4: Storing Semantic SEM_001 as evidence for EP_001...")
    semantic = SemanticMemory(
        id="SEM_001",
        subject="User",
        predicate="loves",
        object="EVA",
        episode_refs=["EP_001"]
    )
    engine.store(semantic.to_dict())

    # 5. Verify Episode back-link (Semantic)
    print("Step 5: Verifying Episode EP_001 has SEM_001 in semantic_refs...")
    updated_ep = engine.retrieve("EP_001")
    assert "SEM_001" in updated_ep.get("semantic_refs", [])
    print("[PASS] Semantic back-link verified")

    # Clean up
    # shutil.rmtree(test_repo)
    print("\n=== Crosslink Manager verification passed! ===")

if __name__ == "__main__":
    verify_crosslinks()
