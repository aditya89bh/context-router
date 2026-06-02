"""SQLite-backed memory store."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from context_router.context.context_types import ContextItem
from context_router.context.store_protocol import ContextStoreProtocol


class SQLiteMemoryStore(ContextStoreProtocol):
    """Durable MemoryStore-compatible implementation backed by sqlite3."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()
        self._fts_enabled = self._create_fts_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS context_items (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                category TEXT NOT NULL,
                importance REAL NOT NULL
            )
            """
        )
        self.connection.commit()

    def _create_fts_table(self) -> bool:
        try:
            self.connection.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS context_items_fts
                USING fts5(id UNINDEXED, text, category UNINDEXED)
                """
            )
            self.connection.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def add(self, item: ContextItem) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO context_items (id, text, timestamp, category, importance)
            VALUES (?, ?, ?, ?, ?)
            """,
            (item.id, item.text, item.timestamp.isoformat(), item.category, item.importance),
        )
        if self._fts_enabled:
            self.connection.execute("DELETE FROM context_items_fts WHERE id = ?", (item.id,))
            self.connection.execute(
                "INSERT INTO context_items_fts (id, text, category) VALUES (?, ?, ?)",
                (item.id, item.text, item.category),
            )
        self.connection.commit()

    def all(self) -> list[ContextItem]:
        rows = self.connection.execute("SELECT * FROM context_items ORDER BY timestamp DESC").fetchall()
        return [self._from_row(row) for row in rows]

    def search(self, query: str) -> list[ContextItem]:
        if self._fts_enabled and query.strip():
            try:
                rows = self.connection.execute(
                    """
                    SELECT c.*
                    FROM context_items_fts f
                    JOIN context_items c ON c.id = f.id
                    WHERE context_items_fts MATCH ?
                    ORDER BY c.timestamp DESC
                    """,
                    (query,),
                ).fetchall()
                return [self._from_row(row) for row in rows]
            except sqlite3.OperationalError:
                pass
        terms = {term.lower() for term in query.split()}
        return [item for item in self.all() if terms & set(item.text.lower().split())]

    def get_recent(self, top_k: int = 5) -> list[ContextItem]:
        rows = self.connection.execute(
            "SELECT * FROM context_items ORDER BY timestamp DESC LIMIT ?",
            (top_k,),
        ).fetchall()
        return [self._from_row(row) for row in rows]

    def get_by_category(self, category: str, top_k: int | None = None) -> list[ContextItem]:
        sql = "SELECT * FROM context_items WHERE category = ? ORDER BY timestamp DESC"
        params: tuple[object, ...] = (category,)
        if top_k is not None:
            sql += " LIMIT ?"
            params = (category, top_k)
        rows = self.connection.execute(sql, params).fetchall()
        return [self._from_row(row) for row in rows]

    def __enter__(self) -> "SQLiteMemoryStore":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        self.connection.close()

    def _from_row(self, row: sqlite3.Row) -> ContextItem:
        return ContextItem(
            id=row["id"],
            text=row["text"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            category=row["category"],
            importance=float(row["importance"]),
        )
