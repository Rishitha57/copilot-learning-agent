"""Tool interface and basic tools for the agent."""

from typing import Any, Dict, List


class Tool:
    """Minimal tool abstraction."""

    name: str = "tool"

    def run(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {"tool": self.name, "status": "ok", "args": args, "kwargs": kwargs}


class SearchTool(Tool):
    """Example search-like tool."""

    name = "search"

    def run(self, query: str, limit: int = 5) -> Dict[str, Any]:
        return {"tool": self.name, "query": query, "limit": limit, "results": []}


class CalculatorTool(Tool):
    """Example calculator tool."""

    name = "calculator"

    def run(self, expression: str) -> Dict[str, Any]:
        return {"tool": self.name, "expression": expression, "result": eval(expression, {"__builtins__": {}}, {})}
