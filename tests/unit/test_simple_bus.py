import pytest


class TestSimpleBus:
    """Tests for SimpleBus implementation."""

    def test_publish_stores_latest(self, simple_bus):
        """Published message should be stored as latest."""
        simple_bus.publish("test:channel", {"data": "hello"})
        latest = simple_bus.get_latest("test:channel")
        assert latest["data"] == "hello"

    def test_subscribe_receives_messages(self, simple_bus):
        """Subscribers should receive published messages."""
        received = []
        simple_bus.subscribe("test:channel", lambda msg: received.append(msg))
        simple_bus.publish("test:channel", {"data": "world"})
        assert len(received) == 1
        assert received[0]["data"] == "world"

    def test_unsubscribe_stops_messages(self, simple_bus):
        """Unsubscribed callbacks should not receive messages."""
        received = []
        sub_id = simple_bus.subscribe("test:channel", lambda msg: received.append(msg))
        simple_bus.unsubscribe(sub_id)
        simple_bus.publish("test:channel", {"data": "ignored"})
        assert len(received) == 0

    def test_list_channels(self, simple_bus):
        """list_channels should return all known channels."""
        simple_bus.publish("channel:a", {})
        simple_bus.publish("channel:b", {})
        channels = simple_bus.list_channels()
        assert "channel:a" in channels
        assert "channel:b" in channels
