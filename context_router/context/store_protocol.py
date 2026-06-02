"""Protocol for context stores used by routers."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from context_router.context.context_types import ContextItem


@runtime_checkable
class ContextStoreProtocol(Protocol):
    """Structural interface shared by in-memory and durable context stores."""

    def add(self, item: ContextItem) -> None:
        """Add or update a context item."""

    def all(self) -> list[ContextItem]:
        """Return all stored context items."""

    def search(self, query: str) -> list[ContextItem]:
        """Return context items matching a query."""

    def get_recent(self, top_k: int = 5) -> list[ContextItem]:
        """Return the most recent context items."""

    def get_by_category(self, category: str, top_k: int | None = None) -> list[ContextItem]:
        """Return context items in a category."""
