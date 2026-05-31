"""Recency-based router."""
from __future__ import annotations

from context_router.context.context_types import ScoredContextItem
from context_router.context.memory_store import MemoryStore
from context_router.scoring.recency import recency_score


class RecencyRouter:
    """Return the most recent memories."""

    name = "recency"

    def __init__(self, store: MemoryStore, top_k: int = 5) -> None:
        self.store = store
        self.top_k = top_k

    def route(self, query: str) -> list[ScoredContextItem]:
        items = self.store.get_recent(self.top_k)
        return [ScoredContextItem(item=item, score=recency_score(item), scores={"recency": recency_score(item)}) for item in items]
