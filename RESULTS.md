# Results

This file captures sample outputs from `context-router` and demonstrates how explicit context routing reduces prompt bloat.

## Sample routing outputs

### Personal assistant

Query:

```text
Help me plan my Greece trip
```

Expected selected context:

```text
[travel] Greece trip plan: Athens for history, Santorini for sunset, ferry buffer day, Schengen visa checklist.
[travel] Book refundable hotels near metro stations and keep one day open for island weather changes.
```

### Coding agent

Query:

```text
Fix Docker build failure
```

Expected selected context:

```text
[coding] Docker build failure: base image mismatch, missing system package, and cached layer invalidation steps.
[coding] CI test failures usually need pinned Python versions and reproducible requirements lockfile.
```

### Robotics agent

Query:

```text
Recover failed CNC pickup
```

Expected selected context:

```text
[robotics] CNC pickup recovery: retry perception, re-home gripper, verify workpiece pose, then resume safe trajectory.
[robotics] ROS/RViz debugging notes: inspect TF tree, joint states, and collision scene before planning.
```

## Context reduction examples

The demo store contains 7 context items. With `top_k=3`, each router sends at most 3 items downstream.

| Query | Router | Available items | Routed items | Reduction |
|---|---|---:|---:|---:|
| Help me plan my Greece trip | HybridRouter | 7 | 3 | 57.1% |
| Fix Docker build failure | HybridRouter | 7 | 3 | 57.1% |
| Recover failed CNC pickup | HybridRouter | 7 | 3 | 57.1% |
| Recover failed CNC pickup | TaskRouter | 7 | 2 | 71.4% |

## Benchmark table

These are lightweight local demo benchmarks, not production retrieval evaluations.

| Router | Query | Top result category | Notes |
|---|---|---|---|
| RecencyRouter | any | most recent category | Good for latest state, not intent-aware |
| SemanticRouter | Docker build failure | coding | Uses embedding similarity |
| TaskRouter | Greece trip | travel | Uses category keywords |
| TaskRouter | CNC pickup | robotics | Predictable domain routing |
| HybridRouter | CNC pickup | robotics | Balances relevance, freshness, importance |

## Sample CLI transcript

Run:

```bash
python -m context_router.demo --query "Recover failed CNC pickup" --router hybrid --top-k 3
```

Representative output:

```text
Query: Recover failed CNC pickup
Selected router: hybrid
Retrieved contexts:
  1. [robotics] CNC pickup recovery: retry perception, re-home gripper, verify workpiece pose, then resume safe trajectory.
     score=...
  2. [robotics] ROS/RViz debugging notes: inspect TF tree, joint states, and collision scene before planning.
     score=...
ContextPack summary: ContextPack(router=hybrid, items=3, categories=['coding', 'robotics'])
```

## Generated benchmark outputs

Generated with:

```bash
python -m context_router.benchmark
python -m context_router.evaluation
```

### Router comparison

| Router | Cases | Avg precision@k | Hit rate | Avg contexts | Context reduction |
|---|---:|---:|---:|---:|---:|
| recency | 3 | 0.333 | 1.000 | 3.0 | 57.1% |
| semantic | 3 | 0.667 | 1.000 | 3.0 | 57.1% |
| task | 3 | 1.000 | 1.000 | 2.0 | 71.4% |
| hybrid | 3 | 0.556 | 1.000 | 3.0 | 57.1% |

### Evaluation CSV

```csv
router,query,expected,precision_at_k,category_hit,retrieved_categories
recency,Help me plan my Greece trip,travel,0.333,True,robotics|coding|travel
recency,Fix Docker build failure,coding,0.333,True,robotics|coding|travel
recency,Recover failed CNC pickup,robotics,0.333,True,robotics|coding|travel
semantic,Help me plan my Greece trip,travel,0.667,True,travel|personal|travel
semantic,Fix Docker build failure,coding,0.667,True,coding|coding|travel
semantic,Recover failed CNC pickup,robotics,0.667,True,robotics|robotics|travel
task,Help me plan my Greece trip,travel,1.000,True,travel|travel
task,Fix Docker build failure,coding,1.000,True,coding|coding
task,Recover failed CNC pickup,robotics,1.000,True,robotics|robotics
hybrid,Help me plan my Greece trip,travel,0.333,True,travel|robotics|coding
hybrid,Fix Docker build failure,coding,0.667,True,coding|coding|robotics
hybrid,Recover failed CNC pickup,robotics,0.667,True,robotics|robotics|coding
```
