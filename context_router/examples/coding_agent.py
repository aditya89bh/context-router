"""Coding agent example: retrieve coding context for Docker build debugging."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from context_router.context.context_pack import ContextPack
from context_router.demo_data import build_demo_store
from context_router.router.task_router import TaskRouter


def run() -> ContextPack:
    query = "Fix Docker build failure"
    router = TaskRouter(build_demo_store(), top_k=3)
    results = router.route(query)
    pack = ContextPack.from_scored(results, query=query, router=router.name)
    print(pack.summary())
    for memory in pack.memories:
        print(f"- [{memory.category}] {memory.text}")
    return pack


if __name__ == "__main__":
    run()
