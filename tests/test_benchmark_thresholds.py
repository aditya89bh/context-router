from context_router.benchmark import BenchmarkResult
from context_router.benchmark_thresholds import BenchmarkThresholds, check_benchmark_thresholds


def result(**overrides):
    data = {
        "router": "hybrid",
        "query": "Prepare for the customer automation meeting",
        "expected_ids": ["customer-profile"],
        "returned_ids": ["customer-profile"],
        "precision": 1.0,
        "recall": 1.0,
        "selected_count": 1,
        "latency_ms": 10.0,
    }
    data.update(overrides)
    return BenchmarkResult(**data)


def test_benchmark_thresholds_pass():
    assert check_benchmark_thresholds([result()]) == []


def test_benchmark_thresholds_fail_precision():
    failures = check_benchmark_thresholds([result(precision=0.25)])
    assert any("precision" in failure for failure in failures)


def test_benchmark_thresholds_fail_recall():
    failures = check_benchmark_thresholds([result(recall=0.25)])
    assert any("recall" in failure for failure in failures)


def test_benchmark_thresholds_fail_latency():
    failures = check_benchmark_thresholds(
        [result(latency_ms=20.0), result(latency_ms=30.0)],
        BenchmarkThresholds(maximum_average_latency_ms=10.0),
    )
    assert any("average latency" in failure for failure in failures)
