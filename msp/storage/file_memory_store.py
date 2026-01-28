"""File-based Memory Storage (File-per-Record)."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from contracts.ports.i_memory_storage import IMemoryStorage

logger = logging.getLogger(__name__)

class FileMemoryStore(IMemoryStorage):
    """
    Implementation of IMemoryStorage using local filesystem.
    Follows Date-based Hierarchical structure (ADR-005).
    """

    def __init__(self, base_dir: str = "memory"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, data: Dict[str, Any]) -> Path:
        """Route data to the correct file path based on 'type' field."""
        m_type = data.get("type")
        created_at_str = data.get("created_at")
        
        # Parse date for path generation
        if created_at_str:
            dt = datetime.fromisoformat(created_at_str)
        else:
            dt = datetime.now()

        year = str(dt.year)
        month = f"{dt.month:02d}"

        if m_type == "episodic_v3":
            return self.base_dir / "episodes" / year / month / f"{data['episode_id']}.json"
        
        elif m_type == "turn_user":
            return self.base_dir / "turns" / "user" / year / month / f"{data['turn_id']}.json"
        
        elif m_type == "turn_llm":
            return self.base_dir / "turns" / "llm" / year / month / f"{data['turn_id']}.json"
        
        elif m_type == "sensory_v1":
            return self.base_dir / "turns" / "sensory" / year / month / f"{data['sensory_id']}.json"
        
        elif m_type == "semantic":
            import hashlib
            subj_hash = hashlib.md5(data["subject"].encode()).hexdigest()[:2]
            return self.base_dir / "semantic" / subj_hash / f"{data['id']}.json"
        
        else:
            # Fallback for generic data
            return self.base_dir / "misc" / f"{data.get('id', 'unknown')}.json"

    def store(self, memory_data: Dict[str, Any]) -> str:
        """Stores a memory record to disk."""
        path = self._get_path(memory_data)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(memory_data, f, indent=2, ensure_ascii=False)
        
        # Return the primary ID of the stored object
        return (memory_data.get("turn_id") or 
                memory_data.get("sensory_id") or 
                memory_data.get("episode_id") or 
                memory_data.get("id"))

    def retrieve(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific memory by ID.
        Note: File-per-record requires knowing the path or searching.
        In this Phase, we assume a search or specific path routing.
        (Refinement needed for efficient global retrieval by ID alone).
        """
        # For Phase 1.1, we'll implement a simple recursive search if path unknown
        for path in self.base_dir.rglob(f"{memory_id}.json"):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def query(self, filters: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Simple file-system query.
        Filters supported: 'type' (episodic, sensory, etc.)
        """
        results = []
        m_type = filters.get("type")
        
        # Search in relevant subfolder if type provided
        search_path = self.base_dir
        if m_type == "episodic": search_path = self.base_dir / "episodes"
        elif m_type == "sensory": search_path = self.base_dir / "turns" / "sensory"
        
        for path in search_path.rglob("*.json"):
            if len(results) >= limit: break
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Apply further filters here if needed
                results.append(data)
        
        return results

    def semantic_search(
        self, 
        query_text: str, 
        limit: int = 10, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """FileMemoryStore does not support vector search yet."""
        logger.warning("Attempted semantic search on FileMemoryStore. Returning empty list.")
        return []

    def delete(self, memory_id: str) -> bool:
        """Deletes the memory file."""
        for path in self.base_dir.rglob(f"{memory_id}.json"):
            path.unlink()
            return True
        return False

    def get_storage_type(self) -> str:
        return "filesystem"
