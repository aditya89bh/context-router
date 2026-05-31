from context_router.benchmark_data import CATEGORIES, build_synthetic_store, synthetic_evaluation_cases


def test_synthetic_benchmark_store_shape():
    store = build_synthetic_store(100)
    items = store.all()
    assert len(items) == 100
    assert {item.category for item in items} == set(CATEGORIES)
    assert all(item.id for item in items)


def test_synthetic_evaluation_cases_are_enterprise_friendly():
    cases = synthetic_evaluation_cases()
    assert {case.expected_category for case in cases} == set(CATEGORIES)
    assert all(case.expected_ids for case in cases)
