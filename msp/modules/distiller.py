"""
Wisdom Distiller - Memory Compression Engine (Canonical 8-8-8 Protocol).
Handles the transition: 8 Sessions -> 1 Core -> 8 Cores -> 1 Sphere.
"""

import logging
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class WisdomDistiller:
    """
    Implements Pillar 5: Tiered Wisdom (8-8-8) per MEM_PHILOSOPHY_888.md
    
    Tiers:
    1. Session Memory: Raw snapshots of consciousness after each session.
    2. Core Memory: Narrative Arcs distilled from 8 Sessions.
    3. Sphere Memory: Wisdom/Identity DNA distilled from 8 Cores.
    """
    
    def __init__(self, msp_engine):
        self.msp = msp_engine
        self.base_dir = Path(msp_engine.base_dir)
        self.session_dir = self.base_dir / "session_memory"
        self.core_dir = self.base_dir / "core_memory"
        self.sphere_dir = self.base_dir / "sphere_memory"
        
        # Ensure directories exist
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.core_dir.mkdir(parents=True, exist_ok=True)
        self.sphere_dir.mkdir(parents=True, exist_ok=True)
        
        # Thresholds per spec
        self.SESSIONS_PER_CORE = 8
        self.CORES_PER_SPHERE = 8
        
    def check_and_distill(self):
        """
        Main entry point for distillation logic. 
        Usually triggered at the end of a session.
        """
        # 1. Distill Sessions to Core
        sessions = self._get_pending_units(self.session_dir, "session")
        if len(sessions) >= self.SESSIONS_PER_CORE:
            self._distill_sessions_to_core(sessions[:self.SESSIONS_PER_CORE])
            
        # 2. Distill Cores to Sphere
        cores = self._get_pending_units(self.core_dir, "core")
        if len(cores) >= self.CORES_PER_SPHERE:
            self._distill_cores_to_sphere(cores[:self.CORES_PER_SPHERE])

    def _get_pending_units(self, directory: Path, prefix: str) -> List[Path]:
        """Returns units that haven't been distilled yet (placeholder logic)."""
        if not directory.exists(): return []
        # For now, just list all and we assume we take the oldest 8.
        # In a real system, we'd mark them as 'archived'/ 'processed'.
        return sorted(list(directory.glob(f"{prefix}_*.json")))

    def _distill_sessions_to_core(self, session_paths: List[Path]):
        """
        8 Sessions -> 1 Core (Narrative Arc)
        Distillation Pillars: Clean, Summary, Index, Relation.
        """
        logger.info(f"[8-8-8] Distilling {len(session_paths)} sessions into 1 Core Memory...")
        
        # Placeholder: Extracting text from sessions
        combined_text = ""
        for p in session_paths:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    combined_text += f"\n--- Session {p.stem} ---\n" + f.read()
            except Exception: pass

        # Distillation (Mock)
        core_id = f"core_{len(list(self.core_dir.glob('core_*.json'))) + 1:03d}"
        core_content = {
            "id": core_id,
            "type": "core_narrative",
            "source_sessions": [p.stem for p in session_paths],
            "distillation": {
                "summary": f"Distilled narrative arc from {len(session_paths)} sessions.",
                "pillars": ["clean", "summary", "index", "relation"]
            }
        }
        
        # Save Core
        with open(self.core_dir / f"{core_id}.json", "w", encoding="utf-8") as f:
            json.dump(core_content, f, indent=2)
            
        logger.info(f"[8-8-8] Core created: {core_id}")

    def _distill_cores_to_sphere(self, core_paths: List[Path]):
        """
        8 Cores -> 1 Sphere (Wisdom / Identity DNA)
        """
        logger.info(f"[8-8-8] Distilling {len(core_paths)} cores into 1 Sphere Memory...")
        
        sphere_id = f"sphere_{len(list(self.sphere_dir.glob('sphere_*.json'))) + 1:03d}"
        sphere_content = {
            "id": sphere_id,
            "type": "wisdom_dna",
            "source_cores": [p.stem for p in core_paths],
            "distillation": {
                "wisdom": "Crystallized behavioral patterns and belief updates.",
                "epistemic_state": "Confirmed"
            }
        }
        
        with open(self.sphere_dir / f"{sphere_id}.json", "w", encoding="utf-8") as f:
            json.dump(sphere_content, f, indent=2)
            
        logger.info(f"[8-8-8] Sphere created (Wisdom DNA): {sphere_id}")
