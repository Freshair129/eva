"""MockLLM - Fake LLM for testing."""

from typing import List, Optional, Dict

from contracts.ports.i_llm_provider import ILLMProvider, LLMMessage, LLMResponse


class MockLLM(ILLMProvider):
    """
    Mock LLM for testing without real API calls.

    Can be configured with:
    - Fixed responses
    - Response based on input patterns
    - Simulated delays
    """

    def __init__(self, default_response: str = "This is a mock response."):
        """
        Initialize MockLLM.

        Args:
            default_response: Default response text
        """
        self._default_response = default_response
        self._responses: Dict[str, str] = {}
        self._call_history: List[List[LLMMessage]] = []

    def set_response(self, trigger: str, response: str) -> None:
        """
        Set a response for a specific trigger phrase.

        Args:
            trigger: If user message contains this, use response
            response: The response to return
        """
        self._responses[trigger.lower()] = response

    def chat(self, messages: List[LLMMessage],
             temperature: float = 0.7,
             max_tokens: int = 1000) -> LLMResponse:
        """
        Return mock response.

        Checks triggers in last user message, otherwise default.
        """
        self._call_history.append(messages)

        # Get last user message
        user_msg = ""
        for msg in reversed(messages):
            if msg.role == "user":
                user_msg = msg.content.lower()
                break

        # Check triggers
        response_text = self._default_response
        for trigger, response in self._responses.items():
            if trigger in user_msg:
                response_text = response
                break

        return LLMResponse(
            content=response_text,
            model="mock-llm",
            tokens_used=len(response_text.split()),
            finish_reason="stop"
        )

    def get_model_name(self) -> str:
        """Returns 'mock-llm'."""
        return "mock-llm"

    def is_available(self) -> bool:
        """Always available."""
        return True

    def get_call_history(self) -> List[List[LLMMessage]]:
        """Get all calls made to this mock."""
        return self._call_history

    def clear_history(self) -> None:
        """Clear call history."""
        self._call_history.clear()
