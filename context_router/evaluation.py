"""Evaluation runner and metrics for context routing quality."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from context_router.context.context_pack import ContextPack
from context_router.context.context_types import ScoredContextItem
from context_router.demo_data import build_demo_store
from context_router.router.hybrid_router import HybridRouter
from context_router.router.recency_router import RecencyRouter
from context_router.router.semantic_router import SemanticRouter
from context_router.router.task_router import TaskRouter


@dataclass(frozen=True)
class EvaluationCase:
    """One query with expected context ids and category."""

    query: str
    expected_ids: set[str]
    expected_category: str
    router: str = "hybrid"


@dataclass(frozen=True)
class EvalResult:
    router: str
    query: str
    expected_category: str
    retrieved_categories: list[str]
    precision_at_k: float
    category_hit: bool


DEFAULT_EVALUATION_CASES: list[EvaluationCase] = [
    EvaluationCase(
        query="Prepare for the customer automation meeting",
        expected_ids={"customer-profile", "customer-actions"},
        expected_category="customer",
    ),
    EvaluationCase(
        query="Fix Docker build failure in CI",
        expected_ids={"coding-docker", "coding-ci"},
        expected_category="coding",
    ),
    EvaluationCase(
        query="Recover failed CNC pickup on the robot cell",
        expected_ids={"robot-cnc", "robot-ros"},
        expected_category="robotics",
    ),
]

# Backward-compatible alias used by the CLI-style runner.
EvalCase = EvaluationCase
DEFAULT_CASES = DEFAULT_EVALUATION_CASES

ROUTERS = {
    "recency": RecencyRouter,
    "semantic": SemanticRouter,
    "task": TaskRouter,
    "hybrid": HybridRouter,
}


def _category_precision(categories: Iterable[str], expected_category: str, k: int) -> float:
    selected = list(categories)[:k]
    if not selected:
        return 0.0
    return sum(category == expected_category for category in selected) / len(selected)


def precision_at_k(results: Sequence[ScoredContextItem] | Iterable[str], expected: set[str] | str, k: int | None = None) -> float:
    """Return precision@k for scored items or category labels."""
    selected = list(results)[:k] if k is not None else list(results)
    if not selected:
        return 0.0
    if isinstance(expected, str):
        return sum(category == expected for category in selected) / len(selected)
    return sum(scored.item.id in expected for scored in selected) / len(selected)  # type: ignore[union-attr]


def recall_at_k(results: Sequence[ScoredContextItem], expected_ids: set[str], *, k: int | None = None) -> float:
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


def category_hit(categories: Iterable[str], expected_category: str) -> bool:
    return expected_category in set(categories)


def evaluate_router(router_name: str, cases: list[EvaluationCase] | None = None, top_k: int = 3) -> list[EvalResult]:
    store = build_demo_store()
    router = ROUTERS[router_name](store, top_k=top_k)
    results: list[EvalResult] = []
    for case in cases or DEFAULT_EVALUATION_CASES:
        routed: list[ScoredContextItem] = router.route(case.query)
        pack = ContextPack.from_scored(routed, query=case.query, router=router_name)
        categories = [item.category for item in pack.memories]
        results.append(
            EvalResult(
                router=router_name,
                query=case.query,
                expected_category=case.expected_category,
                retrieved_categories=categories,
                precision_at_k=_category_precision(categories, case.expected_category, top_k),
                category_hit=category_hit(categories, case.expected_category),
            )
        )
    return results


def evaluate_all(top_k: int = 3) -> list[EvalResult]:
    all_results: list[EvalResult] = []
    for router_name in ROUTERS:
        all_results.extend(evaluate_router(router_name, top_k=top_k))
    return all_results


def format_results(results: list[EvalResult]) -> str:
    lines = ["router,query,expected,precision_at_k,category_hit,retrieved_categories"]
    for result in results:
        lines.append(
            f"{result.router},{result.query},{result.expected_category},"
            f"{result.precision_at_k:.3f},{result.category_hit},"
            f"{'|'.join(result.retrieved_categories)}"
        )
    return "\n".join(lines)


def main() -> None:
    print(format_results(evaluate_all()))


if __name__ == "__main__":
    main()
