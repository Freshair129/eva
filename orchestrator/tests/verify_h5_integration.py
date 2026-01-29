"""Verification script for H5 Integration (P3-003)."""

import sys
import os
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.cim.cim_engine import CIMEngine
from contracts.ports.i_llm_provider import ILLMProvider, LLMMessage, LLMResponse

class MockLLM(ILLMProvider):
    def chat(self, messages: list[LLMMessage]) -> LLMResponse:
        return LLMResponse(content="I speak in tags.", model="mock", tokens_used=10, finish_reason="stop")
    
    def get_model_name(self) -> str:
        return "mock-model"
        
    def is_available(self) -> bool:
        return True

def verify_h5_integration():
    print("Verifying H5 History Integration...\n")
    
    # Setup
    cim = CIMEngine()
    llm = MockLLM()
    orch = OrchestratorEngine(llm, cim)
    
    # Process Message
    print("Processing message...")
    orch.process("Hello")
    
    # Check Internal History
    last_turn = orch.get_history()[-1]
    print(f"Last Turn Tag: {last_turn.h5_tag}")
    
    # Expecting default [H5-000000000000] because we passed empty state
    # (Checking if it starts with [H5-)
    assert last_turn.h5_tag is not None, "Tag should be generated"
    assert last_turn.h5_tag.startswith("[H5-"), "Tag should have H5 prefix"
    
    # Check LLM History View
    history_view = orch._get_history_for_llm()
    last_msg = history_view[-1]
    content = last_msg["content"]
    print(f"LLM View Content: '{content}'")
    
    assert "[H5-" in content, "LLM content should contain the tag"
    assert content.endswith("]"), "LLM content should end with the tag"
    
    print("\n[PASS] H5 Integration successful!")

if __name__ == "__main__":
    verify_h5_integration()
