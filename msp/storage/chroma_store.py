"""ChromaDB Memory Storage for Semantic Search."""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

import chromadb
from chromadb.config import Settings
from contracts.ports.i_memory_storage import IMemoryStorage

logger = logging.getLogger(__name__)

class ChromaMemoryStore(IMemoryStorage):
    """
    Adapter for ChromaDB to provide semantic search capabilities.
    Manages embedding and similarity search for memory records.
    """

    def __init__(self, persist_directory: str = "memory/vector_db"):
        self.persist_directory = persist_directory
        # Use PersistentClient for disk storage
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Default collections
        self.turns_collection = self.client.get_or_create_collection(
            name="memory_turns",
            metadata={"hnsw:space": "cosine"}
        )
        self.episodes_collection = self.client.get_or_create_collection(
            name="memory_episodes",
            metadata={"hnsw:space": "cosine"}
        )
        self.semantic_collection = self.client.get_or_create_collection(
            name="memory_semantic",
            metadata={"hnsw:space": "cosine"}
        )

    def store(self, memory_data: Dict[str, Any]) -> str:
        """
        Embeds and stores a memory record.
        Metadata is used for filtering.
        """
        m_type = memory_data.get("type", "unknown")
        m_id = (memory_data.get("turn_id") or 
                memory_data.get("sensory_id") or 
                memory_data.get("episode_id") or 
                memory_data.get("id"))

        # Determine target collection and text to embed
        text_content = ""
        metadata = {k: v for k, v in memory_data.items() if isinstance(v, (str, int, float, bool))}
        
        if m_type.startswith("turn_"):
            collection = self.turns_collection
            text_content = memory_data.get("text_excerpt", "")
        elif m_type == "episodic_v3":
            collection = self.episodes_collection
            # For episodes, we embed the summary content
            if "summary" in memory_data and isinstance(memory_data["summary"], dict):
                text_content = (memory_data["summary"].get("content", "") + " " +
                               memory_data["summary"].get("action_taken", "") + " " + 
                               memory_data["summary"].get("key_outcome", ""))
        elif m_type == "semantic":
            collection = self.semantic_collection
            # Format subject-predicate-object
            text_content = f"{memory_data.get('subject', '')} {memory_data.get('predicate', '')} {memory_data.get('object', '')}"
        else:
            # Skip non-textual or unindexed types for now
            return m_id

        if not text_content or not text_content.strip():
            logger.warning(f"No text content to embed for {m_id}")
            return m_id

        collection.add(
            ids=[m_id],
            documents=[text_content],
            metadatas=[metadata]
        )
        
        return m_id

    def retrieve(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve by ID from vector DB (returns metadata)."""
        # Try all collections
        for collection in [self.turns_collection, self.episodes_collection, self.semantic_collection]:
            res = collection.get(ids=[memory_id])
            if res["ids"]:
                return res["metadatas"][0]
        return None

    def query(self, filters: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Queries metadata in ChromaDB."""
        # Simple metadata filtering - search all and combine
        results = []
        for collection in [self.turns_collection, self.episodes_collection, self.semantic_collection]:
            res = collection.get(where=filters, limit=limit)
            if res["metadatas"]:
                results.extend(res["metadatas"])
        return results[:limit]

    def semantic_search(
        self, 
        query_text: str, 
        limit: int = 10, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Performs vector similarity search across all collections."""
        all_results = []
        
        for collection in [self.turns_collection, self.episodes_collection, self.semantic_collection]:
            try:
                res = collection.query(
                    query_texts=[query_text],
                    n_results=limit,
                    where=filters
                )
                
                if res["ids"] and res["ids"][0]:
                    for i in range(len(res["ids"][0])):
                        item = res["metadatas"][0][i]
                        item["_distance"] = res["distances"][0][i]
                        item["_id"] = res["ids"][0][i]
                        all_results.append(item)
            except Exception as e:
                logger.error(f"Search failed in collection {collection.name}: {e}")

        # Sort combined results by distance (lower is better for cosine)
        all_results.sort(key=lambda x: x.get("_distance", 1.0))
        
        return all_results[:limit]

    def delete(self, memory_id: str) -> bool:
        """Removes record from vector DB."""
        for collection in [self.turns_collection, self.episodes_collection]:
            collection.delete(ids=[memory_id])
        return True

    def get_storage_type(self) -> str:
        return "vector_db"
