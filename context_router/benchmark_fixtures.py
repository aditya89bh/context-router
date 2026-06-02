"""Load deterministic benchmark fixtures."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from context_router.context.context_types import ContextItem
from context_router.context.memory_store import MemoryStore
from context_router.evaluation import EvaluationCase

DEFAULT_FIXTURE_PATH = Path("benchmarks/fixtures/enterprise_contexts.json")


@dataclass(frozen=True)
class BenchmarkFixture:
    """Loaded benchmark fixture data."""

    name: str
    store: MemoryStore
    cases: list[EvaluationCase]


def load_benchmark_fixture(path: str | Path = DEFAULT_FIXTURE_PATH) -> BenchmarkFixture:
    """Load a deterministic benchmark fixture from JSON."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("benchmark fixture must be a JSON object")
    store = MemoryStore(_context_item(item) for item in _list(payload, "items"))
    cases = [_evaluation_case(case) for case in _list(payload, "cases")]
    return BenchmarkFixture(name=str(payload.get("name", Path(path).stem)), store=store, cases=cases)


def _list(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ValueError(f"benchmark fixture field {key!r} must be a list")
    return [item for item in value if isinstance(item, dict)]


def _context_item(payload: dict[str, Any]) -> ContextItem:
    return ContextItem(
        id=str(payload["id"]),
        text=str(payload["text"]),
        timestamp=datetime.fromisoformat(str(payload["timestamp"])),
        category=str(payload["category"]),
        importance=float(payload.get("importance", 0.5)),
    )


def _evaluation_case(payload: dict[str, Any]) -> EvaluationCase:
    expected_ids = payload.get("expected_ids", [])
    if not isinstance(expected_ids, list):
        raise ValueError("expected_ids must be a list")
    return EvaluationCase(
        query=str(payload["query"]),
        expected_ids={str(item) for item in expected_ids},
        expected_category=str(payload["expected_category"]),
    )
