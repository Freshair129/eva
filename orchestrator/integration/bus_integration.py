"""Bus Integration - Event hooks for Orchestrator."""

import logging
from typing import Callable, Dict, Any, Optional
from contracts.ports.i_bus import IBus

logger = logging.getLogger(__name__)

class BusIntegration:
    """
    Handles bus communication for Orchestrator.

    Publishes:
    - orchestrator:turn_started
    - orchestrator:turn_completed
    - orchestrator:error

    Subscribes to:
    - bus:physical
    - bus:psychological
    - bus:phenomenological
    """

    CHANNEL_TURN_STARTED = "orchestrator:turn_started"
    CHANNEL_TURN_COMPLETED = "orchestrator:turn_completed"
    CHANNEL_ERROR = "orchestrator:error"

    def __init__(self, bus: IBus):
        """
        Initialize bus integration.

        Args:
            bus: IBus implementation
        """
        self._bus = bus
        self._state_cache: Dict[str, Any] = {}

        # Subscribe to state channels
        self._setup_subscriptions()

    def _setup_subscriptions(self) -> None:
        """Subscribe to state channels."""
        channels = ["bus:physical", "bus:psychological", "bus:phenomenological"]
        for channel in channels:
            try:
                # Note: SimpleBus might require a callback that accepts (message)
                # We use a lambda to pass the channel name as well
                self._bus.subscribe(channel, lambda msg, ch=channel: self._cache_state(ch, msg))
                logger.info(f"Subscribed to {channel}")
            except Exception as e:
                logger.error(f"Failed to subscribe to {channel}: {e}")

    def _cache_state(self, channel: str, message: Dict[str, Any]) -> None:
        """Cache latest state from channel."""
        self._state_cache[channel] = message
        logger.debug(f"Cached state from {channel}")

    def get_current_state(self) -> Dict[str, Any]:
        """Get cached state from all channels."""
        return self._state_cache.copy()

    def publish_turn_started(self, user_input: str) -> None:
        """Publish turn started event."""
        self._bus.publish(self.CHANNEL_TURN_STARTED, {
            "user_input": user_input[:200],
            "state_snapshot": self._state_cache.copy()
        })

    def publish_turn_completed(
        self,
        user_input: str,
        response: str,
        tokens_used: int
    ) -> None:
        """Publish turn completed event."""
        self._bus.publish(self.CHANNEL_TURN_COMPLETED, {
            "user_input": user_input[:200],
            "response": response[:200],
            "tokens_used": tokens_used
        })

    def publish_error(self, error: str) -> None:
        """Publish error event."""
        self._bus.publish(self.CHANNEL_ERROR, {
            "error": str(error)
        })
