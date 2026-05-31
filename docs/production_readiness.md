# Production Readiness

`context-router` is intentionally small, but the architecture is designed to grow into a production context-routing layer for agent systems.

## Current readiness

- Deterministic in-memory `MemoryStore` for local demos and tests
- Router interface via `BaseRouter`
- Four routing strategies: recency, semantic, task, and hybrid
- Token-budget-aware `ContextPack` selection
- CLI demo and runnable examples
- Evaluation runner and comparison benchmark
- CI across Python 3.10, 3.11, and 3.12

## Recommended production upgrades

### Storage

Replace the in-memory store with a durable adapter:

- SQLite for local-first agents
- Postgres for multi-user applications
- Redis for low-latency ephemeral context
- Vector databases such as FAISS, Qdrant, or Chroma for larger semantic indexes

### Embeddings

The default `HashingEmbeddingModel` is deterministic and useful for tests. Production systems should pass a sentence-transformers model or hosted embedding backend into `SemanticRouter` and `HybridRouter`.

### Token budgeting

The built-in token estimator is intentionally lightweight. For production LLM calls, swap in a model-specific tokenizer and enforce budgets before prompt assembly.

### Evaluation

Track router quality with domain-specific eval cases:

- precision@k
- category hit rate
- context reduction ratio
- latency per router
- answer quality with and without routed context

### Observability

Log routing metadata from `ContextPack.metadata`:

- query
- router
- selected memory IDs
- score breakdowns
- estimated tokens
- available vs selected context count

### Safety and privacy

Before sending context to a model:

- filter secrets and credentials
- separate user-private memory from shared/team memory
- apply retention policies
- audit category classifiers for leakage across domains

## Deployment checklist

- [ ] Choose durable memory backend
- [ ] Choose embedding model and cache policy
- [ ] Replace approximate token counter with model tokenizer
- [ ] Add domain-specific eval set
- [ ] Add latency and cost monitoring
- [ ] Add PII/secret filtering
- [ ] Define context retention policy
- [ ] Add release/versioning process

## Suggested next milestone

Add a `MemoryStore` protocol plus SQLite and vector-store implementations so router logic stays independent from persistence.
