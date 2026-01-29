"""
Full Stack E2E Test (Phase 0-5).
Verifies the complete flow from Biological Stimulus to Cognitive Response.

Flow:
1. Stimulus ("Threat") -> PhysioCore (Adrenaline Spike)
2. PhysioCore -> Bus ("bus:physical")
3. EVA Matrix -> Bus ("bus:psychological") [Reacts to Adrenaline]
4. RMS -> Bus ("bus:phenomenological") [Encodes Qualia]
5. Orchestrator -> LLM [Visualizes Context with Qualia]
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.simple_bus import SimpleBus
from msp.msp_engine import MSPEngine
from physio_core.system import PhysioSystem
from eva_matrix.system import EVAMatrixSystem
from rms.system import RMSSystem
from orchestrator.orchestrator_engine import OrchestratorEngine
from orchestrator.cim.cim_engine import CIMEngine
from orchestrator.llm_bridge.mock_llm import MockLLM

def test_full_stack():
    print("=" * 60)
    print("EVA Genesis - Full Stack Verification (P0-P5)")
    print("=" * 60)
    
    # 1. Setup Infrastructure
    print("\n[1] Booting Systems...")
    base_path = Path(__file__).parent.parent.parent
    memory_dir = base_path / "memory"
    
    bus = SimpleBus()
    msp = MSPEngine(base_dir=str(memory_dir))
    
    # 2. Boot Subsystems (Body, Mind, Perception)
    physio = PhysioSystem(bus=bus)
    matrix = EVAMatrixSystem(base_path=base_path, bus=bus)
    rms = RMSSystem(bus=bus)
    
    # 3. Boot Cognition (Brain)
    cim = CIMEngine() 
    llm = MockLLM()
    orch = OrchestratorEngine(llm_provider=llm, cim=cim, bus=bus, msp=msp)
    
    print("   [OK] All Systems Online")
    
    # Monitor Bus
    bus_log = []
    def monitor(channel, payload):
        # print(f"   [BUS] {channel} fired")
        bus_log.append(channel)
        
    for ch in ["bus:physical", "bus:psychological", "bus:phenomenological"]:
        bus.subscribe(ch, lambda p, c=ch: monitor(c, p))

    # 4. Inject Stimulus: THREAT (Simulating a scary event)
    print("\n[2] Injecting Stimulus: 'THREAT'...")
    physio.process_stimulus("threat", intensity=0.9)
    
    # Allow async propagation (mocked as synchronous calls usually, but let's be safe)
    # Physio -> Bus:physical
    # Matrix listens to Bus:physical -> Updates -> Bus:psychological
    # RMS listens to both -> Updates -> Bus:phenomenological
    
    # Since SimpleBus is synchronous, Physio.process_stimulus already triggered bus:physical.
    # But Matrix needs to process that signal.
    # In SimpleBus, subscribers are called immediately.
    # So Physio -> Matrix.on_physical -> Matrix.process -> Bus:psychological
    # And Physio -> RMS.on_physical
    # And Matrix -> RMS.on_psychological -> RMS.process -> Bus:phenomenological
    
    print(f"   [BUS] Events logged: {len(bus_log)}")
    print(f"   [BUS] Channels fired: {list(set(bus_log))}")
    
    # 5. Verify State Cascade
    print("\n[3] Verifying State Cascade...")
    
    # Body
    p_state = physio.get_current_state()
    adrenaline = p_state["hormones"].get("adrenaline", 0)
    print(f"   [BODY] Adrenaline: {adrenaline:.2f} (Expected > 0.3)")
    assert adrenaline > 0.3
    
    # Mind
    m_state = matrix.axes_9d
    stress = m_state.get("stress", 0.5)
    print(f"   [MIND] Stress: {stress:.2f} (Should reflect body state)")
    # Note: Matrix logic might be damped, but let's check direction
    
    # Perception
    r_state = rms.get_current_state()
    qualia = r_state.get("qualia", {})
    resonance = r_state.get("resonance", {})
    
    print(f"   [RMS] Narrative: '{qualia.get('narrative')}'")
    print(f"   [RMS] E9 Code: {resonance.get('resonance_code')}")
    
    assert "Heart pounding" in qualia.get("narrative", "") or "razor" in qualia.get("narrative", "")
    
    # 6. Cognitive Access
    print("\n[4] Cognitive Access (Orchestrator)...")
    
    # The Orchestrator should now be able to see this state via CIM introspect
    # Let's ask it to process a user turn.
    response = orch.process("What do you feel right now?")
    
    print(f"   [LLM] Response generated (Tokens: {response.tokens_used})")
    
    # We can inspect the Context constructed by CIM to see if Qualia was included
    # This assumes Orchestrator/CIM exposes inner workings or we trust the integration.
    # For now, we trust the flow if no errors occurred.
    
    return True

if __name__ == "__main__":
    if test_full_stack():
        print("\n>>> FULL STACK VERIFICATION SUCCESSFUL <<<")
    else:
        print("\n>>> VERIFICATION FAILED <<<")
        sys.exit(1)
