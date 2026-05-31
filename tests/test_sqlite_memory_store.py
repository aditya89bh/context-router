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



def test_sqlite_store_search_uses_expected_terms(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("docker", "Docker build failure in CI", 2, "coding"))
    store.add(make_item("robot", "Robot pickup recovery", 1, "robotics"))

    assert [item.id for item in store.search("Docker")] == ["docker"]



def test_sqlite_store_multiple_open_close_cycles(tmp_path):
    path = tmp_path / "memory.db"
    for index in range(3):
        store = SQLiteMemoryStore(path)
        store.add(make_item(f"item-{index}", f"Cycle {index}", index, "operations"))
        store.close()

    reopened = SQLiteMemoryStore(path)
    assert {item.id for item in reopened.all()} == {"item-0", "item-1", "item-2"}


def test_sqlite_store_repeated_writes_replace_same_id(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("same", "Original customer context", 3, "customer", 0.4))
    store.add(make_item("same", "Updated customer context", 1, "customer", 0.9))

    items = store.all()
    assert len(items) == 1
    assert items[0].text == "Updated customer context"
    assert items[0].importance == 0.9


def test_sqlite_store_persistence_after_reopening_with_repeated_write(tmp_path):
    path = tmp_path / "memory.db"
    store = SQLiteMemoryStore(path)
    store.add(make_item("same", "Original", 3, "customer"))
    store.add(make_item("same", "Updated", 1, "customer"))
    store.close()

    reopened = SQLiteMemoryStore(path)
    assert [(item.id, item.text) for item in reopened.all()] == [("same", "Updated")]


def test_sqlite_store_get_recent_ordering(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.db")
    store.add(make_item("old", "Old operations note", 10, "operations"))
    store.add(make_item("new", "New operations note", 1, "operations"))
    store.add(make_item("middle", "Middle operations note", 5, "operations"))

    assert [item.id for item in store.get_recent(3)] == ["new", "middle", "old"]


def test_sqlite_store_read_after_context_manager_close_fails_cleanly(tmp_path):
    path = tmp_path / "memory.db"
    with SQLiteMemoryStore(path) as store:
        store.add(make_item("managed", "Managed connection", 1, "customer"))

    import sqlite3

    try:
        store.all()
    except sqlite3.ProgrammingError as exc:
        assert "closed" in str(exc).lower()
    else:
        raise AssertionError("expected sqlite3.ProgrammingError after close")
