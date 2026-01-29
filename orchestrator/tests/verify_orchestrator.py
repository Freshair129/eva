"""Verification script for Orchestrator Engine (P2-010)."""

import sys
import os
from datetime import datetime
from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.llm_bridge.mock_llm import MockLLM
from orchestrator.cim.cim_engine import CIMEngine
from adapters.simple_bus import SimpleBus

def verify_orchestrator():
    print("Verifying Orchestrator Engine...")

    # Setup mocks
    llm = MockLLM(default_response="Mocked response for testing.")
    llm.set_response("who are you", "I am EVA, your embodied assistant.")
    
    bus = SimpleBus()
    cim = CIMEngine(system_identity="You are a witty cat-like assistant.")
    
    orchestrator = OrchestratorEngine(
        llm_provider=llm,
        cim=cim,
        bus=bus
    )

    # Step 1: Process simple greeting
    print("\nStep 1: Testing simple interaction...")
    resp = orchestrator.process("Hello!")
    print(f"Response: {resp.content}")
    print(f"Model used: {resp.model}")
    print(f"Context meta: {resp.context_used}")
    assert "Mocked response" in resp.content
    print("[PASS] Simple interaction verified")

    # Step 2: Testing trigger-based response
    print("\nStep 2: Testing specialized response...")
    resp = orchestrator.process("Who are you?")
    print(f"Response: {resp.content}")
    assert "EVA" in resp.content
    print("[PASS] Specialized response verified")

    # Step 3: Verify history
    print("\nStep 3: Checking history...")
    history = orchestrator.get_history()
    print(f"Turns in history: {len(history)}")
    assert len(history) == 4 # 2 turns (user + assistant) x 2 interactions
    for turn in history:
        print(f"[{turn.timestamp.strftime('%H:%M:%S')}] {turn.role}: {turn.content[:30]}...")
    print("[PASS] History tracking verified")

    # Step 4: Verify bus publishing
    print("\nStep 4: Checking bus events...")
    # Since SimpleBus stores latest by channel
    latest = bus.get_latest("orchestrator:turn")
    print(f"Latest bus event: {latest}")
    assert latest is not None
    assert "Who are you?" in latest["user_input"]
    print("[PASS] Bus publishing verified")

    print("\n=== Orchestrator Engine verification passed! ===")

if __name__ == "__main__":
    # Ensure project root is in path
    sys.path.append(os.getcwd())
    verify_orchestrator()
