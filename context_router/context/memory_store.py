"""In-memory context store."""
from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from .context_types import ContextItem


class MemoryStore:
    """Simple in-memory store for ContextItem objects."""

    def __init__(self, items: Iterable[ContextItem] | None = None) -> None:
        self._items: list[ContextItem] = list(items or [])

    def add(self, item: ContextItem) -> None:
        self._items.append(item)

    def search(self, query: str) -> list[ContextItem]:
        terms = {term.lower() for term in query.split()}
        return [item for item in self._items if terms & set(item.text.lower().split())]

    def get_recent(self, top_k: int = 5) -> list[ContextItem]:
        return sorted(self._items, key=lambda item: item.timestamp, reverse=True)[:top_k]

    def get_by_category(self, category: str, top_k: int | None = None) -> list[ContextItem]:
        matches = [item for item in self._items if item.category == category]
        matches.sort(key=lambda item: item.timestamp, reverse=True)
        return matches if top_k is None else matches[:top_k]

    def all(self) -> list[ContextItem]:
        return list(self._items)

    def latest_timestamp(self) -> datetime | None:
        if not self._items:
            return None
        return max(item.timestamp for item in self._items)
