"""Base agent runtime and request handling."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentInput:
    """Structured input accepted by the agent."""

    prompt: str
    context: Optional[Dict[str, Any]] = None


class Agent:
    """Minimal CREATE-style agent shell.

    The class is intentionally lightweight and can be extended with a
    planner, reasoning engine, tool runner, and memory accessors.
    """

    def __init__(self, name: str = "capstone-agent", config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}

    def run(self, input_data: AgentInput) -> Dict[str, Any]:
        """Return a simple response envelope for an input prompt."""
        return {
            "agent": self.name,
            "input": input_data.prompt,
            "context": input_data.context or {},
            "response": f"Handled by {self.name}.",
        }
