"""
Knowledge Graph - Semantic Network Engine.
Manages nodes (Concepts) and edges (Relationships) in memory.
"""

from typing import Dict, Any, List, Set, Optional

class KnowledgeGraph:
    """
    In-memory graph representation of Genesis Blocks.
    """
    
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, str]] = [] # source, target, type
        self.index_by_keyword: Dict[str, List[str]] = {}
        
    def build_from_cache(self, block_cache: Dict[str, Any]):
        """
        Constructs the graph from a cache of loaded blocks.
        Parsing logic depends on Genesis Block Structure (4D).
        """
        for block_id, content in block_cache.items():
            self.add_node(block_id, content)
            
            # Extract links?
            # Looking for "related_concepts", "parent", "children" etc.
            # This logic needs to adapt to the specific JSON schema.
            # For checking, we assume standard keys if present.
            
    def add_node(self, node_id: str, data: Any):
        self.nodes[node_id] = data
        
        # Simple keywords indexing
        # Assume node_id is meaningful (e.g. "Concept_Empathy")
        keywords = node_id.lower().replace("_", " ").split()
        for k in keywords:
            if k not in self.index_by_keyword:
                self.index_by_keyword[k] = []
            self.index_by_keyword[k].append(node_id)
            
    def search(self, query: str) -> List[str]:
        """Simple keyword search."""
        query = query.lower()
        results = set()
        
        # Exact match in index
        if query in self.index_by_keyword:
            results.update(self.index_by_keyword[query])
            
        # Partial match
        for key, ids in self.index_by_keyword.items():
            if query in key:
                results.update(ids)
                
        return list(results)

    def get_related(self, node_id: str) -> List[str]:
        """Returns IDs of related nodes."""
        related = []
        for edge in self.edges:
            if edge["source"] == node_id:
                related.append(edge["target"])
            elif edge["target"] == node_id:
                related.append(edge["source"])
        return related
