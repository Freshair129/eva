"""Semantic Memory Schema - Factual knowledge."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4


@dataclass
class SemanticMemory:
    """
    Represents factual knowledge.

    Semantic memories are "what I know" memories:
    - Facts about users
    - Learned information
    - Conceptual knowledge

    Attributes:
        id: Unique identifier
        subject: What/who this fact is about
        predicate: The relationship or property
        object: The value or target
        confidence: How certain we are (0.0-1.0)
        source: Where this fact came from
        learned_at: When this was learned
        last_accessed: Last time this fact was recalled
        access_count: How many times recalled
    """

    subject: str
    predicate: str
    object: str

    id: str = field(default_factory=lambda: f"sem_{uuid4().hex[:8]}")
    confidence: float = 0.8
    source: str = "conversation"
    learned_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None
    access_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "confidence": self.confidence,
            "source": self.source,
            "learned_at": self.learned_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "access_count": self.access_count,
            "type": "semantic"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SemanticMemory":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            subject=data["subject"],
            predicate=data["predicate"],
            object=data["object"],
            confidence=data.get("confidence", 0.8),
            source=data.get("source", "conversation"),
            learned_at=datetime.fromisoformat(data["learned_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            access_count=data.get("access_count", 0)
        )

    def as_triple(self) -> str:
        """Return as subject-predicate-object string."""
        return f"{self.subject} {self.predicate} {self.object}"
