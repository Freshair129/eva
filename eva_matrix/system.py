"""
EVA Matrix System - Psychological State Engine.
"""

import logging
import yaml
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from eva_matrix.modules.psych_engine import MatrixPsychEngine

logger = logging.getLogger(__name__)

class EVAMatrixSystem:
    """
    Role: Authority for Psychological State (9D Matrix).
    Responsibility: Owns state, manages persistence, subscribes to Bus.
    """
    
    def __init__(self, base_path: Path = None, msp=None, bus=None):
        self.base_path = base_path or Path(".")
        self.msp = msp
        self.bus = bus
        
        # 1. Load Config
        self.config_path = self.base_path / "eva_matrix/configs/EVA_Matrix_configs.yaml"
        self.config = self._load_config()
        
        # 2. Setup Persistence
        persistence_subpath = self.config.get("runtime_hook", {}).get(
            "persistence_file", "consciousness/state/psychological/current.json"
        )
        self.state_file = self.base_path / Path(persistence_subpath)
        
        # 3. Initialize Internal State
        self.axes_9d = {
            "stress": 0.5, "warmth": 0.5, "drive": 0.5, "clarity": 0.5, "joy": 0.5,
            "stability": 0.5, "orientation": 0.5,
            "primary": "Neutral", "secondary": "Neutral"
        }
        self.momentum = {"intensity": 0.1}
        self.emotion_label = "Neutral"
        
        self._load_state()
        
        # 4. Init Logic Engine
        self.psych_engine = MatrixPsychEngine(self.config)
        
        # 5. Subscribe to Bus (Phase 3 Integration)
        if self.bus:
            # P0-004 IBus defines subscribe(channel, handler)
            self.bus.subscribe("bus:physical", self._on_physical_signal)
            
        logger.info("[EVA Matrix] System Initialized (5+2+2 Model)")

    def _load_config(self) -> Dict[str, Any]:
        """Loads YAML configuration."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                return {}
        logger.warning(f"Config not found at {self.config_path}")
        return {}

    def _on_physical_signal(self, payload: Dict[str, Any]):
        """Handler for 'bus:physical' signals (from PhysioCore)."""
        # Payload depends on Physio implementation.
        # Assuming payload has 'hormones' dict or similar.
        # Per eva_matrix.py source: payload.get("receptor_signals", {})
        
        # For Phase 2/3 transition, we might get simplified payload
        # For Phase 4, PhysioCore sends: { "impact": {...}, "state_snapshot": {"hormones": {...}} }
        hormones = payload.get("hormones", {})
        
        if not hormones:
            # Check state_snapshot (Full state)
            snapshot = payload.get("state_snapshot", {})
            hormones = snapshot.get("hormones", {})
            
        if not hormones:
            # Check impact (Delta only)
            hormones = payload.get("impact", {})
            
        if not hormones:
            # Legacy Phase 2/3
            hormones = payload.get("receptor_signals", {})
            
        if hormones:
            self.process_signals(hormones)

    def process_signals(self, signals: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Process neural signals and update state.
        """
        # 1. Delegate to Logic Engine
        result = self.psych_engine.calculate_transition(
            self.axes_9d, 
            self.momentum, 
            signals or {}
        )
        
        # 2. Update Internal State
        self.axes_9d = result.get("axes_9d", {})
        self.emotion_label = result.get("emotion_label", "Neutral")
        self.momentum = result.get("momentum", {})
        
        # 3. Publish to Bus
        if self.bus:
            matrix_payload = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "emotions": {
                    "valence": self.axes_9d.get("joy", 0.5), # approx
                    "arousal": self.axes_9d.get("stress", 0.5), # approx
                    "dominance": self.axes_9d.get("drive", 0.5), # approx
                    # Full 9D exposed as well
                    "axes_9d": self.axes_9d 
                },
                "mood": f"{self.emotion_label}_{self.axes_9d.get('primary', 'Neutral')}",
                "primary_emotion": self.axes_9d.get("primary", "Neutral"),
                "secondary_emotion": self.axes_9d.get("secondary", "Neutral"),
                "momentum": self.momentum,
                "source": "eva_matrix_system"
            }
            self.bus.publish("bus:psychological", matrix_payload)

        # 4. Save State
        self._save_state()
        
        return result

    def _save_state(self):
        """Saves current state to persistence file."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Save in format expected by Consciousness Domain/Loader
            data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "emotions": {
                    "valence": self.axes_9d.get("joy"),
                    "arousal": self.axes_9d.get("stress"),
                    "dominance": self.axes_9d.get("drive")
                },
                "axes_9d": self.axes_9d, # Extended
                "mood": self.emotion_label,
                "primary_emotion": self.axes_9d.get("primary"),
                "secondary_emotion": self.axes_9d.get("secondary"),
                "momentum": self.momentum,
                "source": "eva_matrix_system"
            }
            
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"[EVA Matrix] Error saving state: {e}")

    def _load_state(self):
        """Loads state from persistence file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Support both simple structure (if manually edited) and full structure
                    if "axes_9d" in data:
                        self.axes_9d = data["axes_9d"]
                    if "mood" in data:
                        self.emotion_label = data["mood"]
                    if "momentum" in data:
                        self.momentum = data["momentum"]
            except Exception as e:
                logger.error(f"[EVA Matrix] Error loading state: {e}")
