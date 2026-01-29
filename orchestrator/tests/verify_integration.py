"""Verification script for MSP Integration (P2-008)."""

import sys
import os
import shutil
from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.llm_bridge.mock_llm import MockLLM
from orchestrator.cim.cim_engine import CIMEngine
from msp.msp_engine import MSPEngine
from adapters.simple_bus import SimpleBus
from orchestrator.integration.msp_integration import create_integrated_orchestrator

def verify_msp_integration():
    print("Verifying MSP Integration...")
    
    # Clean workspace
    if os.path.exists("test_integration_repo"):
        shutil.rmtree("test_integration_repo")

    # Setup core
    llm = MockLLM(default_response="Interesting!")
    llm.set_response("who am i", "You are my creator.")
    
    bus = SimpleBus()
    msp = MSPEngine(base_dir="test_integration_repo")
    cim = CIMEngine(system_identity="You are EVA.")
    
    base_orchestrator = OrchestratorEngine(llm, cim, bus, msp)
    orchestrator = create_integrated_orchestrator(base_orchestrator, msp)

    # Step 1: Fact Extraction Test
    print("\nStep 1: Testing fact extraction...")
    orchestrator.process("I am Freshair and I like coding.")
    
    # Verify semantic record
    semantic_files = list(Path("test_integration_repo/semantic").rglob("*.json"))
    print(f"Semantic records created: {len(semantic_files)}")
    assert len(semantic_files) >= 2
    
    # Step 2: Episodic Storage Test
    print("\nStep 2: Testing episodic storage...")
    episodic_files = list(Path("test_integration_repo/episodes").rglob("*.json"))
    print(f"Episodic records created: {len(episodic_files)}")
    assert len(episodic_files) >= 1
    
    # Step 3: Context Recall Test (The "Magic" part)
    print("\nStep 3: Testing context recall in next turn...")
    # The next turn should recall the fact that I am Freshair
    resp = orchestrator.process("Who am I?")
    print(f"Response: {resp.content}")
    print(f"Memory count used: {resp.context_used['memory_count']}")
    
    # Even if mock doesn't use it, the metadata should show memory was found
    assert resp.context_used['memory_count'] > 0
    print("[PASS] Context recall verified")

    print("\n=== MSP Integration verification passed! ===")
    
    # Clean up (Safe)
    try:
        if os.path.exists("test_integration_repo"):
            # Close msp properly if we had a close method
            shutil.rmtree("test_integration_repo")
    except Exception as e:
        print(f"[NOTE] Cleanup failed: {e}")

if __name__ == "__main__":
    from pathlib import Path
    sys.path.append(os.getcwd())
    verify_msp_integration()
