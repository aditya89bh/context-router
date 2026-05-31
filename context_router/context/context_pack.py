"""Context pack returned to an agent after routing."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .context_types import ContextItem, ScoredContextItem


@dataclass
class ContextPack:
    """A compact package of selected memories, summaries, and metadata."""

    memories: list[ContextItem]
    summaries: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_scored(
        cls,
        scored_items: list[ScoredContextItem],
        *,
        query: str,
        router: str,
        summary_limit: int = 3,
    ) -> "ContextPack":
        memories = [scored.item for scored in scored_items]
        summaries = [item.text for item in memories[:summary_limit]]
        return cls(
            memories=memories,
            summaries=summaries,
            metadata={
                "query": query,
                "router": router,
                "count": len(memories),
                "scores": [scored.scores or {"final": scored.score} for scored in scored_items],
            },
        )

    def summary(self) -> str:
        categories = sorted({memory.category for memory in self.memories})
        return (
            f"ContextPack(router={self.metadata.get('router')}, "
            f"items={len(self.memories)}, categories={categories})"
        )
