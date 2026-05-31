# Architecture Decision Records

## Context routing is separate from memory storage

Routing decides what context should be sent to an agent. Storage decides where context lives. Keeping these concerns separate lets the same routers work with an in-memory store, SQLite, or future vector/database adapters without changing scoring logic.

## BaseRouter exists as a shared contract

`BaseRouter` gives every router the same shape: a store, a `top_k`, and a `route(query)` method returning scored context items. This makes routers swappable in demos, benchmarks, tests, and downstream agent integrations.

## ContextPack is the output boundary

Routers return ranked context. `ContextPack` turns those ranked items into the package a downstream agent should receive: memories, summaries, metadata, scores, explanations, and token-budget accounting. This keeps prompt assembly from depending on router internals.

## Token budgeting belongs close to ContextPack

Token budgeting is part of packaging, not retrieval. A router can rank many useful items, but `ContextPack` is where those items are constrained for a downstream model budget. The reusable helpers live in `context_router/context/token_budget.py` so budgeting stays centralized while `ContextPack` remains the boundary that applies it.

## Evaluation is required for routing quality

Context routing changes what an agent sees, so it needs measurable quality checks. The evaluation runner and benchmark provide lightweight metrics such as precision, recall, hit rate, and context reduction. These are intentionally simple so teams can replace the demo cases with domain-specific eval sets.

## Current non-goals

- Training a learned router or classifier
- Managing long-term memory lifecycle or retention policies
- Providing a production vector database integration
- Implementing model-specific tokenizers
- Performing prompt injection or PII redaction
- Optimizing latency across large-scale stores
