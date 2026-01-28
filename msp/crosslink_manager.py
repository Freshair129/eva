"""Crosslink Manager - Handles bidirectional integrity between memory types."""

import logging
from typing import Dict, List, Any, Optional
from contracts.ports.i_memory_storage import IMemoryStorage

logger = logging.getLogger(__name__)

class CrosslinkManager:
    """
    Automates the synchronization of bidirectional links between 
    Episodic, Sensory, and Semantic memories.
    """

    def __init__(self, storage: IMemoryStorage):
        self.storage = storage

    def sync_links(self, memory_data: Dict[str, Any]):
        """
        Inspects memory_data and updates the reverse side of any links.
        """
        m_type = memory_data.get("type")
        
        if m_type == "sensory_v1":
            self._sync_sensory_to_episode(memory_data)
        elif m_type == "semantic":
            self._sync_semantic_to_episodes(memory_data)
        elif m_type.startswith("turn_"):
            # Future: Link turn to episode if not already handled by episode creation
            pass

    def _sync_sensory_to_episode(self, sensory_data: Dict[str, Any]):
        """Sensory (episode_id) -> Episodic (sensory_refs)"""
        ep_id = sensory_data.get("episode_id")
        sensory_id = sensory_data.get("sensory_id")
        
        if not ep_id or not sensory_id:
            return

        episode = self.storage.retrieve(ep_id)
        if episode:
            # Add sensory link to episode if missing
            refs = episode.get("sensory_refs", [])
            if sensory_id not in refs:
                refs.append(sensory_id)
                episode["sensory_refs"] = refs
                self.storage.store(episode)
                logger.debug(f"Back-linked Sensory {sensory_id} to Episode {ep_id}")

    def _sync_semantic_to_episodes(self, semantic_data: Dict[str, Any]):
        """Semantic (episode_refs) -> Episodic (semantic_refs)"""
        episode_refs = semantic_data.get("episode_refs", [])
        semantic_id = semantic_data.get("id")
        
        if not episode_refs or not semantic_id:
            return

        for ep_id in episode_refs:
            episode = self.storage.retrieve(ep_id)
            if episode:
                # Add semantic link to episode if missing
                refs = episode.get("semantic_refs", [])
                if semantic_id not in refs:
                    refs.append(semantic_id)
                    episode["semantic_refs"] = refs
                    self.storage.store(episode)
                    logger.debug(f"Back-linked Semantic {semantic_id} to Episode {ep_id}")
