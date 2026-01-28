from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class IMemoryStorage(ABC):
    """
    Port interface for memory persistence.

    Defines standard operations for storing and retrieving memories.

    Implementors:
    - EpisodicMemoryModule
    - SemanticMemoryModule
    - SensoryMemoryModule
    """

    @abstractmethod
    def store(self, memory_data: Dict[str, Any]) -> str:
        """
        Stores a memory record.

        Args:
            memory_data: Memory data to store

        Returns:
            Unique memory ID
        """
        pass

    @abstractmethod
    def retrieve(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific memory by ID.

        Args:
            memory_id: Unique memory identifier

        Returns:
            Memory data or None if not found
        """
        pass

    @abstractmethod
    def query(
        self,
        filters: Dict[str, Any],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Queries memories with filters."""
        pass

    @abstractmethod
    def semantic_search(
        self,
        query_text: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs vector search based on meaning.
        
        Args:
            query_text: The natural language query
            limit: Maximum results
            filters: Optional metadata filters
        """
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        Deletes a memory record.

        Args:
            memory_id: ID of memory to delete

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def get_storage_type(self) -> str:
        """
        Returns storage type identifier.

        Returns:
            One of: 'episodic', 'semantic', 'sensory'
        """
        pass
