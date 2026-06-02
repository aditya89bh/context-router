import json

from context_router.benchmark import collect_benchmark_results, write_json_results
from context_router.benchmark_fixtures import DEFAULT_FIXTURE_PATH, load_benchmark_fixture


def test_benchmark_fixture_loads_contexts_and_cases() -> None:
    fixture = load_benchmark_fixture(DEFAULT_FIXTURE_PATH)

    assert fixture.name == "enterprise_contexts"
    assert [item.id for item in fixture.store.all()] == ["ops-incident-1", "security-review-1", "customer-rollout-1"]
    assert [case.query for case in fixture.cases] == [
        "Review service latency incident and rollback owner",
        "Prepare audit evidence for deployment approval",
        "Plan customer rollout training and success metrics",
    ]


def test_benchmark_runner_accepts_fixture() -> None:
    results = collect_benchmark_results(fixture_path=DEFAULT_FIXTURE_PATH)

    assert len(results) == 12
    assert {result.query for result in results} == {
        "Review service latency incident and rollback owner",
        "Prepare audit evidence for deployment approval",
        "Plan customer rollout training and success metrics",
    }


def test_benchmark_fixture_output_is_deterministic(tmp_path) -> None:
    first = write_json_results(tmp_path / "first.json", fixture_path=DEFAULT_FIXTURE_PATH)
    second = write_json_results(tmp_path / "second.json", fixture_path=DEFAULT_FIXTURE_PATH)

    first_payload = json.loads(first.read_text())
    second_payload = json.loads(second.read_text())

    assert first_payload["fixture"] == str(DEFAULT_FIXTURE_PATH)
    assert first_payload["results"] == second_payload["results"]
