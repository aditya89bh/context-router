"""Deterministic synthetic benchmark data for larger local runs."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.context.memory_store import MemoryStore
from context_router.evaluation import EvaluationCase

CATEGORIES = ("customer", "coding", "robotics", "operations", "planning")

CATEGORY_TEXT = {
    "customer": "Customer automation meeting context for low-risk rollout, stakeholder alignment, ROI estimate, and deployment timeline.",
    "coding": "Coding incident context for Docker build failure, CI diagnostics, pinned Python versions, and reproducible builds.",
    "robotics": "Robotics recovery context for CNC pickup, perception retry, gripper homing, ROS state, and safe trajectory resume.",
    "operations": "Operations handoff context for deployment ownership, support readiness, escalation paths, and service continuity.",
    "planning": "Planning context for roadmap sequencing, milestone review, dependency tracking, and delivery risk management.",
}


def build_synthetic_store(size: int, now: datetime | None = None) -> MemoryStore:
    """Build a deterministic enterprise-friendly memory store with ``size`` items."""
    if size <= 0:
        raise ValueError("size must be positive")
    now = now or datetime.now(timezone.utc)
    store = MemoryStore()
    for index in range(size):
        category = CATEGORIES[index % len(CATEGORIES)]
        store.add(
            ContextItem(
                id=f"{category}-{index}",
                text=f"{CATEGORY_TEXT[category]} Reference item {index}.",
                timestamp=now - timedelta(minutes=index),
                category=category,
                importance=0.5 + ((index % 5) * 0.1),
            )
        )
    return store


def synthetic_evaluation_cases() -> list[EvaluationCase]:
    """Return evaluation cases aligned with the deterministic synthetic dataset."""
    return [
        EvaluationCase(
            query="Prepare for the customer automation meeting",
            expected_ids={"customer-0"},
            expected_category="customer",
        ),
        EvaluationCase(
            query="Fix Docker build failure in CI",
            expected_ids={"coding-1"},
            expected_category="coding",
        ),
        EvaluationCase(
            query="Recover failed CNC pickup on the robot cell",
            expected_ids={"robotics-2"},
            expected_category="robotics",
        ),
        EvaluationCase(
            query="Review deployment handoff and escalation readiness",
            expected_ids={"operations-3"},
            expected_category="operations",
        ),
        EvaluationCase(
            query="Plan roadmap milestones and delivery risks",
            expected_ids={"planning-4"},
            expected_category="planning",
        ),
    ]
