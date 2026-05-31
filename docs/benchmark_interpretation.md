# Benchmark Interpretation Guide

The benchmark output is a lightweight routing-quality check. It is not a claim of model accuracy; it shows whether routers select expected context items for the included evaluation cases.

## Fields

- **expected ids**: Context item IDs that should be retrieved for a query.
- **returned ids**: Context item IDs actually returned by a router.
- **precision**: Of the returned IDs, the fraction that were expected.
- **recall**: Of the expected IDs, the fraction that were returned.
- **selected count**: Number of context items returned for that query.

## Reading precision and recall

High recall with low precision means the router finds expected items but also includes too much unrelated context. That can increase cost and distract the downstream model.

High precision with low recall means returned items are relevant but incomplete. That can omit context the agent needs to answer or act correctly.

Good routing usually needs both: enough expected context and not too much noise.

## Reading `latest_results.json`

`benchmarks/results/latest_results.json` is machine-readable. Use it for CI checks, regression tracking, or custom dashboards. Each row contains router name, query, expected IDs, returned IDs, precision, recall, and selected count.

## Reading `latest_results.md`

`benchmarks/results/latest_results.md` is human-readable. Use the summary table to compare routers quickly, then inspect the per-query table to understand specific misses or noisy selections.
