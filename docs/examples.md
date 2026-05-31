# Examples

All examples are professional, enterprise-friendly scenarios intended to show routing behavior without requiring external services.

## CLI demo

Command:

```bash
python -m context_router.demo
```

Demonstrates: default hybrid routing over the built-in demo store.

Expected output shape: query, selected router, ranked contexts, score details, and `ContextPack` summary.

## CLI demo with token budget

Command:

```bash
python -m context_router.demo --query "Fix Docker build failure" --router hybrid --max-tokens 40
```

Demonstrates: applying a token budget at the `ContextPack` boundary.

Expected output shape: routed contexts plus `Token budget: used/max estimated tokens`.

## Customer assistant example

Command:

```bash
python context_router/examples/customer_assistant.py
```

Demonstrates: task-category routing for customer automation meeting preparation.

Expected output shape: `ContextPack(router=task, ...)` followed by customer-category context items.

## Coding agent example

Command:

```bash
python context_router/examples/coding_agent.py
```

Demonstrates: task-category routing for Docker build and CI troubleshooting.

Expected output shape: `ContextPack(router=task, ...)` followed by coding-category context items.

## Robotics agent example

Command:

```bash
python context_router/examples/robotics_agent.py
```

Demonstrates: task-category routing for robotics/CNC recovery workflows.

Expected output shape: `ContextPack(router=task, ...)` followed by robotics-category context items.

## Benchmark runner

Command:

```bash
python -m context_router.benchmark
```

Demonstrates: router comparison across the default evaluation cases.

Expected output shape: a markdown summary table printed to stdout plus generated files:

- `benchmarks/results/latest_results.json`
- `benchmarks/results/latest_results.md`
