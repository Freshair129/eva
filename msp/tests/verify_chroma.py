"""Verification script for ChromaDB Integration (P1-006)."""

import os
import shutil
import time
from msp.storage.chroma_store import ChromaMemoryStore

def verify_chroma():
    print("Verifying ChromaDB Integration...")
    
    # Setup test DB
    test_db_dir = "test_vector_db"
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)
        
    store = ChromaMemoryStore(persist_directory=test_db_dir)

    # 1. Index some data
    print("Indexing sample turns...")
    store.store({
        "turn_id": "TU_001",
        "type": "turn_user",
        "text_excerpt": "I love eating sushi and japanese food.",
        "category": "food"
    })
    
    store.store({
        "turn_id": "TU_002",
        "type": "turn_user",
        "text_excerpt": "Python is a great programming language for AI.",
        "category": "coding"
    })
    
    store.store({
        "turn_id": "TU_003",
        "type": "turn_user",
        "text_excerpt": "Listening to jazz music helps me focus.",
        "category": "music"
    })

    # Small delay to ensure indexing is ready (though Chroma is usually sync)
    time.sleep(1)

    # 2. Test Semantic Search: Coding
    print("\nTesting Search: 'software development'...")
    results = store.semantic_search("software development", limit=1)
    assert len(results) > 0
    assert results[0]["category"] == "coding"
    print(f"[PASS] Found coding turn: {results[0]['text_excerpt']} (Distance: {results[0]['_distance']:.4f})")

    # 3. Test Semantic Search: Food
    print("\nTesting Search: 'raw fish and rice'...")
    results = store.semantic_search("raw fish and rice", limit=1)
    assert len(results) > 0
    assert results[0]["category"] == "food"
    print(f"[PASS] Found food turn: {results[0]['text_excerpt']} (Distance: {results[0]['_distance']:.4f})")

    # 4. Filter Testing
    print("\nTesting Filtered Search (music category only)...")
    results = store.semantic_search("something to eat", filters={"category": "music"})
    assert len(results) == 1 
    assert results[0]["category"] == "music"
    print(f"[PASS] Filter constrained results to: {results[0]['text_excerpt']}")

    # Clean up
    # shutil.rmtree(test_db_dir)
    print("\n=== ChromaDB verification passed! ===")

if __name__ == "__main__":
    verify_chroma()
