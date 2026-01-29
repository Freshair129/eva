"""
GKS System - The Wisdom Controller.
Exposes the Knowledge Graph to the Orchestrator/CIM.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from .modules.loader import GKSLoader
from .modules.graph import KnowledgeGraph

logger = logging.getLogger(__name__)

class GKSSystem:
    """
    Main interface for accessing EVA's Knowledge Base.
    """
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(".")
        
        # Default library path (Updated key from user info: e:\The Human Algorithm\T2\agent\memory_n_soul_passport\schema)
        # But we might need to be flexible. Let's try to find it.
        # Ideally, we look in e:\eva\gks\knowledge_base first (local), then external if configured.
        
        self.library_path = self.base_path / "gks" / "knowledge_base"
        
        # 1. Init Loader & Graph
        self.loader = GKSLoader(self.library_path)
        self.graph = KnowledgeGraph()
        
        # 2. auto-load if exists
        if self.library_path.exists():
            self._initialize_graph()
        else:
            logger.warning(f"[GKS] Knowledge Base not found at {self.library_path}")

    def _initialize_graph(self):
        """Loads all blocks and builds the graph."""
        blocks = self.loader.scan_library()
        self.graph.build_from_cache(blocks)
        logger.info(f"[GKS] Graph built with {len(self.graph.nodes)} nodes.")

    def query(self, topic: str) -> Dict[str, Any]:
        """
        Semantic search for knowledge.
        Returns formatted context for LLM.
        """
        results = self.graph.search(topic)
        
        context = {
            "query": topic,
            "hits": [],
            "summary": f"Found {len(results)} related blocks."
        }
        
        # Limit hits to top 3
        for node_id in results[:3]:
            data = self.graph.nodes.get(node_id)
            context["hits"].append({
                "id": node_id,
                "content": data
            })
            
        return context
        
    def get_provider_id(self) -> str:
        return "gks_wisdom"
