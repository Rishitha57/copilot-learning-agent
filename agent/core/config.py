"""Configuration defaults for the agent project."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AgentConfig:
    """Simple application config object."""

    name: str = "capstone-agent"
    mode: str = "create"
    enable_memory: bool = True
    enable_skills: bool = True
    allowed_tools: List[str] = None

    def __post_init__(self):
        if self.allowed_tools is None:
            self.allowed_tools = ["search", "calculator"]

    def as_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "mode": self.mode,
            "enable_memory": self.enable_memory,
            "enable_skills": self.enable_skills,
            "allowed_tools": self.allowed_tools,
        }
