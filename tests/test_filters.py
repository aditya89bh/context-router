from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.context.filters import filter_context_items


BASE = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)


def item(item_id: str, hours: int, category: str, importance: float) -> ContextItem:
    return ContextItem(item_id, item_id, BASE + timedelta(hours=hours), category, importance)


def test_filter_by_category():
    items = [item("a", 0, "coding", 0.5), item("b", 1, "robotics", 0.5)]
    assert [x.id for x in filter_context_items(items, category="coding")] == ["a"]


def test_filter_by_minimum_importance():
    items = [item("low", 0, "coding", 0.3), item("high", 1, "coding", 0.9)]
    assert [x.id for x in filter_context_items(items, min_importance=0.8)] == ["high"]


def test_filter_by_start_and_end_timestamp():
    items = [item("early", -2, "coding", 0.8), item("middle", 0, "coding", 0.8), item("late", 2, "coding", 0.8)]
    filtered = filter_context_items(items, start=BASE - timedelta(hours=1), end=BASE + timedelta(hours=1))
    assert [x.id for x in filtered] == ["middle"]


def test_filter_with_combined_criteria():
    items = [
        item("wrong-category", 0, "robotics", 0.9),
        item("too-low", 0, "coding", 0.4),
        item("too-early", -5, "coding", 0.9),
        item("match", 0, "coding", 0.9),
    ]
    filtered = filter_context_items(
        items,
        category="coding",
        start=BASE - timedelta(hours=1),
        end=BASE + timedelta(hours=1),
        min_importance=0.8,
    )
    assert [x.id for x in filtered] == ["match"]
