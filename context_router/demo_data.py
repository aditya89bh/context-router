"""Demo memories shared by examples and CLI."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.context.memory_store import MemoryStore


def build_demo_store(now: datetime | None = None) -> MemoryStore:
    now = now or datetime.now(timezone.utc)
    store = MemoryStore()
    samples = [
        ("travel-greece", "Greece trip plan: Athens for history, Santorini for sunset, ferry buffer day, Schengen visa checklist.", 5, "travel", 0.9),
        ("travel-hotel", "Greece travel booking: choose refundable hotels near metro stations and keep one day open for island weather changes.", 12, "travel", 0.7),
        ("coding-docker", "Docker build failure: base image mismatch, missing system package, and cached layer invalidation steps.", 2, "coding", 0.95),
        ("coding-ci", "Docker build and CI failures usually need pinned Python versions and a reproducible requirements lockfile.", 20, "coding", 0.75),
        ("robot-cnc", "CNC pickup recovery: retry perception, re-home gripper, verify workpiece pose, then resume safe trajectory.", 1, "robotics", 0.95),
        ("robot-ros", "ROS/RViz debugging notes: inspect TF tree, joint states, and collision scene before planning.", 16, "robotics", 0.8),
        ("personal-calendar", "Prefer morning deep-work blocks and keep evenings lighter for planning and review.", 6, "personal", 0.55),
    ]
    for item_id, text, age_hours, category, importance in samples:
        store.add(ContextItem(item_id, text, now - timedelta(hours=age_hours), category, importance))
    return store
