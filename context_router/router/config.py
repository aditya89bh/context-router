"""Router configuration objects."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RouterConfig:
    """Shared configuration for router behavior."""

    top_k: int = 5
    semantic_weight: float = 0.5
    recency_weight: float = 0.3
    importance_weight: float = 0.2
    max_tokens: int | None = None

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
        weights = (self.semantic_weight, self.recency_weight, self.importance_weight)
        if any(weight < 0 for weight in weights):
            raise ValueError("router weights must be non-negative")
        if sum(weights) <= 0:
            raise ValueError("router weight sum must be greater than zero")
        if self.max_tokens is not None and self.max_tokens < 0:
            raise ValueError("max_tokens must be non-negative")
