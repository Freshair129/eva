"""Episodic Memory Schema - File-per-Record Architecture."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


@dataclass
class SituationContext:
    """Context of the interaction."""
    context_id: str
    interaction_mode: str  # small_talk, deep_discussion, etc.
    stakes_level: str      # low, medium, high
    time_pressure: str     # low, medium, high
    
    # Enhanced Context
    location_context: Optional[str] = None  # local_dev, mobile_ssh, cloud_prod
    domain_area: Optional[str] = None       # coding, music_analysis
    mission_goal: Optional[str] = None      # "Apply for job" (Macro goal)
    agent_role: Optional[str] = None        # "Senior Dev", "Friend"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SituationContext":
        return cls(**data)


@dataclass
class StructuredSummary:
    """Structured summary of the episode."""
    content: str
    action_taken: str = ""
    key_outcome: str = ""
    future_implication: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructuredSummary":
        return cls(**data)


@dataclass
class EpisodicMemory:
    """
    Represents an autobiographical memory (File-per-Record).
    
    This is a lightweight metadata container.
    Actual turn content is stored separately and referenced by turn_refs.
    
    File location: episodes/{year}/{month}/{episode_id}.json
    """

    episode_id: str
    created_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    persona_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    event_id: Optional[str] = None
    
    # Turn & Sensory References (IDs only)
    turn_refs: List[str] = field(default_factory=list)     # ["TU_xxx", "TL_xxx"]
    sensory_refs: List[str] = field(default_factory=list)  # ["SMEM_xxx"]
    
    # Structure
    situation_context: Optional[SituationContext] = None
    summary: Optional[StructuredSummary] = None
    state_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    # High-Level Helpers
    tags: List[str] = field(default_factory=list)
    cues: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "episode_id": self.episode_id,
            "created_at": self.created_at.isoformat(),
            "persona_id": self.persona_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "event_id": self.event_id,
            "turn_refs": self.turn_refs,
            "sensory_refs": self.sensory_refs,
            "situation_context": self.situation_context.to_dict() if self.situation_context else None,
            "summary": self.summary.to_dict() if self.summary else None,
            "state_snapshot": self.state_snapshot,
            "tags": self.tags,
            "cues": self.cues,
            "type": "episodic_v3"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EpisodicMemory":
        """Create from dictionary."""
        return cls(
            episode_id=data["episode_id"],
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            persona_id=data.get("persona_id"),
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
            event_id=data.get("event_id"),
            turn_refs=data.get("turn_refs", []),
            sensory_refs=data.get("sensory_refs", []),
            situation_context=SituationContext.from_dict(data["situation_context"]) if data.get("situation_context") else None,
            summary=StructuredSummary.from_dict(data["summary"]) if data.get("summary") else None,
            state_snapshot=data.get("state_snapshot", {}),
            tags=data.get("tags", []),
            cues=data.get("cues", [])
        )

    def get_file_path(self, base_dir: str = "memory") -> Path:
        """Generate file path: {base}/episodes/{year}/{month}/{episode_id}.json"""
        dt = self.created_at
        return Path(base_dir) / "episodes" / str(dt.year) / f"{dt.month:02d}" / f"{self.episode_id}.json"
