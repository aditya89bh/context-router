"""Context pack returned to an agent after routing."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .context_types import ContextItem, ScoredContextItem
from .token_budget import estimate_tokens, select_with_token_budget, token_budget_metadata


def _explain_selection(scored: ScoredContextItem) -> dict[str, Any]:
    """Build a compact, human-readable explanation for one selected item."""
    score_details = scored.scores or {"final": scored.score}
    numeric_scores = {key: value for key, value in score_details.items() if isinstance(value, int | float)}
    strongest_signal = max(numeric_scores, key=numeric_scores.get) if numeric_scores else "score"
    return {
        "id": scored.item.id,
        "category": scored.item.category,
        "final_score": round(scored.score, 4),
        "strongest_signal": strongest_signal,
        "scores": {key: round(value, 4) for key, value in numeric_scores.items()},
        "reason": f"Selected from {scored.item.category} context because {strongest_signal} was the strongest routing signal.",
    }


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
        max_tokens: int | None = None,
    ) -> "ContextPack":
        selected_scored_items = select_with_token_budget(scored_items, max_tokens)
        memories = [scored.item for scored in selected_scored_items]
        summaries = [item.text for item in memories[:summary_limit]]
        explanations = [_explain_selection(scored) for scored in selected_scored_items]
        return cls(
            memories=memories,
            summaries=summaries,
            metadata={
                "query": query,
                "router": router,
                "count": len(memories),
                "available_count": len(scored_items),
                "max_tokens": max_tokens,
                **token_budget_metadata(selected_scored_items),
                "scores": [scored.scores or {"final": scored.score} for scored in selected_scored_items],
                "explanations": explanations,
            },
        )

    def summary(self) -> str:
        categories = sorted({memory.category for memory in self.memories})
        return (
            f"ContextPack(router={self.metadata.get('router')}, "
            f"items={len(self.memories)}, categories={categories})"
        )
