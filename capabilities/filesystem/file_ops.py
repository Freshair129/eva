"""
File System Tools - File operations for EVA.
Security Level: L1 (read/list), L2 (write/mkdir - requires confirmation)
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

# Sandbox configuration
ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".yaml", ".yml", ".py", ".js", ".html", ".css"}
MAX_FILE_SIZE = 1024 * 1024  # 1MB
FORBIDDEN_PATHS = {"C:\\Windows", "C:\\Program Files", "/etc", "/usr", "/bin"}


def _is_path_safe(path: str) -> bool:
    """Check if path is safe to access."""
    abs_path = os.path.abspath(path)
    
    # Check forbidden paths
    for forbidden in FORBIDDEN_PATHS:
        if abs_path.startswith(forbidden):
            return False
    
    return True


def _check_extension(path: str) -> bool:
    """Check if file extension is allowed."""
    ext = Path(path).suffix.lower()
    return ext in ALLOWED_EXTENSIONS or ext == ""


# ============================================================
# L1: Safe Operations (Auto-execute)
# ============================================================

def read_file(path: str, encoding: str = "utf-8") -> str:
    """
    Reads content of a file (text/code).
    Security Level: L1 (Safe - Auto-execute)
    
    Args:
        path: File path to read
        encoding: File encoding (default: utf-8)
        
    Returns:
        File content as string, or error message
    """
    try:
        if not _is_path_safe(path):
            return f"[ERROR] Access denied: {path}"
        
        if not os.path.exists(path):
            return f"[ERROR] File not found: {path}"
        
        if not os.path.isfile(path):
            return f"[ERROR] Not a file: {path}"
            
        # Check file size
        if os.path.getsize(path) > MAX_FILE_SIZE:
            return f"[ERROR] File too large (max {MAX_FILE_SIZE} bytes): {path}"
        
        with open(path, "r", encoding=encoding) as f:
            return f.read()
            
    except Exception as e:
        logger.error(f"Error reading file {path}: {e}")
        return f"[ERROR] {str(e)}"


def list_files(path: str, pattern: str = "*", recursive: bool = False) -> List[str]:
    """
    Lists files in a directory.
    Security Level: L1 (Safe - Auto-execute)
    
    Args:
        path: Directory path to list
        pattern: Glob pattern (default: "*")
        recursive: Search recursively (default: False)
        
    Returns:
        List of file paths
    """
    try:
        if not _is_path_safe(path):
            return [f"[ERROR] Access denied: {path}"]
        
        if not os.path.exists(path):
            return [f"[ERROR] Path not found: {path}"]
        
        if not os.path.isdir(path):
            return [f"[ERROR] Not a directory: {path}"]
        
        p = Path(path)
        
        if recursive:
            files = list(p.rglob(pattern))
        else:
            files = list(p.glob(pattern))
        
        # Return relative paths
        return [str(f.relative_to(p)) for f in files if f.is_file()]
        
    except Exception as e:
        logger.error(f"Error listing {path}: {e}")
        return [f"[ERROR] {str(e)}"]


# ============================================================
# L2: Destructive Operations (Requires Confirmation)
# ============================================================

def write_file(
    path: str, 
    content: str, 
    encoding: str = "utf-8",
    overwrite: bool = False,
    _confirmed: bool = False
) -> Dict[str, Any]:
    """
    Creates or overwrites a file.
    Security Level: L2 (Destructive - Requires Confirmation)
    
    Args:
        path: File path to write
        content: Content to write
        encoding: File encoding (default: utf-8)
        overwrite: Allow overwriting existing file
        _confirmed: Internal flag for confirmation bypass
        
    Returns:
        Result dictionary with status and message
    """
    # Check confirmation
    if not _confirmed:
        return {
            "status": "pending_confirmation",
            "action": "write_file",
            "path": path,
            "message": f"Request to write {len(content)} bytes to {path}. Confirm?"
        }
    
    try:
        if not _is_path_safe(path):
            return {"status": "error", "message": f"Access denied: {path}"}
        
        if not _check_extension(path):
            return {"status": "error", "message": f"Extension not allowed: {Path(path).suffix}"}
        
        # Check if exists
        if os.path.exists(path) and not overwrite:
            return {"status": "error", "message": f"File exists. Set overwrite=True to replace."}
        
        # Create parent directories
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding=encoding) as f:
            f.write(content)
        
        logger.info(f"Wrote {len(content)} bytes to {path}")
        return {"status": "success", "message": f"File written: {path}", "bytes": len(content)}
        
    except Exception as e:
        logger.error(f"Error writing file {path}: {e}")
        return {"status": "error", "message": str(e)}


def make_directory(
    path: str,
    _confirmed: bool = False
) -> Dict[str, Any]:
    """
    Creates a new folder.
    Security Level: L2 (Destructive - Requires Confirmation)
    
    Args:
        path: Directory path to create
        _confirmed: Internal flag for confirmation bypass
        
    Returns:
        Result dictionary with status and message
    """
    # Check confirmation
    if not _confirmed:
        return {
            "status": "pending_confirmation",
            "action": "make_directory",
            "path": path,
            "message": f"Request to create directory: {path}. Confirm?"
        }
    
    try:
        if not _is_path_safe(path):
            return {"status": "error", "message": f"Access denied: {path}"}
        
        # Check if exists
        if os.path.exists(path):
            if os.path.isdir(path):
                return {"status": "exists", "message": f"Directory already exists: {path}"}
            else:
                return {"status": "error", "message": f"Path exists and is not a directory: {path}"}
        
        Path(path).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created directory: {path}")
        return {"status": "success", "message": f"Directory created: {path}"}
        
    except Exception as e:
        logger.error(f"Error creating directory {path}: {e}")
        return {"status": "error", "message": str(e)}


def delete_file(
    path: str,
    _confirmed: bool = False
) -> Dict[str, Any]:
    """
    Deletes a file.
    Security Level: L2 (Destructive - Requires Confirmation)
    
    Args:
        path: File path to delete
        _confirmed: Internal flag for confirmation bypass
        
    Returns:
        Result dictionary with status and message
    """
    # Check confirmation
    if not _confirmed:
        return {
            "status": "pending_confirmation",
            "action": "delete_file",
            "path": path,
            "message": f"Request to DELETE file: {path}. This is irreversible. Confirm?"
        }
    
    try:
        if not _is_path_safe(path):
            return {"status": "error", "message": f"Access denied: {path}"}
        
        if not os.path.exists(path):
            return {"status": "error", "message": f"File not found: {path}"}
        
        if not os.path.isfile(path):
            return {"status": "error", "message": f"Not a file (use delete_directory for folders): {path}"}
        
        os.remove(path)
        
        logger.info(f"Deleted file: {path}")
        return {"status": "success", "message": f"File deleted: {path}"}
        
    except Exception as e:
        logger.error(f"Error deleting file {path}: {e}")
        return {"status": "error", "message": str(e)}
