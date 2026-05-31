"""Minimal enterprise integration example."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from context_router import ContextItem, ContextPack, HybridRouter, MemoryStore


def run() -> ContextPack:
    now = datetime.now(timezone.utc)
    store = MemoryStore(
        [
            ContextItem(
                id="customer-rollout",
                text="Customer rollout requires a low-risk phased deployment plan for inspection automation.",
                timestamp=now - timedelta(hours=2),
                category="customer",
                importance=0.9,
            ),
            ContextItem(
                id="customer-roi",
                text="Customer stakeholders requested an ROI estimate and timeline options before approval.",
                timestamp=now - timedelta(hours=4),
                category="customer",
                importance=0.85,
            ),
            ContextItem(
                id="support-handoff",
                text="Support handoff notes mention validating ownership before changing deployment scope.",
                timestamp=now - timedelta(hours=8),
                category="operations",
                importance=0.6,
            ),
        ]
    )

    query = "Prepare for the customer automation meeting"
    router = HybridRouter(store, top_k=2)
    scored = router.route(query)
    pack = ContextPack.from_scored(scored, query=query, router=router.name)

    print(pack.summary())
    for item in pack.memories:
        print(f"- [{item.category}] {item.text}")
    return pack


if __name__ == "__main__":
    run()
