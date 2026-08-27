"""Registry of available skills."""

from typing import Dict, List, Type

from agent.skills.skill_base import SkillBase


class SkillRegistry:
    """A lightweight registry for skills."""

    def __init__(self):
        self.skills: Dict[str, Type[SkillBase]] = {}

    def register(self, skill_class: Type[SkillBase]) -> None:
        """Register a skill class by its class-level name."""
        self.skills[skill_class.name] = skill_class

    def list(self) -> List[str]:
        """Return names of loaded skills."""
        return sorted(self.skills.keys())

    def get(self, name: str) -> Type[SkillBase]:
        """Return a registered skill class."""
        if name not in self.skills:
            raise KeyError(f"Skill '{name}' is not registered.")
        return self.skills[name]
