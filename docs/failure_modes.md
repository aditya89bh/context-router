# Failure Modes

| Failure mode | Symptom | Cause | Mitigation |
|---|---|---|---|
| Stale context | Agent uses old project or customer state. | Recent changes were not stored or recency weight is too low. | Add freshness checks, tune recency weight, archive outdated items. |
| Wrong task classification | Task router returns the wrong category. | Keyword taxonomy is incomplete or ambiguous. | Add domain keywords, evaluate task cases, fall back to hybrid routing. |
| Weak semantic similarity | Semantic router misses obvious context. | Embedding fallback is lightweight or wording differs strongly. | Use production embeddings and add representative eval cases. |
| Over-reliance on recency | New but irrelevant context wins. | Recency score dominates ranking. | Lower recency weight or combine with semantic relevance. |
| Over-reliance on importance | High-priority but unrelated context wins. | Importance is static and not query-aware. | Use hybrid routing and review importance labels. |
| Token budget drops useful context | Expected item is ranked but absent from `ContextPack`. | Budget is too small or earlier items consume it. | Increase budget, reduce item size, or improve ranking. |
| Duplicate memories | Same fact appears multiple times. | Store has no deduplication process. | Add ingestion dedupe or periodic memory cleanup. |
| Noisy memory stores | Router returns broad or vague notes. | Items are low-quality or categories are too broad. | Improve memory authoring and filter by category/time/importance. |
| Benchmark overfitting | Metrics look good but real queries fail. | Eval cases are too small or too similar to demo data. | Add production-like cases and track regressions over time. |
