"""
Code Execution Tools - Python sandbox for EVA.
Security Level: L3 (Code - Requires Confirmation + Strict Sandbox)
"""

import logging
import sys
import io
import contextlib
from typing import Dict, Any, Optional
import traceback

logger = logging.getLogger(__name__)

# Blocked imports for security
BLOCKED_IMPORTS = {
    "os", "sys", "subprocess", "shutil", "pathlib",
    "socket", "requests", "urllib", "http",
    "pickle", "marshal", "ctypes",
    "importlib", "__builtins__"
}

# Allowed safe modules
ALLOWED_MODULES = {
    "math", "random", "datetime", "json", "re",
    "collections", "itertools", "functools",
    "statistics", "decimal", "fractions"
}


def run_python(
    code: str,
    timeout: int = 5,
    _confirmed: bool = False
) -> Dict[str, Any]:
    """
    Executes Python code in a restricted sandbox.
    Security Level: L3 (Code - Requires Confirmation + Sandbox)
    
    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds (default: 5)
        _confirmed: Internal flag for confirmation bypass
        
    Returns:
        Dictionary with execution result or confirmation request
        
    Note:
        This is a basic sandbox. For production, use RestrictedPython or a container.
    """
    # Check confirmation
    if not _confirmed:
        # Show code preview
        code_preview = code[:200] + "..." if len(code) > 200 else code
        return {
            "status": "pending_confirmation",
            "action": "run_python",
            "code_preview": code_preview,
            "message": f"Request to execute Python code ({len(code)} chars). Review and confirm?"
        }
    
    try:
        # Security checks
        for blocked in BLOCKED_IMPORTS:
            if f"import {blocked}" in code or f"from {blocked}" in code:
                return {
                    "status": "error",
                    "message": f"Blocked import detected: {blocked}"
                }
        
        # Check for dangerous patterns
        dangerous = ["exec(", "eval(", "compile(", "__import__", "open(", "file("]
        for d in dangerous:
            if d in code:
                return {
                    "status": "error",
                    "message": f"Dangerous operation blocked: {d}"
                }
        
        # Capture stdout
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        # Create restricted globals
        safe_globals = {
            "__builtins__": {
                "print": print,
                "len": len,
                "range": range,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "abs": abs,
                "min": min,
                "max": max,
                "sum": sum,
                "round": round,
                "sorted": sorted,
                "reversed": reversed,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "any": any,
                "all": all,
                "isinstance": isinstance,
                "type": type,
            }
        }
        
        # Add allowed modules
        import math
        import random as rand_module
        import datetime
        import json
        import re
        
        safe_globals["math"] = math
        safe_globals["random"] = rand_module
        safe_globals["datetime"] = datetime
        safe_globals["json"] = json
        safe_globals["re"] = re
        
        # Execute with captured output
        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            exec(code, safe_globals)
        
        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()
        
        return {
            "status": "success",
            "stdout": stdout_output,
            "stderr": stderr_output,
            "message": "Code executed successfully"
        }
        
    except SyntaxError as e:
        return {
            "status": "error",
            "error_type": "SyntaxError",
            "message": str(e),
            "line": e.lineno
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }


def evaluate_expression(expression: str) -> Dict[str, Any]:
    """
    Evaluates a simple Python expression (safer than run_python).
    Security Level: L1 (Safe - limited to expressions)
    
    Args:
        expression: Python expression to evaluate
        
    Returns:
        Dictionary with evaluation result
    """
    try:
        # Block dangerous patterns
        dangerous = ["import", "exec", "eval", "compile", "__", "open", "file"]
        for d in dangerous:
            if d in expression.lower():
                return {"status": "error", "message": f"Blocked: {d}"}
        
        # Safe eval environment
        import math
        safe_dict = {
            "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
            "len": len, "str": str, "int": int, "float": float, "bool": bool,
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log, "exp": math.exp, "pi": math.pi, "e": math.e,
            "True": True, "False": False, "None": None
        }
        
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        
        return {
            "status": "success",
            "expression": expression,
            "result": result,
            "type": type(result).__name__
        }
        
    except Exception as e:
        return {
            "status": "error",
            "expression": expression,
            "message": str(e)
        }
