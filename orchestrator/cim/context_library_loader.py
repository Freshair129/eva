"""Context Library Loader - Modular context loading from file system."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ContextLibraryLoader:
    """
    Loads context from the context_library folder structure.
    
    Structure:
    - identity/: Static persona (always loaded)
    - state/: Dynamic state from Bus
    - knowledge/: Domain-specific knowledge (selective)
    - prompts/: Reusable prompt fragments
    """

    def __init__(self, library_path: str = "consciousness"):
        self._library_path = Path(library_path)
        self._cache: Dict[str, str] = {}

    # =========================================================================
    # IDENTITY (Always Loaded)
    # =========================================================================

    def load_identity(self) -> str:
        """Load all identity files."""
        identity_path = self._library_path / "identity"
        parts = []

        for file in ["core.md", "voice.md", "constitution.md"]:
            content = self._read_file(identity_path / file)
            if content:
                parts.append(content)

        return "\n\n---\n\n".join(parts)

    # =========================================================================
    # STATE (Loaded from files, refreshed from Bus)
    # =========================================================================

    def load_state(self) -> Dict[str, Any]:
        """Load current state from JSON files."""
        state_path = self._library_path / "state"
        state = {}

        for channel in ["physical", "psychological", "phenomenological"]:
            file_path = state_path / channel / "current.json"
            content = self._read_json(file_path)
            if content:
                state[f"bus:{channel}"] = content

        return state

    def update_state(self, channel: str, data: Dict[str, Any]) -> None:
        """Write state update to file (called by Bus integration)."""
        channel_name = channel.replace("bus:", "")
        file_path = self._library_path / "state" / channel_name / "current.json"
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"Failed to update state file: {e}")

    # =========================================================================
    # KNOWLEDGE (Selective Loading)
    # =========================================================================

    def load_knowledge(self, keywords: Optional[List[str]] = None) -> str:
        """Load knowledge files based on keywords."""
        knowledge_path = self._library_path / "knowledge"
        parts = []

        # Always load user profile and project context
        for file in ["user_profile.md", "project_context.md"]:
            content = self._read_file(knowledge_path / file)
            if content:
                parts.append(content)

        # Load domain knowledge if keywords match
        if keywords:
            domain_path = knowledge_path / "domain"
            if domain_path.exists():
                for domain_file in domain_path.glob("*.md"):
                    domain_name = domain_file.stem.lower()
                    # Check if any keyword matches the domain
                    for kw in keywords:
                        if kw.lower() in domain_name or domain_name in kw.lower():
                            content = self._read_file(domain_file)
                            if content:
                                parts.append(content)
                            break

        return "\n\n---\n\n".join(parts)

    # =========================================================================
    # PROMPTS (Always Loaded)
    # =========================================================================

    def load_prompts(self) -> Dict[str, str]:
        """Load all prompt fragments."""
        prompts_path = self._library_path / "prompts"
        prompts = {}

        for file in ["system_prefix.md", "bio_digital_gap.md", "response_guidelines.md"]:
            content = self._read_file(prompts_path / file)
            if content:
                prompts[file.replace(".md", "")] = content

        return prompts

    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================

    def _read_file(self, path: Path) -> Optional[str]:
        """Read a text file and cache it."""
        cache_key = str(path)
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                self._cache[cache_key] = content
                return content
        except Exception as e:
            logger.error(f"Failed to read {path}: {e}")

        return None

    def _read_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """Read a JSON file."""
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read JSON {path}: {e}")

        return None

    def clear_cache(self) -> None:
        """Clear the file cache."""
        self._cache.clear()


# Singleton instance for convenience
_default_loader: Optional[ContextLibraryLoader] = None


def get_context_library(library_path: str = "consciousness") -> ContextLibraryLoader:
    """Get or create the default context library loader."""
    global _default_loader
    if _default_loader is None:
        _default_loader = ContextLibraryLoader(library_path)
    return _default_loader
