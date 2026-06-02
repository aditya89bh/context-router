from datetime import datetime, timezone

from context_router.context.context_types import ContextItem
from context_router.context.memory_store import MemoryStore
from context_router.context.sqlite_memory_store import SQLiteMemoryStore
from context_router.context.store_protocol import ContextStoreProtocol


def _item(item_id: str = "ctx-1") -> ContextItem:
    return ContextItem(
        id=item_id,
        text="enterprise incident review and remediation plan",
        timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc),
        category="operations",
        importance=0.8,
    )


def _assert_store_contract(store: ContextStoreProtocol) -> None:
    item = _item()
    store.add(item)

    assert isinstance(store, ContextStoreProtocol)
    assert store.all() == [item]
    assert store.search("incident") == [item]
    assert store.get_recent(1) == [item]
    assert store.get_by_category("operations") == [item]


def test_memory_store_satisfies_context_store_protocol() -> None:
    _assert_store_contract(MemoryStore())


def test_sqlite_memory_store_satisfies_context_store_protocol(tmp_path) -> None:
    with SQLiteMemoryStore(tmp_path / "contexts.db") as store:
        _assert_store_contract(store)
