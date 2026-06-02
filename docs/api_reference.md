# API Reference

## Context types

### `ContextItem`

A single retrievable context unit.

Fields: `id`, `text`, `timestamp`, `category`, `importance`, optional `metadata`.

### `ScoredContextItem`

A `ContextItem` plus router score metadata.

Fields: `item`, `score`, `scores`.

### `ContextPack`

Output boundary for downstream agents. Use `ContextPack.from_scored(...)` to package routed items with summaries, score metadata, explanations, and token-budget accounting.

## Stores

### `ContextStoreProtocol`

Structural protocol for store implementations. Defines `add()`, `all()`, `search()`, `get_recent()`, and `get_by_category()`.

### `MemoryStore`

In-memory store for demos and tests.

Methods: `add()`, `all()`, `search()`, `get_recent()`, `get_by_category()`.

### `SQLiteMemoryStore`

SQLite-backed store using only the Python standard library. Supports the same read/write behavior as `MemoryStore`, plus `close()` and context manager usage.

```python
with SQLiteMemoryStore("context.db") as store:
    store.add(item)
```

## Routers

### `BaseRouter`

Shared router contract. Routers expose `route(query) -> list[ScoredContextItem]`.

### `RouterConfig`

Configuration object for router behavior.

Fields: `top_k`, `semantic_weight`, `recency_weight`, `importance_weight`, `max_tokens`.

### `RecencyRouter`

Returns the most recent context items.

### `SemanticRouter`

Ranks context by embedding similarity. Defaults to a deterministic hashing embedder for lightweight local use; production callers can pass a sentence-transformers model.

### `TaskRouter`

Classifies a query into a domain category and returns matching context items.

### `HybridRouter`

Combines semantic, recency, and importance scores. Defaults to `0.5 / 0.3 / 0.2` weights and supports custom direct weights or `RouterConfig`.

## Evaluation helpers

- `precision_at_k(...)`
- `recall_at_k(...)`
- `evaluate_results(...)`
- `evaluate_router(...)`
- `evaluate_all(...)`
- `format_results(...)`

Use these to compare router quality against expected context IDs or categories.

## Token budget helpers

Defined in `context_router.context.token_budget`:

- `estimate_tokens(text)`
- `select_with_token_budget(scored_items, max_tokens)`
- `token_budget_metadata(scored_items)`

These helpers are intentionally lightweight and can be replaced by model-specific tokenizers in production integrations.

## Utility helpers

- `context_router.deprecation`: standard-library deprecation warning helpers.
- `context_router.context.pii_filter.sanitize_text`: optional email, phone, and API-key-like redaction utility.
- `context_router.context.validation`: explicit context field validation helpers.
