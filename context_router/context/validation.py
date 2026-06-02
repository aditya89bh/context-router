"""Validation helpers for context item fields."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from context_router.context.context_types import ContextItem


def validate_context_fields(
    *,
    id: str,
    text: str,
    timestamp: datetime,
    importance: float,
) -> None:
    """Validate common context fields and raise clear ValueError messages."""
    if not isinstance(id, str) or not id.strip():
        raise ValueError("context id must be a non-empty string")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("context text must be a non-empty string")
    if not isinstance(timestamp, datetime):
        raise ValueError("context timestamp must be a datetime")
    if not 0 <= importance <= 1:
        raise ValueError("context importance must be between 0 and 1")


def validate_context_item(item: ContextItem) -> None:
    """Validate an existing ContextItem."""
    validate_context_fields(id=item.id, text=item.text, timestamp=item.timestamp, importance=item.importance)


def validate_context_payload(payload: dict[str, Any]) -> None:
    """Validate a dictionary before constructing a ContextItem."""
    validate_context_fields(
        id=str(payload.get("id", "")),
        text=str(payload.get("text", "")),
        timestamp=payload.get("timestamp"),
        importance=float(payload.get("importance", 0.5)),
    )
