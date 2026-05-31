"""Context pack returned to an agent after routing."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .context_types import ContextItem, ScoredContextItem


def estimate_tokens(text: str) -> int:
    """Lightweight token estimate used for local context budgeting."""
    return len(text.split())


def select_with_token_budget(items: list[ContextItem], max_tokens: int | None) -> list[ContextItem]:
    """Select items in order until the token budget is exhausted."""
    if max_tokens is None:
        return items
    if max_tokens < 0:
        raise ValueError("max_tokens must be non-negative")

    selected: list[ContextItem] = []
    used = 0
    for item in items:
        item_tokens = estimate_tokens(item.text)
        if used + item_tokens <= max_tokens:
            selected.append(item)
            used += item_tokens
    return selected


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
        ranked_memories = [scored.item for scored in scored_items]
        memories = select_with_token_budget(ranked_memories, max_tokens)
        selected_ids = {item.id for item in memories}
        selected_scored_items = [scored for scored in scored_items if scored.item.id in selected_ids]
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
                "estimated_tokens": sum(estimate_tokens(item.text) for item in memories),
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
