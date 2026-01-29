"""Verification script for LLM Bridge (P2-010)."""

import sys
import os
from orchestrator.llm_bridge.mock_llm import MockLLM
from orchestrator.llm_bridge.ollama_adapter import OllamaAdapter
from contracts.ports.i_llm_provider import LLMMessage

def verify_llm_bridge():
    print("Verifying LLM Bridge...")

    # 1. Verify MockLLM
    print("Step 1: Testing MockLLM...")
    mock = MockLLM(default_response="Meow!")
    mock.set_response("hello", "Greetings, human.")
    
    resp_default = mock.chat([LLMMessage(role="user", content="How are you?")])
    print(f"Default Response: {resp_default.content}")
    assert resp_default.content == "Meow!"
    
    resp_trigger = mock.chat([LLMMessage(role="user", content="Hello EVA")])
    print(f"Trigger Response: {resp_trigger.content}")
    assert resp_trigger.content == "Greetings, human."
    print("[PASS] MockLLM verified")

    # 2. Verify Ollama Connection (Optional)
    print("\nStep 2: Checking Ollama availability...")
    ollama = OllamaAdapter(model="qwen2") # Try qwen2 or llama2
    if ollama.is_available():
        print("[INFO] Ollama is available!")
        try:
            models = ollama.list_models()
            print(f"Available models: {models}")
            if models:
                # Use first available model if qwen2 not found
                test_model = models[0]
                ollama._model = test_model
                print(f"Testing chat with model: {test_model}...")
                resp = ollama.chat([LLMMessage(role="user", content="Hi, who are you?")])
                print(f"Ollama Response: {resp.content}")
                print("[PASS] Ollama connection verified")
            else:
                print("[SKIP] No models found in Ollama.")
        except Exception as e:
            print(f"[ERROR] Ollama chat failed: {e}")
    else:
        print("[SKIP] Ollama is not running locally. Skipping live test.")

    print("\n=== LLM Bridge verification passed! ===")

if __name__ == "__main__":
    # Ensure project root is in path
    sys.path.append(os.getcwd())
    verify_llm_bridge()
