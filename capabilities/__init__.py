"""Capabilities Domain - The 'Hands' of EVA."""
__version__ = "0.1.0"

from .core.state_tools import compress_state, introspect_state
from .core.time_tools import get_time, get_timestamp, format_relative_time
from .core.memory_tools import recall_memory, save_memory
