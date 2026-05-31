"""Recency scoring utilities."""
from __future__ import annotations

from datetime import datetime, timezone

from context_router.context.context_types import ContextItem


def recency_score(item: ContextItem, *, now: datetime | None = None, half_life_hours: float = 72.0) -> float:
    """Exponential decay recency score in [0, 1]."""
    if half_life_hours <= 0:
        raise ValueError("half_life_hours must be positive")
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    age_hours = max(0.0, (now - item.timestamp).total_seconds() / 3600)
    return 0.5 ** (age_hours / half_life_hours)
