"""General helper utilities."""

from typing import Any, Dict, Iterable


def normalize_text(text: str) -> str:
    """Normalize whitespace in an incoming text string."""
    return " ".join(text.strip().split())


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge dictionaries without overriding keys recursively."""
    merged: Dict[str, Any] = {}
    for item in dicts:
        merged.update(item)
    return merged


def chunk_text(text: str, chunk_size: int = 200) -> Iterable[str]:
    """Yield text chunks of a desired size."""
    for index in range(0, len(text), chunk_size):
        yield text[index:index + chunk_size]
