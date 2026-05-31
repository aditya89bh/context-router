"""Task-category router."""
from __future__ import annotations

from context_router.context.context_types import ScoredContextItem
from context_router.context.memory_store import MemoryStore
from context_router.scoring.importance import importance_score


TASK_KEYWORDS: dict[str, set[str]] = {
    "coding": {"code", "docker", "build", "bug", "test", "python", "github", "ci", "deploy", "fix"},
    "travel": {"trip", "travel", "flight", "hotel", "greece", "visa", "itinerary", "plan"},
    "robotics": {"robot", "robotics", "cnc", "pickup", "gripper", "ros", "rviz", "arm", "kinematic"},
    "personal": {"email", "calendar", "remind", "habit", "family", "health", "personal"},
}


class TaskRouter:
    """Route context based on inferred task category."""

    name = "task"

    def __init__(self, store: MemoryStore, top_k: int = 5, task_keywords: dict[str, set[str]] | None = None) -> None:
        self.store = store
        self.top_k = top_k
        self.task_keywords = task_keywords or TASK_KEYWORDS

    def classify(self, query: str) -> str:
        terms = set(query.lower().replace("/", " ").replace("-", " ").split())
        ranked = sorted(
            ((category, len(terms & keywords)) for category, keywords in self.task_keywords.items()),
            key=lambda pair: pair[1],
            reverse=True,
        )
        if ranked and ranked[0][1] > 0:
            return ranked[0][0]
        return "personal"

    def route(self, query: str) -> list[ScoredContextItem]:
        category = self.classify(query)
        items = self.store.get_by_category(category, self.top_k)
        return [
            ScoredContextItem(item=item, score=importance_score(item), scores={"task_category": 1.0, "importance": importance_score(item)})
            for item in items
        ]
