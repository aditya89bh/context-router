"""Token-budget helpers for packing routed context."""
from __future__ import annotations

from context_router.context.context_types import ScoredContextItem


def estimate_tokens(text: str) -> int:
    """Estimate token count without requiring a tokenizer dependency.

    This intentionally uses a conservative word-based approximation so the
    package stays lightweight. Production integrations can swap this with a
    model-specific tokenizer.
    """
    if not text:
        return 0
    return max(1, int(len(text.split()) * 1.3))


def select_with_token_budget(
    scored_items: list[ScoredContextItem],
    *,
    max_tokens: int,
) -> list[ScoredContextItem]:
    """Select highest-ranked context items while staying inside a token budget.

    The input should already be sorted by the router. Items that would exceed
    the remaining budget are skipped rather than truncating memory text.
    """
    if max_tokens <= 0:
        return []

    selected: list[ScoredContextItem] = []
    used_tokens = 0
    for scored in scored_items:
        item_tokens = estimate_tokens(scored.item.text)
        if used_tokens + item_tokens <= max_tokens:
            selected.append(scored)
            used_tokens += item_tokens
    return selected


def token_budget_metadata(scored_items: list[ScoredContextItem]) -> dict[str, int]:
    """Return simple token accounting for a selected context set."""
    return {
        "estimated_tokens": sum(estimate_tokens(scored.item.text) for scored in scored_items),
        "selected_items": len(scored_items),
    }
