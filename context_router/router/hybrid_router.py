"""Hybrid context router."""
from __future__ import annotations

from datetime import datetime

from context_router.context.context_types import ScoredContextItem
from context_router.context.memory_store import MemoryStore
from context_router.router.base import BaseRouter
from context_router.scoring.importance import importance_score
from context_router.scoring.recency import recency_score
from context_router.scoring.relevance import EmbeddingModel, HashingEmbeddingModel, relevance_scores


class HybridRouter(BaseRouter):
    """Combine semantic relevance, recency, and importance.

    final_score = 0.5 * semantic + 0.3 * recency + 0.2 * importance
    """

    name = "hybrid"

    def __init__(
        self,
        store: MemoryStore,
        top_k: int = 5,
        model: EmbeddingModel | None = None,
        now: datetime | None = None,
    ) -> None:
        super().__init__(store, top_k)
        self.model = model or HashingEmbeddingModel()
        self.now = now

    def route(self, query: str) -> list[ScoredContextItem]:
        items = self.store.all()
        semantic = relevance_scores(query, [item.text for item in items], self.model)
        scored: list[ScoredContextItem] = []
        for item, semantic_score in zip(items, semantic):
            recent = recency_score(item, now=self.now)
            important = importance_score(item)
            final = 0.5 * semantic_score + 0.3 * recent + 0.2 * important
            scored.append(
                ScoredContextItem(
                    item=item,
                    score=final,
                    scores={
                        "semantic": semantic_score,
                        "recency": recent,
                        "importance": important,
                        "final": final,
                    },
                )
            )
        return sorted(scored, key=lambda item: item.score, reverse=True)[: self.top_k]
