"""Lightweight observability primitives for routing calls."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RoutingEvent:
    """Structured event describing one routing operation.

    The event is intentionally dependency-free so applications can send the
    dictionary output to their preferred logging, metrics, or tracing system.
    """

    router: str
    query: str
    latency_ms: float | None
    selected_count: int
    estimated_tokens: int | None
    scores: list[dict] | None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the event."""
        return asdict(self)
