import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.simple_bus import SimpleBus
from adapters.mocks.mock_state_providers import (
    MockPhysioProvider,
    MockMatrixProvider,
)
from adapters.mocks.mock_resonance_encoder import MockResonanceEncoder


@pytest.fixture
def simple_bus():
    """Provides a fresh SimpleBus instance."""
    bus = SimpleBus()
    yield bus
    bus.clear()


@pytest.fixture
def mock_physio():
    """Provides MockPhysioProvider."""
    return MockPhysioProvider()


@pytest.fixture
def mock_matrix():
    """Provides MockMatrixProvider."""
    return MockMatrixProvider()


@pytest.fixture
def mock_encoder():
    """Provides MockResonanceEncoder."""
    return MockResonanceEncoder()
