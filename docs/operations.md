# Operations Guide

This guide supports the Production readiness roadmap in GitHub issue #1.

## Run tests

```bash
python -m pip install -e .[dev]
python -m pytest
```

## Run demos

```bash
python -m context_router.demo
python -m context_router.demo --max-tokens 40
python -m context_router.demo --query "Fix Docker build failure" --router hybrid
```

## Run benchmarks

```bash
python -m context_router.benchmark
python -m context_router.benchmark --dataset-size 100
```

The default benchmark is intentionally small and fast. The synthetic dataset flag is for local scale checks without changing the default developer workflow.

## Interpret latency and precision/recall

- **Latency**: Measured per routing call in milliseconds. Track average latency by router and investigate sudden increases.
- **Precision**: How much returned context was expected. Low precision means noisy routing.
- **Recall**: How much expected context was returned. Low recall means important context was missed.

High precision and high recall are both important. A router can be fast but still unsafe if it consistently misses required context.

## Use SQLiteMemoryStore

Use `SQLiteMemoryStore` when context must persist across process restarts or when local demos need durable state.

```python
from context_router import SQLiteMemoryStore

with SQLiteMemoryStore("context.db") as store:
    items = store.get_recent(top_k=5)
```

Close the store when finished. Reads after close follow normal `sqlite3` closed-connection behavior.

## Use token budgets

Use token budgets when selected context will be inserted into an LLM prompt. Budgets are approximate and should be treated as a guardrail, not exact tokenizer accounting.

Good uses:

- keep prompts predictable
- prevent low-priority context from crowding out useful context
- test how routing behaves under constrained context windows

## Troubleshooting common failures

- **Expected context missing**: inspect returned IDs, scores, and token budget drops.
- **Noisy context selected**: tune router weights or improve memory categories.
- **SQLite search returns too much or too little**: check FTS availability and query terms.
- **Benchmark regression**: compare `latest_results.json` before and after the change.
- **Slow routing**: run the synthetic benchmark and inspect average latency by router.

## Production limitations

- The built-in semantic model is suitable for a reference implementation, not a full production retrieval stack.
- Token estimates are approximate.
- Synthetic benchmark data is deterministic but not a replacement for production evaluation cases.
- SQLite is a pragmatic local store; large distributed systems may need a dedicated storage layer.

## Suggested monitoring fields

Capture structured routing events with fields such as:

- router
- query category or query hash
- latency_ms
- selected_count
- estimated_tokens
- selected context IDs
- score components
- precision/recall in offline benchmark jobs
