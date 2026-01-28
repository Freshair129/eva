from datetime import datetime
from typing import Dict, Any
from contracts.ports.i_state_provider import IStateProvider


class MockPhysioProvider(IStateProvider):
    """
    Mock implementation of PhysioCore for Phase 1.
    Returns neutral baseline biological state.
    """

    def get_current_state(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "hormones": {
                "dopamine": 0.5,
                "serotonin": 0.5,
                "cortisol": 0.3,
                "oxytocin": 0.4,
                "adrenaline": 0.2,
                "noradrenaline": 0.2,
                "gaba": 0.5,
                "acetylcholine": 0.5,
                "endorphin": 0.3,
                "melatonin": 0.3,
            },
            "vitals": {
                "heart_rate": 72,
                "breathing_rate": 14,
                "temperature": 36.6,
                "blood_pressure": {"systolic": 120, "diastolic": 80},
            },
            "source": "mock_physio_v1",
        }

    def get_state_type(self) -> str:
        return "physical"

    def get_provider_id(self) -> str:
        return "mock_physio_provider"


class MockMatrixProvider(IStateProvider):
    """
    Mock implementation of EVA Matrix for Phase 1.
    Returns neutral emotional baseline.
    """

    def get_current_state(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "dimensions": {
                "valence": 0.5,       # Neutral (not happy/sad)
                "arousal": 0.4,       # Calm
                "dominance": 0.5,     # Neutral control
                "curiosity": 0.6,     # Slightly curious
                "trust": 0.5,         # Neutral trust
                "anticipation": 0.5,  # Neutral
                "surprise": 0.3,      # Low surprise
                "fear": 0.2,          # Low fear
                "sadness": 0.2,       # Low sadness
            },
            "mood": "neutral",
            "dominant_emotion": None,
            "source": "mock_matrix_v1",
        }

    def get_state_type(self) -> str:
        return "psychological"

    def get_provider_id(self) -> str:
        return "mock_matrix_provider"


class MockQualiaProvider(IStateProvider):
    """
    Mock implementation of Artifact Qualia for Phase 1.
    Returns neutral phenomenological state.
    """

    def get_current_state(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "texture": "smooth",
            "color": "#808080",  # Gray
            "soundscape": "quiet",
            "temperature_feel": "neutral",
            "source": "mock_qualia_v1",
        }

    def get_state_type(self) -> str:
        return "phenomenological"

    def get_provider_id(self) -> str:
        return "mock_qualia_provider"
