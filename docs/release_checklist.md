# Release Checklist

Use this checklist before tagging a release.

- [ ] Run tests: `python -m pytest`
- [ ] Run CLI demo: `python -m context_router.demo`
- [ ] Run max-token demo: `python -m context_router.demo --max-tokens 40`
- [ ] Run benchmark: `python -m context_router.benchmark`
- [ ] Confirm `benchmarks/results/latest_results.json` exists
- [ ] Confirm `benchmarks/results/latest_results.md` exists
- [ ] Inspect `RESULTS.md`
- [ ] Check README examples and commands
- [ ] Check API docs and example docs
- [ ] Confirm GitHub CI passes on Python 3.10, 3.11, and 3.12
- [ ] Tag release, for example: `git tag v0.1.0`
- [ ] Push tag: `git push origin v0.1.0`
- [ ] Create GitHub release notes from `docs/releases/v0.1.0.md`
