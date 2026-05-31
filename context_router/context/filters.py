"""Filtering helpers for context item collections."""
from __future__ import annotations

from datetime import datetime, timezone

from context_router.context.context_types import ContextItem


def _normalize_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def filter_context_items(
    items: list[ContextItem],
    *,
    category: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    min_importance: float | None = None,
) -> list[ContextItem]:
    """Filter context items by category, time window, and minimum importance."""
    normalized_start = _normalize_timestamp(start) if start is not None else None
    normalized_end = _normalize_timestamp(end) if end is not None else None

    filtered: list[ContextItem] = []
    for item in items:
        if category is not None and item.category != category:
            continue
        if normalized_start is not None and item.timestamp < normalized_start:
            continue
        if normalized_end is not None and item.timestamp > normalized_end:
            continue
        if min_importance is not None and item.importance < min_importance:
            continue
        filtered.append(item)
    return filtered
