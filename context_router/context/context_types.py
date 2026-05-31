"""Core context data structures."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ContextItem:
    """One retrievable memory/context unit."""

    id: str
    text: str
    timestamp: datetime
    category: str
    importance: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0 <= self.importance <= 1:
            raise ValueError("importance must be between 0 and 1")
        if self.timestamp.tzinfo is None:
            object.__setattr__(self, "timestamp", self.timestamp.replace(tzinfo=timezone.utc))


@dataclass(frozen=True)
class ScoredContextItem:
    """A context item with routing scores attached."""

    item: ContextItem
    score: float
    scores: dict[str, float] = field(default_factory=dict)
