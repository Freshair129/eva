"""
Memory Tools - MSP integration for memory operations.
Security Level: L1 (Safe - Auto-execute)
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


def recall_memory(
    query: str,
    type: str = "all",
    limit: int = 5,
    msp = None
) -> List[Dict[str, Any]]:
    """
    Retrieves relevant episodic or semantic memories.
    
    Args:
        query: Search query string
        type: Memory type filter ("episodic", "semantic", "all")
        limit: Maximum number of results
        msp: MSP instance (injected at runtime)
        
    Returns:
        List of memory dictionaries with content and metadata
    """
    if msp is None:
        logger.warning("MSP not available for recall_memory")
        return []
    
    results = []
    
    try:
        if type in ["episodic", "all"]:
            # Search episodic memories
            episodes = msp.search_episodic(query, limit=limit)
            for ep in episodes:
                results.append({
                    "type": "episodic",
                    "id": ep.get("episode_id", "unknown"),
                    "content": ep.get("summary", ""),
                    "context": ep.get("situation_context", ""),
                    "timestamp": ep.get("timestamp", ""),
                    "relevance": ep.get("score", 0.0)
                })
                
        if type in ["semantic", "all"]:
            # Search semantic memories
            facts = msp.search_semantic(query, limit=limit)
            for fact in facts:
                results.append({
                    "type": "semantic",
                    "id": fact.get("fact_id", "unknown"),
                    "content": fact.get("statement", ""),
                    "subject": fact.get("subject", ""),
                    "timestamp": fact.get("timestamp", ""),
                    "relevance": fact.get("score", 0.0)
                })
                
        # Sort by relevance
        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        return results[:limit]
        
    except Exception as e:
        logger.error(f"Error in recall_memory: {e}")
        return []


def save_memory(
    content: str,
    type: str = "episodic",
    importance: float = 0.5,
    msp = None,
    context: str = ""
) -> str:
    """
    Explicitly saves a new memory or fact.
    
    Args:
        content: The memory content to save
        type: Memory type ("episodic" or "semantic")
        importance: Importance score (0.0 - 1.0)
        msp: MSP instance (injected at runtime)
        context: Additional context for the memory
        
    Returns:
        Memory ID of the saved record
    """
    if msp is None:
        logger.warning("MSP not available for save_memory")
        return "error:no_msp"
    
    try:
        if type == "episodic":
            # Store as episodic memory
            memory_id = msp.store_episode(
                summary=content,
                context=context or "Explicitly saved memory",
                importance=importance
            )
        elif type == "semantic":
            # Store as semantic fact
            memory_id = msp.store_fact(
                statement=content,
                subject=context or "general",
                confidence=importance
            )
        else:
            logger.warning(f"Unknown memory type: {type}")
            return f"error:invalid_type:{type}"
            
        logger.info(f"Saved {type} memory: {memory_id}")
        return memory_id
        
    except Exception as e:
        logger.error(f"Error in save_memory: {e}")
        return f"error:{str(e)}"
