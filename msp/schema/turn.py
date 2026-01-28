"""Turn Schema - User and LLM turn records (File-per-Record)."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


@dataclass
class TurnUser:
    """
    User's turn in a conversation.
    Stored as individual file: turns/user/{year}/{month}/{turn_id}.json
    """
    turn_id: str
    episode_id: str  # Foreign key to Episode
    
    speaker: str = "user"
    username: Optional[str] = None
    user_id: Optional[str] = None
    text_excerpt: str = ""
    emotion_signal: Optional[str] = None
    intent: Optional[str] = None
    salience_anchor: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "episode_id": self.episode_id,
            "speaker": self.speaker,
            "username": self.username,
            "user_id": self.user_id,
            "text_excerpt": self.text_excerpt,
            "emotion_signal": self.emotion_signal,
            "intent": self.intent,
            "salience_anchor": self.salience_anchor,
            "created_at": self.created_at.isoformat(),
            "type": "turn_user"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TurnUser":
        return cls(
            turn_id=data["turn_id"],
            episode_id=data["episode_id"],
            speaker=data.get("speaker", "user"),
            username=data.get("username"),
            user_id=data.get("user_id"),
            text_excerpt=data.get("text_excerpt", ""),
            emotion_signal=data.get("emotion_signal"),
            intent=data.get("intent"),
            salience_anchor=data.get("salience_anchor", []),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        )

    def get_file_path(self, base_dir: str = "memory") -> Path:
        """Generate file path: {base}/turns/user/{year}/{month}/{turn_id}.json"""
        dt = self.created_at
        return Path(base_dir) / "turns" / "user" / str(dt.year) / f"{dt.month:02d}" / f"{self.turn_id}.json"


@dataclass
class TurnLLM:
    """
    LLM's turn in a conversation.
    Stored as individual file: turns/llm/{year}/{month}/{turn_id}.json
    """
    turn_id: str
    episode_id: str  # Foreign key to Episode
    
    speaker: str = "llm"
    text_excerpt: str = ""
    epistemic_mode: str = "assert"  # explore, hypothesize, assert, caution, reflect
    confidence: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "episode_id": self.episode_id,
            "speaker": self.speaker,
            "text_excerpt": self.text_excerpt,
            "epistemic_mode": self.epistemic_mode,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "type": "turn_llm"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TurnLLM":
        return cls(
            turn_id=data["turn_id"],
            episode_id=data["episode_id"],
            speaker=data.get("speaker", "llm"),
            text_excerpt=data.get("text_excerpt", ""),
            epistemic_mode=data.get("epistemic_mode", "assert"),
            confidence=data.get("confidence", 0.5),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        )

    def get_file_path(self, base_dir: str = "memory") -> Path:
        """Generate file path: {base}/turns/llm/{year}/{month}/{turn_id}.json"""
        dt = self.created_at
        return Path(base_dir) / "turns" / "llm" / str(dt.year) / f"{dt.month:02d}" / f"{self.turn_id}.json"
