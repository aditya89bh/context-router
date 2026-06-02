# Versioning Policy

`context-router` follows semantic versioning: `MAJOR.MINOR.PATCH`.

## Semantic versioning

- `MAJOR` changes may include incompatible public API changes.
- `MINOR` changes add backward-compatible capabilities.
- `PATCH` changes fix bugs, documentation, packaging, or reliability issues without changing public behavior.

## v0.x expectations

Until `v1.0.0`, the project is production-readiness focused but still allowed to refine APIs when necessary. During `v0.x`:

- public APIs should remain stable whenever practical;
- breaking changes should be rare, documented, and justified;
- migration guidance should be included when behavior changes;
- internal implementation details may change without notice.

## v1.0 stability expectations

`v1.0.0` means the core routing, context item, store, configuration, benchmark, and observability APIs are considered stable for general use.

After `v1.0.0`:

- backward-incompatible public API changes require a major version bump;
- new optional capabilities should be introduced through minor releases;
- bug fixes and documentation corrections should use patch releases.

## Deprecation policy

Deprecated APIs should:

1. Emit a `DeprecationWarning` when used.
2. Include the replacement API when one exists.
3. Remain available for at least one minor release when possible.
4. Be documented in the changelog or release notes before removal.

The project uses lightweight standard-library deprecation helpers to keep warnings consistent without adding runtime dependencies.
