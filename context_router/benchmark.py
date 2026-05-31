"""Router comparison benchmark."""
from __future__ import annotations

from dataclasses import dataclass

from context_router.demo_data import build_demo_store
from context_router.evaluation import ROUTERS, evaluate_router


@dataclass(frozen=True)
class BenchmarkRow:
    router: str
    cases: int
    avg_precision_at_k: float
    hit_rate: float
    avg_context_count: float
    context_reduction: float


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


if __name__ == "__main__":
    main()
