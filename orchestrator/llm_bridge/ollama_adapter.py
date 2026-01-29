"""OllamaAdapter - Local LLM via Ollama."""

import requests
import logging
from typing import List

from contracts.ports.i_llm_provider import ILLMProvider, LLMMessage, LLMResponse

logger = logging.getLogger(__name__)

class OllamaAdapter(ILLMProvider):
    """
    LLM provider using local Ollama server.

    Ollama runs local models like Llama, Mistral, etc.
    Default endpoint: http://localhost:11434

    Attributes:
        _base_url: Ollama server URL
        _model: Model name (e.g., 'llama2', 'mistral')
    """

    def __init__(
        self,
        model: str = "llama2",
        base_url: str = "http://localhost:11434"
    ):
        """
        Initialize Ollama adapter.

        Args:
            model: Model name to use
            base_url: Ollama server URL
        """
        self._model = model
        self._base_url = base_url.rstrip("/")

    def chat(self, messages: List[LLMMessage],
             temperature: float = 0.7,
             max_tokens: int = 1000) -> LLMResponse:
        """
        Send chat request to Ollama.

        Args:
            messages: Conversation history
            temperature: Creativity (0.0-1.0)
            max_tokens: Max response tokens

        Returns:
            LLMResponse with content

        Raises:
            ConnectionError: If Ollama server unavailable
        """
        # Format messages for Ollama API
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        try:
            response = requests.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": formatted_messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120  # Long timeout for local inference
            )
            response.raise_for_status()

            data = response.json()

            return LLMResponse(
                content=data["message"]["content"],
                model=self._model,
                tokens_used=data.get("eval_count", 0),
                finish_reason=data.get("done_reason", "stop")
            )

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self._base_url}. "
                "Is Ollama running?"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError("Ollama request timed out")

    def get_model_name(self) -> str:
        """Returns the configured model name."""
        return self._model

    def is_available(self) -> bool:
        """Check if Ollama server is reachable."""
        try:
            response = requests.get(
                f"{self._base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """
        List available models on Ollama server.

        Returns:
            List of model names
        """
        try:
            response = requests.get(
                f"{self._base_url}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []
