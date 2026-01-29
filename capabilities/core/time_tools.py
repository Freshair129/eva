"""
Time Tools - Temporal utilities for EVA.
Security Level: L1 (Safe - Auto-execute)
"""

from datetime import datetime, timezone
from typing import Optional
import locale


def get_time(format: str = "full") -> str:
    """
    Returns current date, time, and timezone.
    
    Args:
        format: Output format
                - "full": Full datetime with timezone (default)
                - "date": Date only (YYYY-MM-DD)
                - "time": Time only (HH:MM:SS)
                - "iso": ISO 8601 format
                
    Returns:
        Formatted datetime string
    """
    now = datetime.now(timezone.utc).astimezone()  # Local timezone
    
    if format == "date":
        return now.strftime("%Y-%m-%d")
    elif format == "time":
        return now.strftime("%H:%M:%S")
    elif format == "iso":
        return now.isoformat()
    else:  # full
        # Human-readable format with timezone name
        tz_name = now.strftime("%Z") or "UTC"
        return f"{now.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})"


def get_timestamp() -> float:
    """Returns current Unix timestamp."""
    return datetime.now(timezone.utc).timestamp()


def format_relative_time(timestamp: float) -> str:
    """
    Formats a timestamp as relative time (e.g., "2 hours ago").
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Human-readable relative time string
    """
    now = datetime.now(timezone.utc).timestamp()
    diff = now - timestamp
    
    if diff < 60:
        return "just now"
    elif diff < 3600:
        minutes = int(diff / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif diff < 86400:
        hours = int(diff / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff < 604800:
        days = int(diff / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    else:
        weeks = int(diff / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
