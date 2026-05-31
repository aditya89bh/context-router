"""Router comparison benchmark."""
from __future__ import annotations

import argparse
import json
from time import perf_counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from context_router.benchmark_data import build_synthetic_store, synthetic_evaluation_cases
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
    latency_ms: float


def collect_benchmark_results(top_k: int = 3, dataset_size: int | None = None) -> list[BenchmarkResult]:
    results: list[BenchmarkResult] = []
    cases = synthetic_evaluation_cases() if dataset_size is not None else DEFAULT_EVALUATION_CASES
    for router_name, router_cls in ROUTERS.items():
        store = build_synthetic_store(dataset_size) if dataset_size is not None else build_demo_store()
        router = router_cls(store, top_k=top_k)
        for case in cases:
            started_at = perf_counter()
            routed = router.route(case.query)
            latency_ms = (perf_counter() - started_at) * 1000
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
                    latency_ms=round(latency_ms, 3),
                )
            )
    return results


def write_json_results(path: Path = DEFAULT_JSON_PATH, top_k: int = 3, dataset_size: int | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    results = [asdict(result) for result in collect_benchmark_results(top_k=top_k, dataset_size=dataset_size)]
    generated_at = datetime.now(timezone.utc).isoformat()
    if path.exists():
        try:
            existing = json.loads(path.read_text())
            if existing.get("top_k") == top_k and existing.get("dataset_size") == dataset_size and existing.get("results") == results:
                generated_at = existing.get("generated_at", generated_at)
        except json.JSONDecodeError:
            pass
    payload = {
        "generated_at": generated_at,
        "top_k": top_k,
        "dataset_size": dataset_size,
        "results": results,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def write_markdown_report(json_path: Path = DEFAULT_JSON_PATH, markdown_path: Path | None = None) -> Path:
    markdown_path = markdown_path or json_path.with_suffix(".md")
    payload = json.loads(json_path.read_text())
    results = payload["results"]

    by_router: dict[str, list[dict[str, object]]] = {}
    for result in results:
        by_router.setdefault(str(result["router"]), []).append(result)

    lines = [
        "# Latest Router Benchmark",
        "",
        f"Generated at: `{payload['generated_at']}`",
        "",
        "## Summary by router",
        "",
        "| Router | Cases | Avg precision | Avg recall | Avg selected | Avg latency ms |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for router, router_results in by_router.items():
        cases = len(router_results)
        avg_precision = sum(float(item["precision"]) for item in router_results) / cases
        avg_recall = sum(float(item["recall"]) for item in router_results) / cases
        avg_selected = sum(int(item["selected_count"]) for item in router_results) / cases
        avg_latency = sum(float(item["latency_ms"]) for item in router_results) / cases
        lines.append(f"| {router} | {cases} | {avg_precision:.3f} | {avg_recall:.3f} | {avg_selected:.1f} | {avg_latency:.3f} |")

    lines.extend([
        "",
        "## Per-query results",
        "",
        "| Router | Query | Expected IDs | Returned IDs | Precision | Recall | Selected | Latency ms |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ])
    for result in results:
        expected = ", ".join(result["expected_ids"])
        returned = ", ".join(result["returned_ids"])
        lines.append(
            f"| {result['router']} | {result['query']} | {expected} | {returned} | "
            f"{float(result['precision']):.3f} | {float(result['recall']):.3f} | "
            f"{result['selected_count']} | {float(result['latency_ms']):.3f} |"
        )

    markdown_path.write_text("\n".join(lines) + "\n")
    return markdown_path


def compare_routers(top_k: int = 3, dataset_size: int | None = None) -> list[BenchmarkRow]:
    total_context = dataset_size if dataset_size is not None else len(build_demo_store().all())
    rows: list[BenchmarkRow] = []
    synthetic_results = collect_benchmark_results(top_k=top_k, dataset_size=dataset_size) if dataset_size is not None else None
    for router_name in ROUTERS:
        if dataset_size is None:
            eval_results = evaluate_router(router_name, top_k=top_k)
            cases = len(eval_results)
            avg_precision = sum(result.precision_at_k for result in eval_results) / cases
            hit_rate = sum(result.category_hit for result in eval_results) / cases
            avg_count = sum(len(result.retrieved_categories) for result in eval_results) / cases
        else:
            router_results = [result for result in synthetic_results or [] if result.router == router_name]
            cases = len(router_results)
            avg_precision = sum(result.precision for result in router_results) / cases
            hit_rate = sum(result.recall > 0 for result in router_results) / cases
            avg_count = sum(result.selected_count for result in router_results) / cases
        reduction = 1 - (avg_count / total_context)
        rows.append(
            BenchmarkRow(
                router=router_name,
                cases=cases,
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
    parser = argparse.ArgumentParser(description="Run context-router benchmark reports.")
    parser.add_argument("--dataset-size", type=int, choices=(100, 1000, 10000), default=None)
    args = parser.parse_args()
    print(format_markdown_table(compare_routers(dataset_size=args.dataset_size)))
    path = DEFAULT_JSON_PATH
    if args.dataset_size is not None:
        path = DEFAULT_RESULTS_DIR / f"latest_results_{args.dataset_size}.json"
    path = write_json_results(path=path, dataset_size=args.dataset_size)
    report_path = write_markdown_report(path)
    print(f"\nWrote JSON benchmark results to {path}")
    print(f"Wrote markdown benchmark report to {report_path}")


if __name__ == "__main__":
    main()
