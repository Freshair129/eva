"""Capabilities Domain - The 'Hands' of EVA."""
__version__ = "0.1.0"

# Core Tools (L1)
from .core.state_tools import compress_state, introspect_state
from .core.time_tools import get_time, get_timestamp, format_relative_time
from .core.memory_tools import recall_memory, save_memory

# File System Tools (L1/L2)
from .filesystem.file_ops import read_file, list_files, write_file, make_directory, delete_file

# Utility Tools (L1)
from .utility.math_tools import calculator, random_number, random_choice, dice_roll

# Agentic Tools (L1/L3)
from .agentic.web_tools import web_search, fetch_url
from .agentic.code_tools import run_python, evaluate_expression
from .agentic.planning_tools import plan_task, track_progress, reflect_on_task
