"""Skill interface used by the CREATE-style agent."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class SkillBase(ABC):
    """Base contract for all reusable skills."""

    name: str = "skill"

    @abstractmethod
    def execute(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the skill and return a model-friendly response."""
        raise NotImplementedError
