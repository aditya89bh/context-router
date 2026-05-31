# Latest Router Benchmark

Generated at: `2026-05-31T21:19:18.040963+00:00`

## Summary by router

| Router | Cases | Avg precision | Avg recall | Avg selected | Avg latency ms |
|---|---:|---:|---:|---:|---:|
| recency | 3 | 0.333 | 0.500 | 3.0 | 0.019 |
| semantic | 3 | 0.667 | 1.000 | 3.0 | 0.792 |
| task | 3 | 1.000 | 1.000 | 2.0 | 0.017 |
| hybrid | 3 | 0.667 | 1.000 | 3.0 | 0.810 |

## Per-query results

| Router | Query | Expected IDs | Returned IDs | Precision | Recall | Selected | Latency ms |
|---|---|---|---|---:|---:|---:|---:|
| recency | Prepare for the customer automation meeting | customer-actions, customer-profile | robot-cnc, coding-docker, customer-profile | 0.333 | 0.500 | 3 | 0.021 |
| recency | Fix Docker build failure in CI | coding-ci, coding-docker | robot-cnc, coding-docker, customer-profile | 0.333 | 0.500 | 3 | 0.019 |
| recency | Recover failed CNC pickup on the robot cell | robot-cnc, robot-ros | robot-cnc, coding-docker, customer-profile | 0.333 | 0.500 | 3 | 0.018 |
| semantic | Prepare for the customer automation meeting | customer-actions, customer-profile | customer-profile, customer-actions, coding-ci | 0.667 | 1.000 | 3 | 0.800 |
| semantic | Fix Docker build failure in CI | coding-ci, coding-docker | coding-ci, coding-docker, planning-calendar | 0.667 | 1.000 | 3 | 0.791 |
| semantic | Recover failed CNC pickup on the robot cell | robot-cnc, robot-ros | robot-cnc, robot-ros, customer-profile | 0.667 | 1.000 | 3 | 0.785 |
| task | Prepare for the customer automation meeting | customer-actions, customer-profile | customer-profile, customer-actions | 1.000 | 1.000 | 2 | 0.021 |
| task | Fix Docker build failure in CI | coding-ci, coding-docker | coding-docker, coding-ci | 1.000 | 1.000 | 2 | 0.016 |
| task | Recover failed CNC pickup on the robot cell | robot-cnc, robot-ros | robot-cnc, robot-ros | 1.000 | 1.000 | 2 | 0.015 |
| hybrid | Prepare for the customer automation meeting | customer-actions, customer-profile | customer-profile, customer-actions, robot-cnc | 0.667 | 1.000 | 3 | 0.816 |
| hybrid | Fix Docker build failure in CI | coding-ci, coding-docker | coding-docker, coding-ci, customer-profile | 0.667 | 1.000 | 3 | 0.803 |
| hybrid | Recover failed CNC pickup on the robot cell | robot-cnc, robot-ros | robot-cnc, robot-ros, coding-docker | 0.667 | 1.000 | 3 | 0.811 |
