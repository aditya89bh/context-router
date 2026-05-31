from datetime import datetime, timezone

import pytest

from context_router.context.context_pack import ContextPack
from context_router.context.context_types import ContextItem, ScoredContextItem
from context_router.context.memory_store import MemoryStore


def item(i, category="coding", importance=0.5):
    return ContextItem(str(i), f"text {i}", datetime(2026, 1, i, tzinfo=timezone.utc), category, importance)


def test_context_item_validates_importance():
    with pytest.raises(ValueError):
        item(1, importance=1.5)


def test_memory_store_add_and_all():
    store = MemoryStore()
    store.add(item(1))
    assert len(store.all()) == 1


def test_memory_store_get_recent():
    store = MemoryStore([item(1), item(3), item(2)])
    assert [x.id for x in store.get_recent(2)] == ["3", "2"]


def test_memory_store_get_by_category():
    store = MemoryStore([item(1, "coding"), item(2, "customer")])
    assert store.get_by_category("customer")[0].id == "2"


def test_memory_store_search():
    store = MemoryStore([ContextItem("a", "Docker build failed", datetime.now(timezone.utc), "coding")])
    assert store.search("Docker")


def test_context_pack_creation():
    scored = [ScoredContextItem(item(1), 0.8, {"final": 0.8})]
    pack = ContextPack.from_scored(scored, query="q", router="hybrid")
    assert pack.memories[0].id == "1"
    assert pack.metadata["router"] == "hybrid"
    assert "ContextPack" in pack.summary()
