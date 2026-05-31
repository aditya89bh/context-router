# Router Selection Guide

## Recommended default

Use `HybridRouter` as the default for most production-like systems. It balances semantic relevance, freshness, and importance while keeping score details inspectable.

## RecencyRouter

Use when latest state matters most, such as recent incidents, active tickets, or live operations notes.

Do not use when older but semantically relevant context is critical.

## SemanticRouter

Use when users ask natural-language questions and wording should drive retrieval.

Do not use alone when stale or low-importance items are risky.

## TaskRouter

Use when queries map cleanly to known enterprise categories such as customer, coding, or robotics.

Do not use when categories overlap heavily or when the taxonomy is incomplete.

## HybridRouter

Use when you need a practical default across mixed workloads. Tune weights with `RouterConfig` and benchmark results.

Do not use without evaluation if downstream actions are high impact.

## Example use cases

- Customer meeting preparation: `TaskRouter` or `HybridRouter`
- Docker build incident: `SemanticRouter` or `HybridRouter`
- Robotics recovery workflow: `TaskRouter` or `HybridRouter`
- Latest handoff notes: `RecencyRouter`
