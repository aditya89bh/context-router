"""Lightweight evaluation helpers for context routing."""
from __future__ import annotations

from dataclasses import dataclass

from context_router.context.context_types import ScoredContextItem


@dataclass(frozen=True)
class EvaluationCase:
    """One query with the expected context item ids."""

    query: str
    expected_ids: set[str]
    router: str = "hybrid"


DEFAULT_EVALUATION_CASES: list[EvaluationCase] = [
    EvaluationCase(
        query="Prepare for the customer automation meeting",
        expected_ids={"customer-profile", "customer-actions"},
    ),
    EvaluationCase(
        query="Fix Docker build failure in CI",
        expected_ids={"coding-docker", "coding-ci"},
    ),
    EvaluationCase(
        query="Recover failed CNC pickup on the robot cell",
        expected_ids={"robot-cnc", "robot-ros"},
    ),
]


def precision_at_k(results: list[ScoredContextItem], expected_ids: set[str], *, k: int | None = None) -> float:
    """Return the fraction of selected items that are relevant."""
    selected = results[:k] if k is not None else results
    if not selected:
        return 0.0
    relevant = sum(1 for scored in selected if scored.item.id in expected_ids)
    return relevant / len(selected)


def recall_at_k(results: list[ScoredContextItem], expected_ids: set[str], *, k: int | None = None) -> float:
    """Return the fraction of expected items that were retrieved."""
    if not expected_ids:
        return 0.0
    selected = results[:k] if k is not None else results
    found = {scored.item.id for scored in selected if scored.item.id in expected_ids}
    return len(found) / len(expected_ids)


def evaluate_results(results: list[ScoredContextItem], expected_ids: set[str], *, k: int | None = None) -> dict[str, float]:
    """Compute basic retrieval metrics for one routed result set."""
    return {
        "precision": round(precision_at_k(results, expected_ids, k=k), 4),
        "recall": round(recall_at_k(results, expected_ids, k=k), 4),
    }
