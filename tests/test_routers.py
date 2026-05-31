from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.context.memory_store import MemoryStore
from context_router.demo_data import build_demo_store
from context_router.router.config import RouterConfig
from context_router.router.hybrid_router import HybridRouter
from context_router.router.recency_router import RecencyRouter
from context_router.router.semantic_router import SemanticRouter
from context_router.router.task_router import TaskRouter


def test_recency_router_returns_most_recent():
    now = datetime.now(timezone.utc)
    store = MemoryStore([
        ContextItem("old", "old", now - timedelta(days=3), "personal"),
        ContextItem("new", "new", now, "personal"),
    ])
    assert RecencyRouter(store, top_k=1).route("anything")[0].item.id == "new"


def test_semantic_router_returns_relevant_item():
    store = build_demo_store()
    result = SemanticRouter(store, top_k=1).route("Docker build failure")[0]
    assert result.item.category == "coding"


def test_task_router_classifies_customer():
    router = TaskRouter(build_demo_store())
    assert router.classify("Prepare for the customer automation meeting") == "customer"


def test_task_router_returns_customer_memories():
    results = TaskRouter(build_demo_store(), top_k=2).route("Prepare for the customer automation meeting")
    assert results
    assert all(result.item.category == "customer" for result in results)


def test_task_router_returns_coding_memories():
    results = TaskRouter(build_demo_store(), top_k=2).route("Fix Docker build failure")
    assert all(result.item.category == "coding" for result in results)


def test_task_router_returns_robotics_memories():
    results = TaskRouter(build_demo_store(), top_k=2).route("Recover failed CNC pickup")
    assert all(result.item.category == "robotics" for result in results)


def test_hybrid_router_exposes_weighted_scores():
    results = HybridRouter(build_demo_store(), top_k=3).route("Recover failed CNC pickup")
    assert "semantic" in results[0].scores
    assert "recency" in results[0].scores
    assert "importance" in results[0].scores
    assert "final" in results[0].scores


def test_hybrid_router_prefers_relevant_robotics_memory():
    results = HybridRouter(build_demo_store(), top_k=1).route("Recover failed CNC pickup")
    assert results[0].item.category == "robotics"


def test_top_k_respected():
    assert len(HybridRouter(build_demo_store(), top_k=2).route("Greece trip")) == 2


def test_hybrid_router_accepts_custom_direct_weights():
    results = HybridRouter(
        build_demo_store(),
        top_k=1,
        semantic_weight=0.0,
        recency_weight=0.0,
        importance_weight=1.0,
    ).route("Recover failed CNC pickup")
    assert results[0].scores["final"] == results[0].scores["importance"]


def test_hybrid_router_accepts_router_config_weights():
    config = RouterConfig(top_k=1, semantic_weight=0.0, recency_weight=1.0, importance_weight=0.0)
    results = HybridRouter(build_demo_store(), config=config).route("Recover failed CNC pickup")
    assert results[0].scores["final"] == results[0].scores["recency"]
