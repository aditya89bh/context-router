"""Regression threshold checks for benchmark results."""
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable

from context_router.benchmark import BenchmarkResult


@dataclass(frozen=True)
class BenchmarkThresholds:
    """Minimum quality and maximum latency gates for benchmarks."""

    minimum_precision: float = 0.5
    minimum_recall: float = 0.5
    maximum_average_latency_ms: float = 1000.0


def check_benchmark_thresholds(
    results: Iterable[BenchmarkResult],
    thresholds: BenchmarkThresholds | None = None,
) -> list[str]:
    """Return human-readable failures for results that miss thresholds."""
    thresholds = thresholds or BenchmarkThresholds()
    failures: list[str] = []
    latency_by_router: dict[str, list[float]] = defaultdict(list)

    for result in results:
        if result.precision < thresholds.minimum_precision:
            failures.append(
                f"{result.router} precision {result.precision:.3f} below {thresholds.minimum_precision:.3f} for {result.query}"
            )
        if result.recall < thresholds.minimum_recall:
            failures.append(f"{result.router} recall {result.recall:.3f} below {thresholds.minimum_recall:.3f} for {result.query}")
        latency_by_router[result.router].append(result.latency_ms)

    for router, latencies in latency_by_router.items():
        average_latency = sum(latencies) / len(latencies)
        if average_latency > thresholds.maximum_average_latency_ms:
            failures.append(
                f"{router} average latency {average_latency:.3f} ms above {thresholds.maximum_average_latency_ms:.3f} ms"
            )

    return failures
