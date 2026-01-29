"""
Verify 8-8-8 Protocol - Tiered Distillation Test.
Simulates 8 sessions to trigger Core creation.
"""
import sys
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.simple_bus import SimpleBus
from msp.msp_engine import MSPEngine
from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.cim.cim_engine import CIMEngine
from orchestrator.llm_bridge.mock_llm import MockLLM

def test_888_protocol():
    print("=" * 60)
    print("EVA Genesis - 8-8-8 Protocol Verification")
    print("=" * 60)
    
    # Setup
    base_path = Path(__file__).parent.parent.parent
    mem_path = base_path / "memory_888_test"
    if mem_path.exists():
        shutil.rmtree(mem_path)
    mem_path.mkdir()
        
    bus = SimpleBus()
    msp = MSPEngine(base_dir=str(mem_path))
    cim = CIMEngine()
    cim.set_msp(msp)
    llm = MockLLM()
    orch = OrchestratorEngine(llm_provider=llm, cim=cim, bus=bus, msp=msp)
    
    print("\n[1] Simulating 8 Sessions...")
    for i in range(1, 9):
        sess_id = f"SESS_{i:03d}"
        print(f"   - Processing Session {sess_id}...")
        orch.process(f"Message in session {i}")
        orch.finalize_session(sess_id)
        
    # Check Session Memory
    session_count = len(list((mem_path / "session_memory").glob("session_*.json")))
    print(f"\n[2] Session Memory Status:")
    print(f"   - Total Snapshots: {session_count}")
    assert session_count == 8
    
    # Check Core Memory (Should have been triggered by the 8th session)
    core_units = list((mem_path / "core_memory").glob("core_*.json"))
    print(f"\n[3] Core Memory Status:")
    print(f"   - Total Core Units: {len(core_units)}")
    
    if len(core_units) >= 1:
        print(f"   - [SUCCESS] 8-8-8 Triggered: Core Memory Created.")
        # Inspect 1st core
        import json
        with open(core_units[0], "r") as f:
            data = json.load(f)
            print(f"   - Core ID: {data['id']}")
            print(f"   - Source Sessions: {data['source_sessions']}")
            assert len(data['source_sessions']) == 8
    else:
        print("   - [FAIL] Core Memory not triggered.")
        return False
        
    return True

if __name__ == "__main__":
    if test_888_protocol():
        print("\n>>> 8-8-8 TESTS PASSED <<<")
    else:
        print("\n>>> 8-8-8 TESTS FAILED <<<")
        sys.exit(1)
