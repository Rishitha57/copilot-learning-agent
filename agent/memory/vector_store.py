"""Vector memory store abstraction.

This file is intentionally dependency-light and can be backed by a real
embeddings provider or local vector database in a production implementation.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple


class VectorStore:
    """In-memory vector index abstraction."""

    def __init__(self):
        self._items: List[Dict[str, Any]] = []

    def add(self, vector: Sequence[float], metadata: Optional[Dict[str, Any]] = None) -> None:
        self._items.append({"vector": list(vector), "metadata": metadata or {}})

    def search(self, vector: Sequence[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Return nearest matches by simple Euclidean distance in a vector."""
        if not self._items:
            return []

        similarities = []
        for item in self._items:
            dist = sum((a - b) ** 2 for a, b in zip(vector, item["vector"]))
            similarities.append((dist, item))

        similarities.sort(key=lambda item: item[0])
        return [item[1] for item in similarities[:top_k]]

    def clear(self) -> None:
        self._items.clear()
