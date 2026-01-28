"""Verification script for MSP Engine Integration (P1-007)."""

import os
import shutil
import time
from msp.msp_engine import MSPEngine
from msp.schema.turn import TurnUser

def verify_msp_engine():
    print("Verifying MSPEngine Integration...")
    
    # Setup test environment
    test_repo = "test_msp_repo"
    if os.path.exists(test_repo):
        shutil.rmtree(test_repo)
        
    engine = MSPEngine(base_dir=test_repo)

    # 1. Store a memory via Engine
    print("Storing TurnUser...")
    turn = TurnUser(
        turn_id="TU_ENGINE_01",
        episode_id="EP_ENGINE_01",
        text_excerpt="I am learning how to use the MSP Engine.",
        intent="learning",
        salience_anchor=["MSP", "Engine"]
    )
    
    engine.store(turn.to_dict())
    print("[PASS] Store completed")

    # 2. Verify File Persistence
    # Expected path check (just existence check for brevity)
    found_files = list(Path(test_repo).rglob("TU_ENGINE_01.json"))
    assert len(found_files) == 1
    print(f"[PASS] File persisted at: {found_files[0]}")

    # 3. Test Semantic Search (Hydrated)
    print("\nPerforming Semantic Search for 'memory system integration'...")
    # Delay for indexing stability although Chroma is mostly synchronous
    time.sleep(1)
    
    results = engine.semantic_search("memory system integration", limit=1)
    
    assert len(results) == 1
    # Verify hydration: Should have full object fields (like intent) not just text
    assert results[0]["turn_id"] == "TU_ENGINE_01"
    assert results[0]["intent"] == "learning"
    assert "_search_score" in results[0]
    
    print(f"[PASS] Found hydrated memory: '{results[0]['text_excerpt']}'")
    print(f"       Intent: {results[0]['intent']}")
    print(f"       Search Distance: {results[0].get('_search_score'):.4f}")

    # Clean up
    # shutil.rmtree(test_repo)
    print("\n=== MSPEngine Integration verified! ===")

if __name__ == "__main__":
    from pathlib import Path
    verify_msp_engine()
