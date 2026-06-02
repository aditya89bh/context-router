from datetime import datetime, timezone

import pytest

from context_router.context.context_types import ContextItem
from context_router.context.validation import validate_context_fields, validate_context_item, validate_context_payload


def test_validate_context_fields_accepts_valid_values() -> None:
    validate_context_fields(
        id="ctx-1",
        text="Review operational readiness",
        timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        importance=0.5,
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"id": "", "text": "valid", "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc), "importance": 0.5},
        {"id": "ctx-1", "text": "", "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc), "importance": 0.5},
        {"id": "ctx-1", "text": "valid", "timestamp": "2024-01-01", "importance": 0.5},
        {"id": "ctx-1", "text": "valid", "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc), "importance": 1.1},
    ],
)
def test_validate_context_fields_rejects_invalid_values(kwargs) -> None:
    with pytest.raises(ValueError):
        validate_context_fields(**kwargs)


def test_validate_context_item_accepts_context_item() -> None:
    item = ContextItem(id="ctx-1", text="Review deployment", timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc), category="operations")

    validate_context_item(item)


def test_validate_context_payload_accepts_valid_payload() -> None:
    validate_context_payload(
        {
            "id": "ctx-1",
            "text": "Review deployment",
            "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "importance": 0.6,
        }
    )
