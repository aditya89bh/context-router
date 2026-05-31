"""Shared router interface for all context routing strategies."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from context_router.context.context_types import ScoredContextItem
from context_router.context.memory_store import MemoryStore


class BaseRouter(ABC):
    """Common contract implemented by every context router.

    A router receives a user or agent query and returns ranked context items.
    Keeping one interface makes routers swappable in demos, tests, and future
    agent frameworks.
    """

    name: ClassVar[str] = "base"

    def __init__(self, store: MemoryStore, top_k: int = 5) -> None:
        self.store = store
        self.top_k = top_k

    @abstractmethod
    def route(self, query: str) -> list[ScoredContextItem]:
        """Return ranked context items for a query."""
        raise NotImplementedError
