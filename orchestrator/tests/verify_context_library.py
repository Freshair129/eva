"""Verification script for Context Library Container (P2-013)."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from orchestrator.cim.context_library_loader import ContextLibraryLoader
from orchestrator.cim.cim_engine import CIMEngine

def verify_context_library():
    print("Verifying Context Library Container...\n")

    # Step 1: Test ContextLibraryLoader standalone
    print("Step 1: Testing ContextLibraryLoader...")
    loader = ContextLibraryLoader("consciousness")
    
    identity = loader.load_identity()
    assert len(identity) > 100, "Identity should load content"
    print(f"  Identity loaded: {len(identity)} chars")

    state = loader.load_state()
    assert "bus:physical" in state, "Physical state should be present"
    assert "bus:psychological" in state, "Psychological state should be present"
    print(f"  State channels: {list(state.keys())}")

    prompts = loader.load_prompts()
    assert "system_prefix" in prompts, "System prefix prompt should be present"
    print(f"  Prompts loaded: {list(prompts.keys())}")

    knowledge = loader.load_knowledge(keywords=["coding", "python"])
    assert len(knowledge) > 50, "Knowledge should load content"
    print(f"  Knowledge loaded: {len(knowledge)} chars")

    print("[PASS] ContextLibraryLoader works!\n")

    # Step 2: Test CIMEngine integration
    print("Step 2: Testing CIMEngine with library...")
    cim = CIMEngine(library_path="consciousness")
    
    # Check that identity was auto-loaded
    assert len(cim._system_identity) > 100, "CIM should auto-load identity"
    print(f"  CIM identity loaded: {len(cim._system_identity)} chars")

    # Check that prompts are available
    assert len(cim._prompts) > 0, "CIM should have prompts"
    print(f"  CIM prompts loaded: {list(cim._prompts.keys())}")

    print("[PASS] CIMEngine integration works!\n")

    # Step 3: Test context building
    print("Step 3: Testing context building...")
    bundle = cim.build_context("Hello, EVA!")
    
    assert bundle.user_input == "Hello, EVA!", "User input should match"
    assert len(bundle.system_identity) > 0, "Identity should be in bundle"
    print(f"  Bundle created with identity: {len(bundle.system_identity)} chars")

    print("[PASS] Context building works!\n")

    print("=== Context Library verification passed! ===")


if __name__ == "__main__":
    verify_context_library()
