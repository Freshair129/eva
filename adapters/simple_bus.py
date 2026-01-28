import uuid
from typing import Dict, Any, Callable, Optional, List
from contracts.ports.i_bus import IBus


class SimpleBus(IBus):
    """
    Simple in-memory message bus for Phase 1.

    Features:
    - Basic pub/sub
    - Stores latest message per channel
    - No persistence
    - No message replay
    - No guaranteed delivery

    For production, use ResonanceBus (Phase 5).
    """

    def __init__(self):
        self._subscriptions: Dict[str, Dict[str, Callable]] = {}
        self._latest: Dict[str, Dict[str, Any]] = {}
        self._channels: set = set()

    def publish(self, channel: str, payload: Dict[str, Any]) -> None:
        """Publishes payload to channel and notifies subscribers."""
        self._channels.add(channel)
        self._latest[channel] = payload

        # Notify all subscribers
        if channel in self._subscriptions:
            for callback in self._subscriptions[channel].values():
                try:
                    callback(payload)
                except Exception as e:
                    # Log but don't fail
                    print(f"[SimpleBus] Callback error on {channel}: {e}")

    def subscribe(
        self,
        channel: str,
        callback: Callable[[Dict[str, Any]], None]
    ) -> str:
        """Subscribes to channel, returns subscription ID."""
        self._channels.add(channel)

        if channel not in self._subscriptions:
            self._subscriptions[channel] = {}

        sub_id = str(uuid.uuid4())[:8]
        self._subscriptions[channel][sub_id] = callback
        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Removes subscription by ID."""
        for channel, subs in self._subscriptions.items():
            if subscription_id in subs:
                del subs[subscription_id]
                return True
        return False

    def get_latest(self, channel: str) -> Optional[Dict[str, Any]]:
        """Returns most recent message on channel."""
        return self._latest.get(channel)

    def list_channels(self) -> List[str]:
        """Returns list of known channels."""
        return list(self._channels)

    # Utility methods (not in interface)

    def clear(self) -> None:
        """Clears all subscriptions and messages. For testing."""
        self._subscriptions.clear()
        self._latest.clear()
        self._channels.clear()

    def get_subscriber_count(self, channel: str) -> int:
        """Returns number of subscribers on a channel."""
        return len(self._subscriptions.get(channel, {}))
