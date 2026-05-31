# Architecture Glossary

- **ContextItem**: One unit of context that may be sent to an agent, such as a customer note, incident detail, or robotics recovery step.
- **ScoredContextItem**: A `ContextItem` plus routing scores that explain why it was selected.
- **MemoryStore**: Lightweight in-memory storage for context items, useful for demos, tests, and small integrations.
- **SQLiteMemoryStore**: Durable standard-library SQLite storage with the same basic behavior as `MemoryStore`.
- **BaseRouter**: The shared interface every router follows: accept a query and return ranked `ScoredContextItem` objects.
- **RecencyRouter**: Selects the newest context first.
- **SemanticRouter**: Selects context based on text similarity to the query.
- **TaskRouter**: Selects context by classifying the query into a domain category.
- **HybridRouter**: Combines semantic relevance, recency, and importance into one weighted score.
- **RouterConfig**: Configuration object for router options such as `top_k`, score weights, and optional token budget.
- **ContextPack**: The final package of selected context, summaries, metadata, scores, and explanations for a downstream agent or LLM.
- **Token budget**: A limit applied while packaging context so the selected items stay within an approximate prompt budget.
- **Evaluation case**: A query with expected context IDs or categories used to measure routing quality.
- **Benchmark report**: Generated JSON or markdown output that summarizes router performance across evaluation cases.
