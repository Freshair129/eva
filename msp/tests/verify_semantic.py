from msp.schema.semantic import SemanticMemory

def verify_semantic():
    print("Verifying SemanticMemory...")
    
    # 1. Creation
    fact = SemanticMemory(subject="User", predicate="likes", object="Sushi")
    assert fact.subject == "User"
    assert fact.predicate == "likes"
    assert fact.object == "Sushi"
    assert fact.id.startswith("sem_")
    print("[PASS] Creation passed")

    # 2. Triple Format
    assert fact.as_triple() == "User likes Sushi"
    print("[PASS] Triple format passed")

    # 3. Serialization
    data = fact.to_dict()
    assert data["subject"] == "User"
    assert data["type"] == "semantic"
    print("[PASS] Serialization passed")

    # 4. Deserialization
    reconstructed = SemanticMemory.from_dict(data)
    assert reconstructed.id == fact.id
    assert reconstructed.subject == fact.subject
    assert reconstructed.learned_at == fact.learned_at
    print("[PASS] Deserialization passed")

if __name__ == "__main__":
    verify_semantic()
