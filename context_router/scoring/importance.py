"""Importance scoring."""
from __future__ import annotations

from context_router.context.context_types import ContextItem


def importance_score(item: ContextItem) -> float:
    """Return normalized importance already stored on the item."""
    return max(0.0, min(1.0, item.importance))
