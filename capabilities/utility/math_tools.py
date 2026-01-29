"""
Math Tools - Mathematical utilities for EVA.
Security Level: L1 (Safe - Auto-execute)
"""

import math
import random
import logging
from typing import Union, Optional

logger = logging.getLogger(__name__)

# Safe math operations whitelist
SAFE_NAMES = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "pow": pow,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "floor": math.floor,
    "ceil": math.ceil,
    "pi": math.pi,
    "e": math.e,
}


def calculator(expression: str) -> Union[float, str]:
    """
    Performs mathematical calculations safely.
    Security Level: L1 (Safe - Auto-execute)
    
    Args:
        expression: Mathematical expression to evaluate
                   Supports: +, -, *, /, **, (), sqrt, sin, cos, tan, log, pi, e
        
    Returns:
        Calculation result as float, or error message
        
    Examples:
        calculator("2 + 2") -> 4.0
        calculator("sqrt(16)") -> 4.0
        calculator("sin(pi/2)") -> 1.0
    """
    try:
        # Clean the expression
        expr = expression.strip()
        
        # Block dangerous operations
        dangerous = ["import", "exec", "eval", "open", "__", "os.", "sys."]
        for d in dangerous:
            if d in expr.lower():
                return f"[ERROR] Blocked operation: {d}"
        
        # Evaluate in safe environment
        result = eval(expr, {"__builtins__": {}}, SAFE_NAMES)
        
        return float(result)
        
    except ZeroDivisionError:
        return "[ERROR] Division by zero"
    except Exception as e:
        logger.error(f"Calculator error: {e}")
        return f"[ERROR] {str(e)}"


def random_number(min_val: int = 0, max_val: int = 100) -> int:
    """
    Generates a random integer.
    Security Level: L1 (Safe - Auto-execute)
    
    Args:
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
        
    Returns:
        Random integer between min and max
    """
    return random.randint(min_val, max_val)


def random_choice(options: list) -> any:
    """
    Picks a random item from a list.
    Security Level: L1 (Safe - Auto-execute)
    
    Args:
        options: List of items to choose from
        
    Returns:
        Random item from the list
    """
    if not options:
        return None
    return random.choice(options)


def dice_roll(sides: int = 6, count: int = 1) -> dict:
    """
    Simulates rolling dice.
    Security Level: L1 (Safe - Auto-execute)
    
    Args:
        sides: Number of sides on each die (default: 6)
        count: Number of dice to roll (default: 1)
        
    Returns:
        Dictionary with rolls and total
    """
    rolls = [random.randint(1, sides) for _ in range(count)]
    return {
        "rolls": rolls,
        "total": sum(rolls),
        "notation": f"{count}d{sides}"
    }
