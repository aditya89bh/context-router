from context_router.benchmark import compare_routers, format_markdown_table
from context_router.evaluation import category_hit, evaluate_all, evaluate_router, format_results, precision_at_k


def test_precision_at_k_counts_expected_categories():
    assert precision_at_k(["coding", "travel", "coding"], "coding", 3) == 2 / 3


def test_precision_at_k_handles_empty_categories():
    assert precision_at_k([], "coding", 3) == 0.0


def test_category_hit_detects_present_category():
    assert category_hit(["travel", "coding"], "coding") is True
    assert category_hit(["travel"], "robotics") is False


def test_evaluate_router_returns_one_result_per_case():
    results = evaluate_router("task", top_k=3)
    assert len(results) == 3
    assert all(result.category_hit for result in results)


def test_evaluate_all_includes_all_routers():
    routers = {result.router for result in evaluate_all(top_k=3)}
    assert routers == {"recency", "semantic", "task", "hybrid"}


def test_format_results_outputs_csv_header():
    csv = format_results(evaluate_router("task", top_k=3))
    assert csv.startswith("router,query,expected")


def test_compare_routers_outputs_benchmark_rows():
    rows = compare_routers(top_k=3)
    assert {row.router for row in rows} == {"recency", "semantic", "task", "hybrid"}
    assert all(0 <= row.hit_rate <= 1 for row in rows)


def test_format_markdown_table_contains_router_names():
    table = format_markdown_table(compare_routers(top_k=3))
    assert "| hybrid |" in table
    assert "Avg precision@k" in table
