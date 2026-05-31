"""CLI demo: python -m context_router.demo"""
from __future__ import annotations

import argparse

from context_router.context.context_pack import ContextPack
from context_router.demo_data import build_demo_store
from context_router.router.hybrid_router import HybridRouter
from context_router.router.recency_router import RecencyRouter
from context_router.router.semantic_router import SemanticRouter
from context_router.router.task_router import TaskRouter

ROUTERS = {
    "recency": RecencyRouter,
    "semantic": SemanticRouter,
    "task": TaskRouter,
    "hybrid": HybridRouter,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Route the right context to the right agent at the right time.")
    parser.add_argument("--query", default="Help me plan my Greece trip")
    parser.add_argument("--router", choices=ROUTERS.keys(), default="hybrid")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    store = build_demo_store()
    router = ROUTERS[args.router](store, top_k=args.top_k)
    retrieved = router.route(args.query)
    pack = ContextPack.from_scored(retrieved, query=args.query, router=args.router)

    print(f"Query: {args.query}")
    print(f"Selected router: {args.router}")
    print("Retrieved contexts:")
    for idx, scored in enumerate(retrieved, start=1):
        print(f"  {idx}. [{scored.item.category}] {scored.item.text}")
        print(f"     score={scored.score:.3f} details={{{', '.join(f'{k}: {v:.3f}' for k, v in scored.scores.items() if isinstance(v, float))}}}")
    print(f"ContextPack summary: {pack.summary()}")


if __name__ == "__main__":
    main()
