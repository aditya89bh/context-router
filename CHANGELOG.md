# Changelog

All notable changes to `context-router` are documented here.

The project follows semantic versioning. See `docs/VERSIONING.md`.

## v0.1.0 - Initial public release

### Core routing

- Context routing primitives for task, recency, semantic, and hybrid routing.
- `ContextItem` and scored context abstractions.
- Router configuration through `RouterConfig`.
- Token budgeting for constrained context packs.

### Storage

- In-memory `MemoryStore`.
- Durable `SQLiteMemoryStore`.
- Store protocol abstraction for compatible storage implementations.

### Evaluation and benchmarking

- Evaluation metrics for precision, recall, and category hits.
- Deterministic benchmark runner and generated benchmark reports.
- Large synthetic benchmark dataset support.
- Deterministic benchmark fixture support for repeatable checks.

### Observability and operations

- Observability helpers for routing decisions and context packs.
- Production readiness documentation.
- Operations, benchmark interpretation, architecture, API reference, and release checklist docs.

### Reliability and release readiness

- CI, CodeQL, dependency audit, package build checks, and release notes.
- Lightweight deprecation utilities for future API transitions.
- PII filtering utility for optional text sanitization workflows.
- Context validation utilities for explicit field validation.
