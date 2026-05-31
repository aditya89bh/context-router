from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.context.sqlite_memory_store import SQLiteMemoryStore


def make_item(item_id: str, text: str, age_hours: int, category: str, importance: float = 0.5) -> ContextItem:
    now = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    return ContextItem(item_id, text, now - timedelta(hours=age_hours), category, importance)


def test_sqlite_store_add_and_retrieve_all(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("1", "Docker build", 2, "coding"))
    assert [item.id for item in store.all()] == ["1"]


def test_sqlite_store_search(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("1", "Docker build failure", 2, "coding"))
    store.add(make_item("2", "Customer meeting", 1, "customer"))
    assert [item.id for item in store.search("Docker")] == ["1"]


def test_sqlite_store_get_recent(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("old", "old", 5, "coding"))
    store.add(make_item("new", "new", 1, "coding"))
    assert [item.id for item in store.get_recent(1)] == ["new"]


def test_sqlite_store_get_by_category(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("code", "Docker", 2, "coding"))
    store.add(make_item("robot", "CNC", 1, "robotics"))
    assert [item.id for item in store.get_by_category("robotics")] == ["robot"]


def test_sqlite_store_persists_after_reopen(tmp_path):
    path = tmp_path / "memory.db"
    store = SQLiteMemoryStore(path)
    store.add(make_item("persisted", "Durable context", 1, "customer"))
    store.close()

    reopened = SQLiteMemoryStore(path)
    assert [item.id for item in reopened.all()] == ["persisted"]


def test_sqlite_store_context_manager_closes_connection(tmp_path):
    path = tmp_path / "memory.db"
    with SQLiteMemoryStore(path) as store:
        store.add(make_item("managed", "Managed connection", 1, "customer"))

    reopened = SQLiteMemoryStore(path)
    assert [item.id for item in reopened.all()] == ["managed"]

