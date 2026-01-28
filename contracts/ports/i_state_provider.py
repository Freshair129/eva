from abc import ABC, abstractmethod
from typing import Dict, Any

class IStateProvider(ABC):
    """
    Port interface for systems that provide state snapshots.

    Implementors:
    - MockPhysioProvider (Phase 1)
    - MockMatrixProvider (Phase 1)
    - PhysioCore (Phase 4)
    - EVAMatrix (Phase 3)
    """

    @abstractmethod
    def get_current_state(self) -> Dict[str, Any]:
        """
        Returns current system state snapshot.

        Returns:
            Dict containing:
            - timestamp: ISO format string
            - state data specific to the system
            - source: identifier string
        """
        pass

    @abstractmethod
    def get_state_type(self) -> str:
        """
        Returns the type of state this provider gives.

        Returns:
            One of: 'physical', 'psychological', 'phenomenological'
        """
        pass

    @abstractmethod
    def get_provider_id(self) -> str:
        """
        Returns unique identifier for this provider.
        """
        pass
