from datetime import datetime, timezone

import pytest

from context_router.context.context_pack import ContextPack, estimate_tokens, select_with_token_budget
from context_router.context.context_types import ContextItem, ScoredContextItem


def make_item(item_id: str, text: str) -> ContextItem:
    return ContextItem(item_id, text, datetime.now(timezone.utc), "coding", 0.5)


def test_estimate_tokens_counts_words():
    assert estimate_tokens("one two three") == 3


def test_select_with_token_budget_keeps_ordered_items_that_fit():
    items = [make_item("1", "one two"), make_item("2", "three four five"), make_item("3", "six")]
    selected = select_with_token_budget(items, max_tokens=3)
    assert [item.id for item in selected] == ["1", "3"]


def test_context_pack_applies_max_tokens():
    scored = [
        ScoredContextItem(make_item("1", "one two"), 0.9),
        ScoredContextItem(make_item("2", "three four five"), 0.8),
    ]
    pack = ContextPack.from_scored(scored, query="q", router="hybrid", max_tokens=2)
    assert [item.id for item in pack.memories] == ["1"]
    assert pack.metadata["estimated_tokens"] == 2
    assert pack.metadata["available_count"] == 2


def test_context_pack_rejects_negative_token_budget():
    scored = [ScoredContextItem(make_item("1", "one"), 0.9)]
    with pytest.raises(ValueError):
        ContextPack.from_scored(scored, query="q", router="hybrid", max_tokens=-1)
