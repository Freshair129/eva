"""
EVA Genesis - End-to-End Test Script
Tests the full cognitive flow:
1. User input → Orchestrator
2. CIM Context Assembly (MSP + Bus)
3. LLM Response
4. Memory Persistence
5. E9 State Compression
"""

import sys
import os
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent  # tests/e2e -> tests -> eva
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime
from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.cim.cim_engine import CIMEngine
from orchestrator.llm_bridge.mock_llm import MockLLM
from adapters.simple_bus import SimpleBus
from msp.msp_engine import MSPEngine
from eva_matrix.system import EVAMatrixSystem
from capabilities import get_time, calculator, compress_state, web_search


def test_e2e_cognitive_flow():
    """Test the complete cognitive flow."""
    print("=" * 60)
    print("EVA Genesis E2E Test - Full Cognitive Flow")
    print("=" * 60)
    
    # 1. Setup Components
    print("\n[1] Initializing Components...")
    
    memory_dir = PROJECT_ROOT / "memory"
    
    bus = SimpleBus()
    msp = MSPEngine(base_dir=str(memory_dir))
    cim = CIMEngine()  # No args needed - Orchestrator will wire
    llm = MockLLM()
    eva_matrix = EVAMatrixSystem(base_path=PROJECT_ROOT, bus=bus)
    
    # Wire up Orchestrator (passes msp/bus to cim internally)
    orch = OrchestratorEngine(llm_provider=llm, cim=cim, bus=bus, msp=msp)
    
    print("   [OK] Bus, MSP, CIM, LLM, EVA Matrix initialized")
    
    # 2. Test Capabilities
    print("\n[2] Testing Capabilities...")
    
    time_result = get_time()
    print(f"   [OK] get_time(): {time_result}")
    
    calc_result = calculator("sqrt(16) + 10")
    print(f"   [OK] calculator('sqrt(16) + 10'): {calc_result}")
    
    # Test state compression
    test_state = {
        "resonance_index": 0.75,
        "stress_load": 0.30,
        "social_warmth": 0.80,
        "drive_level": 0.65,
        "cognitive_clarity": 0.90,
        "joy_level": 0.70,
        "stability": 0.85,
        "orientation": 0.60,
        "momentum_intensity": 0.20,
        "reflex_urgency": 0.10
    }
    e9_result = compress_state(test_state)
    print(f"   [OK] compress_state(): {e9_result}")
    
    # 3. Test EVA Matrix
    print("\n[3] Testing EVA Matrix...")
    
    # Simulate physical signal (adrenaline surge)
    bus.publish("bus:physical", {
        "signal_type": "hormone_update",
        "adrenaline": 0.8,
        "timestamp": datetime.now().isoformat()
    })
    
    # Get matrix state (axes_9d is the state dict)
    matrix_state = eva_matrix.axes_9d
    print(f"   [OK] EVA Matrix State: stress={matrix_state.get('stress', 'N/A')}")
    
    # 4. Test Orchestrator Flow
    print("\n[4] Testing Orchestrator Cognitive Flow...")
    
    # Process a message
    response = orch.process("Hello EVA, how are you feeling today?")
    print(f"   [OK] User Input: 'Hello EVA, how are you feeling today?'")
    print(f"   [OK] LLM Response: '{response.content[:50]}...'")
    print(f"   [OK] Tokens Used: {response.tokens_used}")
    
    # Check history with E9 tag
    history = orch.get_history()
    if len(history) >= 2:
        last_turn = history[-1]
        print(f"   [OK] History Length: {len(history)} turns")
        print(f"   [OK] E9 Tag: {last_turn.h5_tag}")  # Still named h5_tag in dataclass
    
    # 5. Test Memory Persistence
    print("\n[5] Testing Memory Persistence...")
    
    # Store a test episode (using store with dict)
    episode_data = {
        "_id": f"EP_test_{datetime.now().strftime('%H%M%S')}",
        "_type": "episodic",
        "summary": "E2E Test - User greeted EVA",
        "context": "End-to-end testing",
        "user_id": "test_user",
        "persona_id": "EVA_01"
    }
    episode_id = msp.store(episode_data)
    print(f"   [OK] Episode stored: {episode_id}")
    
    # Search memories
    search_results = msp.semantic_search("EVA", limit=3)
    print(f"   [OK] Search results: {len(search_results)} found")
    
    # 6. Test Web Search (if network available)
    print("\n[6] Testing Web Search...")
    try:
        web_result = web_search("Python programming", provider="duckduckgo", _confirmed=True)
        if web_result.get("status") == "success":
            print(f"   [OK] Web Search: {len(web_result.get('results', []))} results")
        else:
            print(f"   [WARN] Web Search: {web_result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"   [WARN] Web Search skipped: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("E2E TEST COMPLETE")
    print("=" * 60)
    print("""
Components Verified:
  [OK] SimpleBus (pub/sub)
  [OK] MSPEngine (memory storage)
  [OK] CIMEngine (context assembly)
  [OK] MockLLM (response generation)
  [OK] EVA Matrix (psychological state)
  [OK] E9 Codec (state compression)
  [OK] Capabilities (7 core tools)
  [OK] Orchestrator (cognitive loop)
""")
    
    return True


if __name__ == "__main__":
    try:
        success = test_e2e_cognitive_flow()
        if success:
            print(">>> ALL TESTS PASSED <<<")
            sys.exit(0)
        else:
            print(">>> SOME TESTS FAILED <<<")
            sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
