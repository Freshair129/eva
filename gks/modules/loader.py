"""
GKS Loader - Genesis Block Reader.
Parses standardized JSON blocks into internal dictionary structures.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class GKSLoader:
    """
    Responsible for loading and validating Genesis Blocks.
    """
    
    def __init__(self, library_path: Path):
        self.library_path = library_path
        
    def load_block(self, filename: str) -> Optional[Dict[str, Any]]:
        """Loads a single JSON block file."""
        path = self.library_path / filename
        if not path.exists():
            # Try adding .json
            path = self.library_path / f"{filename}.json"
            
        if not path.exists():
            logger.warning(f"[GKS] Block not found: {filename}")
            return None
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Basic Validation (Is it a Genesis Block?)
            if "Genesis_Block" not in data and "Knowledge_Block" not in data:
                 logger.warning(f"[GKS] Invalid block structure: {filename}")
                 
            return data
            
        except Exception as e:
            logger.error(f"[GKS] Error loading {filename}: {e}")
            return None

    def scan_library(self) -> Dict[str, Dict[str, Any]]:
        """Loads all valid JSON blocks in the library path."""
        cache = {}
        if not self.library_path.exists():
            logger.warning(f"[GKS] Library path does not exist: {self.library_path}")
            return cache
            
        for path in self.library_path.glob("*.json"):
            block = self.load_block(path.name)
            if block:
                # Use filename stem as ID (or internal ID if available)
                block_id = path.stem
                cache[block_id] = block
                
        logger.info(f"[GKS] Loaded {len(cache)} knowledge blocks.")
        return cache
