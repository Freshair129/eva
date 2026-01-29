"""MSP Engine - The unified memory service for EVA."""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from contracts.ports.i_memory_storage import IMemoryStorage
from msp.storage.file_memory_store import FileMemoryStore
from msp.storage.chroma_store import ChromaMemoryStore
from msp.storage.chroma_store import ChromaMemoryStore
from msp.crosslink_manager import CrosslinkManager
from msp.modules.distiller import WisdomDistiller

logger = logging.getLogger(__name__)

class MSPEngine(IMemoryStorage):
    """
    Central orchestrator for all memory operations.
    Delegates persistence to FileMemoryStore and indexing to ChromaMemoryStore.
    """

    def __init__(self, base_dir: str = "memory"):
        self.base_dir = Path(base_dir)
        self.file_store = FileMemoryStore(base_dir=str(self.base_dir))
        self.vector_store = ChromaMemoryStore(persist_directory=str(self.base_dir / "vector_db"))
        self.crosslink_manager = CrosslinkManager(storage=self)
        self.distiller = WisdomDistiller(self)

    def store(self, memory_data: Dict[str, Any]) -> str:
        """
        Stores memory in both persistent file and vector index.
        """
        # 1. Save to File (Source of Truth)
        m_id = self.file_store.store(memory_data)
        
        # 2. Index in Vector DB (for search)
        try:
            self.vector_store.store(memory_data)
        except Exception as e:
            logger.error(f"Failed to index memory {m_id} in Chroma: {e}")
            
        # 3. Synchronize Crosslinks (Bidirectional)
        try:
            self.crosslink_manager.sync_links(memory_data)
        except Exception as e:
            logger.error(f"Failed to sync crosslinks for {m_id}: {e}")
            
        return m_id

    def retrieve(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves hydrated memory from File Store."""
        return self.file_store.retrieve(memory_id)

    def query(self, filters: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Queries memories via File Store metadata listing."""
        return self.file_store.query(filters, limit)

    def semantic_search(
        self, 
        query_text: str, 
        limit: int = 10, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search by meaning and hydrate results with full data from files.
        """
        # 1. Get matches from Vector DB
        matches = self.vector_store.semantic_search(query_text, limit, filters)
        
        # 2. Hydrate matches with full data
        hydrated_results = []
        for match in matches:
            m_id = match.get("_id")
            if m_id:
                full_data = self.retrieve(m_id)
                if full_data:
                    # Merge search score into metadata
                    full_data["_search_score"] = match.get("_distance", 1.0)
                    hydrated_results.append(full_data)
                else:
                    # Fallback to metadata if file is missing (unexpected)
                    hydrated_results.append(match)
                    
        return hydrated_results

    def delete(self, memory_id: str) -> bool:
        """Deletes from both stores."""
        success_file = self.file_store.delete(memory_id)
        success_vector = self.vector_store.delete(memory_id)
        return success_file or success_vector

    def get_storage_type(self) -> str:
        return "unified_msp"
