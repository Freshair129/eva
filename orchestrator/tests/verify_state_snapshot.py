"""Verification script for State Snapshot (P2-016)."""

import sys
import os
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from orchestrator.orchestrator_engine import OrchestratorEngine, OrchestratorResponse
from orchestrator.integration.msp_integration import MSPIntegration, IntegratedOrchestrator
from orchestrator.cim.cim_engine import CIMEngine
from contracts.ports.i_llm_provider import ILLMProvider, LLMMessage, LLMResponse
from contracts.ports.i_bus import IBus

class MockLLM(ILLMProvider):
    def chat(self, messages: list[LLMMessage]) -> LLMResponse:
        return LLMResponse(content="I feel nothing.", model="mock", tokens_used=10, finish_reason="stop")
    
    def get_model_name(self) -> str:
        return "mock-model"
        
    def is_available(self) -> bool:
        return True

def verify_state_snapshot():
    print("Verifying State Snapshot Integration...\n")

    # 1. Setup Mocks
    mock_msp = MagicMock()
    mock_bus = MagicMock()
    
    # Mock Bus behaviour to return state
    mock_bus.get_latest.side_effect = lambda channel: {
        "bus:physical": {"heart_rate": 80},
        "bus:psychological": {"mood": "curious"},
        "bus:phenomenological": {"qualia": "blue_light"}
    }.get(channel)

    # 2. Setup Components
    cim = CIMEngine()
    llm = MockLLM()
    orch_engine = OrchestratorEngine(llm, cim, bus=mock_bus, msp=mock_msp)
    
    # Create the Integrated Orchestrator (System Under Test)
    integrated_orch = IntegratedOrchestrator(orch_engine, msp=mock_msp, bus=mock_bus)
    
    # Spy on the internal integration's store_turn method
    # Since IntegratedOrchestrator creates its own MSPIntegration instance internally,
    # we need to mock THAT instance or its method.
    # But wait, IntegratedOrchestrator.__init__ creates self._integration = MSPIntegration(msp)
    # We can access it directly to mock its store_turn.
    
    integrated_orch._integration.store_turn = MagicMock(return_value="EP_12345")
    
    # 3. Simulate Interaction
    print("Processing interaction...")
    user_input = "How do you feel?"
    integrated_orch.process(user_input)
    
    # 4. Verification
    # Check if store_turn was called
    assert integrated_orch._integration.store_turn.called, "store_turn should be called"
    
    # Check arguments passed to store_turn
    args, kwargs = integrated_orch._integration.store_turn.call_args
    state_captured = kwargs.get('state_snapshot')
    
    print(f"Captured State: {state_captured}")
    
    assert state_captured is not None, "State snapshot should be passed"
    assert state_captured["bus:physical"]["heart_rate"] == 80, "Physical state should be captured"
    assert state_captured["bus:psychological"]["mood"] == "curious", "Psych state should be captured"
    
    print("\n[PASS] State Snapshot verification successful!")

if __name__ == "__main__":
    verify_state_snapshot()
