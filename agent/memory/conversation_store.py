"""Conversation memory store abstraction."""

from typing import Any, Dict, List, Optional


class ConversationStore:
    """Store messages for a session-aware agent conversation."""

    def __init__(self):
        self.messages: List[Dict[str, Any]] = []

    def add(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.messages.append({"role": role, "content": content, "metadata": metadata or {}})

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit is None:
            return list(self.messages)
        return list(self.messages[-limit:])

    def clear(self) -> None:
        self.messages.clear()
