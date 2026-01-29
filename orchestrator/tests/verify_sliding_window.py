"""Verification script for Sliding Window History (P2-015)."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.cim.cim_engine import CIMEngine
from contracts.ports.i_llm_provider import ILLMProvider, LLMMessage, LLMResponse

class MockLLM(ILLMProvider):
    def chat(self, messages: list[LLMMessage]) -> LLMResponse:
        return LLMResponse(content="Test response", model="mock", tokens_used=10)
    
    def get_model_name(self) -> str:
        return "mock-model"
        
    def is_available(self) -> bool:
        return True

def verify_sliding_window():
    print("Verifying Sliding Window History...\n")

    # Initialize components
    cim = CIMEngine()
    llm = MockLLM()
    
    # Init orchestrator with small window
    window_size = 3
    orch = OrchestratorEngine(llm_provider=llm, cim=cim, max_history_turns=window_size)
    print(f"Initialized Orchestrator with window size: {window_size}")

    # Add 10 turns (user + assistant = 2 turns per interaction)
    # We want to create enough turns to exceed the window
    print("Simulating 5 interactions (10 turns)...")
    for i in range(5):
        orch._add_to_history("user", f"User inputs {i}")
        orch._add_to_history("assistant", f"Assistant response {i}")

    # Check total stored (should be all)
    total_stored = len(orch._conversation_history)
    print(f"Total stored history: {total_stored} turns")
    
    # Check what is returned for LLM (should be only window_size)
    history_for_llm = orch._get_history_for_llm()
    returned_len = len(history_for_llm)
    print(f"History returned for LLM: {returned_len} turns")

    assert total_stored == 10, "Should store full history internally"
    assert returned_len == window_size, f"Should return exactly {window_size} turns for LLM"
    
    # Verify content of returned history (should be the most recent)
    last_msg = history_for_llm[-1]
    print(f"Last message: {last_msg}")
    assert last_msg["content"] == "Assistant response 4", "Last message should match most recent turn"

    first_msg = history_for_llm[0]
    print(f"First message in window: {first_msg}")
    # With window 3, we expect: [User 3, Assistant 3, User 4, Assistant 4] -> Wait, window size is N turns.
    # Indices: 0,1, 2,3, 4,5, 6,7, 8,9
    # Slicing [-3:] gives indices 7, 8, 9
    # 7: Assistant response 3
    # 8: User inputs 4
    # 9: Assistant response 4
    
    assert first_msg["content"] == "Assistant response 3", "First message in window should be correct"

    print("\n[PASS] Sliding window verification successful!")

if __name__ == "__main__":
    verify_sliding_window()
