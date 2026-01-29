"""
Verify GKS - Knowledge System Test.
Tests Loading, Graph Building, and Querying.
"""
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gks.system import GKSSystem

def test_gks():
    print("=" * 60)
    print("EVA Genesis - Knowledge System (GKS) Verification")
    print("=" * 60)
    
    # 1. Setup
    base_path = Path(__file__).parent.parent.parent
    gks = GKSSystem(base_path=base_path)
    
    # 2. Check Graph Build
    node_count = len(gks.graph.nodes)
    print(f"\n[1] Graph Status:")
    print(f"   - Nodes: {node_count}")
    
    # We expect at least the sample block we made
    assert node_count >= 1
    
    # 3. Test Query
    print(f"\n[2] Querying 'Umbrella'...")
    result = gks.query("Umbrella")
    
    print(f"   - Summary: {result['summary']}")
    hits = result['hits']
    if hits:
        print(f"   - Hit 1 ID: {hits[0]['id']}")
        content = hits[0]['content']
        # Depending on JSON structure, navigate to definition
        # Our sample: Genesis_Block -> Content -> Definition
        def_text = content.get("Genesis_Block", {}).get("Content", {}).get("Definition", "N/A")
        print(f"   - Definition: {def_text}")
        
        assert "shelter" in def_text
    else:
        print("   [FAIL] No hits found for 'Umbrella'")
        return False
        
    return True

if __name__ == "__main__":
    if test_gks():
        print("\n>>> GKS TESTS PASSED <<<")
    else:
        print("\n>>> GKS TESTS FAILED <<<")
        sys.exit(1)
