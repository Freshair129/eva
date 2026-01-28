"""Sensory Memory Schema - Perceptual data and Qualia."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


@dataclass
class Qualia:
    """Subjective sensory experience (Phenomenological state)."""
    color_hex: str = "#808080"
    texture: str = "neutral"
    soundscape: Optional[str] = None
    temperature_feel: str = "neutral"
    intensity: float = 0.5  # 0.0 - 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Qualia":
        return cls(**data)


@dataclass
class SensoryMemory:
    """
    Represents a sensory memory record (File-per-Record).
    Captures what was perceived and how it felt subjectiveley.
    
    File location: turns/sensory/{year}/{month}/{sensory_id}.json
    """
    sensory_id: str
    episode_id: str  # Link to the episode where this was perceived
    
    data_type: str  # image, audio, visual_pattern, text_visual
    raw_data_ref: Optional[str] = None  # URI or relative path to raw asset
    
    # Perceptual qualities
    qualia: Optional[Qualia] = None
    extracted_features: Dict[str, Any] = field(default_factory=dict)
    
    # Crosslinks
    concept_refs: List[str] = field(default_factory=list)  # Link to Semantic Memory ["sem_xxx"]
    
    # Biological state at time of perception
    physio_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    source: str = "perception"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensory_id": self.sensory_id,
            "episode_id": self.episode_id,
            "data_type": self.data_type,
            "raw_data_ref": self.raw_data_ref,
            "qualia": self.qualia.to_dict() if self.qualia else None,
            "extracted_features": self.extracted_features,
            "concept_refs": self.concept_refs,
            "physio_snapshot": self.physio_snapshot,
            "created_at": self.created_at.isoformat(),
            "source": self.source,
            "type": "sensory_v1"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SensoryMemory":
        return cls(
            sensory_id=data["sensory_id"],
            episode_id=data["episode_id"],
            data_type=data["data_type"],
            raw_data_ref=data.get("raw_data_ref"),
            qualia=Qualia.from_dict(data["qualia"]) if data.get("qualia") else None,
            extracted_features=data.get("extracted_features", {}),
            concept_refs=data.get("concept_refs", []),
            physio_snapshot=data.get("physio_snapshot", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            source=data.get("source", "perception")
        )

    def get_file_path(self, base_dir: str = "memory") -> Path:
        """Generate file path: {base}/turns/sensory/{year}/{month}/{sensory_id}.json"""
        dt = self.created_at
        return Path(base_dir) / "turns" / "sensory" / str(dt.year) / f"{dt.month:02d}" / f"{self.sensory_id}.json"
