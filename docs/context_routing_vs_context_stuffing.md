# Context Routing vs. Context Stuffing

Agent systems often start by dumping every available memory into a prompt. That works for small demos, but it becomes fragile as memory grows. Context routing makes selection explicit and measurable.

| Dimension | Context stuffing | Context routing |
|---|---|---|
| Cost | Sends unnecessary tokens. | Sends a smaller selected set. |
| Latency | More prompt tokens and slower calls. | Less context to serialize and process. |
| Relevance | Important details compete with noise. | Routers rank context for the current query. |
| Debugging | Hard to know why an item was included. | Scores and explanations are attached to selected items. |
| Evaluation | Usually anecdotal. | Evaluation cases and benchmark reports track quality. |
| Failure modes | Prompt bloat, stale context, accidental leakage. | Misranking, weak classification, or budget drops are easier to inspect. |

## When stuffing is acceptable

- Very small memory sets
- Prototypes with no cost or latency constraints
- One-off debugging where all context is intentionally needed

## When routing is better

- Multi-agent systems
- Enterprise assistants with domain-specific memory
- Systems with token budgets
- Workflows where stale or irrelevant context can cause wrong actions
- Projects that need routing quality to be tested over time
