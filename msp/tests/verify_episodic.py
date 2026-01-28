"""Verification script for File-per-Record Architecture."""

from msp.schema.episodic import EpisodicMemory, SituationContext, StructuredSummary
from msp.schema.turn import TurnUser, TurnLLM

def verify_file_per_record():
    print("Verifying File-per-Record Architecture...")

    # 1. Create Turns (standalone)
    t_user = TurnUser(
        turn_id="TU_20260128_001",
        episode_id="EP_20260128_001",
        text_excerpt="Hello EVA",
        emotion_signal="joy"
    )
    
    t_llm = TurnLLM(
        turn_id="TL_20260128_001",
        episode_id="EP_20260128_001",
        text_excerpt="Hi there!",
        epistemic_mode="reflect"
    )
    
    assert t_user.episode_id == "EP_20260128_001"
    assert t_llm.episode_id == "EP_20260128_001"
    print("[PASS] Turn creation passed")

    # 2. Check file paths
    user_path = t_user.get_file_path("memory")
    llm_path = t_llm.get_file_path("memory")
    assert "turns" in user_path.as_posix() and "user" in user_path.as_posix()
    assert "turns" in llm_path.as_posix() and "llm" in llm_path.as_posix()
    print(f"[PASS] User turn path: {user_path}")
    print(f"[PASS] LLM turn path: {llm_path}")

    # 3. Create Episode (lightweight, references only)
    ctx = SituationContext(
        context_id="ctx_001",
        interaction_mode="casual",
        stakes_level="low",
        time_pressure="low",
        domain_area="greeting"
    )
    
    summary = StructuredSummary(
        content="User greeted system.",
        action_taken="Replied with greeting."
    )
    
    episode = EpisodicMemory(
        episode_id="EP_20260128_001",
        turn_refs=["TU_20260128_001", "TL_20260128_001"],  # References only!
        situation_context=ctx,
        summary=summary
    )
    
    assert episode.turn_refs == ["TU_20260128_001", "TL_20260128_001"]
    assert "TU_20260128_001" in episode.turn_refs
    print("[PASS] Episode creation with turn_refs passed")

    # 4. Check episode file path
    ep_path = episode.get_file_path("memory")
    assert "episodes" in ep_path.as_posix()
    print(f"[PASS] Episode path: {ep_path}")

    # 5. Serialization
    ep_dict = episode.to_dict()
    assert ep_dict["type"] == "episodic_v3"
    assert ep_dict["turn_refs"] == ["TU_20260128_001", "TL_20260128_001"]
    print("[PASS] Serialization passed")

    # 6. Deserialization
    reconstructed = EpisodicMemory.from_dict(ep_dict)
    assert reconstructed.turn_refs == episode.turn_refs
    print("[PASS] Deserialization passed")

    print("\n=== All File-per-Record tests passed! ===")

if __name__ == "__main__":
    verify_file_per_record()
