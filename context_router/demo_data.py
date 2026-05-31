"""Demo memories shared by examples and CLI."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.context.memory_store import MemoryStore


def build_demo_store(now: datetime | None = None) -> MemoryStore:
    now = now or datetime.now(timezone.utc)
    store = MemoryStore()
    samples = [
        (
            "customer-profile",
            "Customer meeting prep: Acme Manufacturing wants a low-risk automation rollout for end-of-line inspection.",
            5,
            "customer",
            0.9,
        ),
        (
            "customer-actions",
            "Open customer action items: confirm stakeholder list, prepare ROI estimate, and bring deployment timeline options.",
            12,
            "customer",
            0.85,
        ),
        (
            "coding-docker",
            "Docker build failure: base image mismatch, missing system package, and cached layer invalidation steps.",
            2,
            "coding",
            0.95,
        ),
        (
            "coding-ci",
            "Docker build and CI failures usually need pinned Python versions and a reproducible requirements lockfile.",
            20,
            "coding",
            0.75,
        ),
        (
            "robot-cnc",
            "CNC pickup recovery: retry perception, re-home gripper, verify workpiece pose, then resume safe trajectory.",
            1,
            "robotics",
            0.95,
        ),
        (
            "robot-ros",
            "ROS/RViz debugging notes: inspect TF tree, joint states, and collision scene before planning.",
            16,
            "robotics",
            0.8,
        ),
        (
            "planning-calendar",
            "Prefer morning deep-work blocks for technical planning and reserve late afternoon for reviews and follow-ups.",
            6,
            "planning",
            0.55,
        ),
    ]
    for item_id, text, age_hours, category, importance in samples:
        store.add(ContextItem(item_id, text, now - timedelta(hours=age_hours), category, importance))
    return store
