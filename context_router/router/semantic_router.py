"""Semantic similarity router."""
from __future__ import annotations

from context_router.context.context_types import ScoredContextItem
from context_router.context.memory_store import MemoryStore
from context_router.router.base import BaseRouter
from context_router.scoring.relevance import EmbeddingModel, HashingEmbeddingModel, relevance_scores


class SemanticRouter(BaseRouter):
    """Return nearest context items by embedding similarity.

    By default this uses a deterministic local hashing model. Pass a sentence-transformers
    model from ``load_sentence_transformer()`` for production-grade embeddings.
    """

    name = "semantic"

    def __init__(self, store: MemoryStore, top_k: int = 5, model: EmbeddingModel | None = None) -> None:
        super().__init__(store, top_k)
        self.model = model or HashingEmbeddingModel()

    def route(self, query: str) -> list[ScoredContextItem]:
        items = self.store.all()
        scores = relevance_scores(query, [item.text for item in items], self.model)
        scored = [ScoredContextItem(item=item, score=score, scores={"semantic": score}) for item, score in zip(items, scores)]
        return sorted(scored, key=lambda item: item.score, reverse=True)[: self.top_k]
