"""Router comparison benchmark."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from context_router.demo_data import build_demo_store
from context_router.evaluation import DEFAULT_EVALUATION_CASES, ROUTERS, evaluate_results, evaluate_router

DEFAULT_RESULTS_DIR = Path("benchmarks/results")
DEFAULT_JSON_PATH = DEFAULT_RESULTS_DIR / "latest_results.json"


@dataclass(frozen=True)
class BenchmarkRow:
    router: str
    cases: int
    avg_precision_at_k: float
    hit_rate: float
    avg_context_count: float
    context_reduction: float


@dataclass(frozen=True)
class BenchmarkResult:
    router: str
    query: str
    expected_ids: list[str]
    returned_ids: list[str]
    precision: float
    recall: float
    selected_count: int


def collect_benchmark_results(top_k: int = 3) -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []
    for router_name, router_cls in ROUTERS.items():
        store = build_demo_store()
        router = router_cls(store, top_k=top_k)
        for case in DEFAULT_EVALUATION_CASES:
            routed = router.route(case.query)
            metrics = evaluate_results(routed, case.expected_ids, k=top_k)
            results.append(
                BenchmarkResult(
                    router=router_name,
                    query=case.query,
                    expected_ids=sorted(case.expected_ids),
                    returned_ids=[scored.item.id for scored in routed[:top_k]],
                    precision=metrics["precision"],
                    recall=metrics["recall"],
                    selected_count=len(routed[:top_k]),
                )
            )
    return results


def write_json_results(path: Path = DEFAULT_JSON_PATH, top_k: int = 3) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "top_k": top_k,
        "results": [asdict(result) for result in collect_benchmark_results(top_k=top_k)],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def compare_routers(top_k: int = 3) -> list[BenchmarkRow]:
    total_context = len(build_demo_store().all())
    rows: list[BenchmarkRow] = []
    for router_name in ROUTERS:
        results = evaluate_router(router_name, top_k=top_k)
        avg_precision = sum(result.precision_at_k for result in results) / len(results)
        hit_rate = sum(result.category_hit for result in results) / len(results)
        avg_count = sum(len(result.retrieved_categories) for result in results) / len(results)
        reduction = 1 - (avg_count / total_context)
        rows.append(
            BenchmarkRow(
                router=router_name,
                cases=len(results),
                avg_precision_at_k=avg_precision,
                hit_rate=hit_rate,
                avg_context_count=avg_count,
                context_reduction=reduction,
            )
        )
    return rows


def format_markdown_table(rows: list[BenchmarkRow]) -> str:
    lines = [
        "| Router | Cases | Avg precision@k | Hit rate | Avg contexts | Context reduction |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.router} | {row.cases} | {row.avg_precision_at_k:.3f} | "
            f"{row.hit_rate:.3f} | {row.avg_context_count:.1f} | {row.context_reduction:.1%} |"
        )
    return "\n".join(lines)


def main() -> None:
    print(format_markdown_table(compare_routers()))
    path = write_json_results()
    print(f"\nWrote JSON benchmark results to {path}")


if __name__ == "__main__":
    main()
