## Why

A security audit of the okc codebase identified 6 findings across code, dependencies, and CLI behavior. While no findings are CRITICAL or HIGH, the path traversal and SQL injection vectors are genuine exploitation paths when introspecting a malicious database. Addressing them now prevents future regressions as the project grows.

## What Changes

- **Path traversal prevention**: Validate concept ID segments in `concept_id_to_path()` and guard bundle output writes with a real-path containment check
- **SQLite identifier quoting**: Validate table/schema names before interpolating into PRAGMA queries; reject invalid identifiers
- **PostgreSQL password exposure**: Document `PGPASSWORD` environment variable as the recommended way to supply credentials; deprecate embedding passwords in connection URLs (no breaking change — still functional)
- **Dependency version pinning**: Set minimum versions for `pyyaml>=6.0` and `psycopg2-binary>=2.9` in `pyproject.toml`
- **Verbose error messages**: Suppress raw exception messages in CLI output; use a generic user-facing message and log details under a `--verbose` flag
- All fixes are backwards-compatible — no breaking changes

## Capabilities

### New Capabilities

None — this change hardens existing code paths without introducing new user-facing capabilities.

### Modified Capabilities

None — no spec-level behavior changes.

## Impact

- **`src/okc/bundle/paths.py`**: Add segment validation to `concept_id_to_path()`
- **`src/okc/bundle/generator.py`**: Add path containment guard around file writes
- **`src/okc/sources/sqlite.py`**: Add identifier validation in `_quote()`
- **`src/okc/cli.py`**: Suppress raw exception messages, update help text for URL argument
- **`pyproject.toml`**: Pin `pyyaml>=6.0` and `psycopg2-binary>=2.9`
- No new dependencies required
