## Context

A security audit identified 6 findings across the okc codebase. All are code-quality and hardening issues — no breaking changes required. The codebase is a Python CLI with SQLite (stdlib) and PostgreSQL (psycopg2) database introspection, writing OKF bundle files to disk.

## Goals / Non-Goals

**Goals:**
- Prevent path traversal when writing bundle files from malicious database metadata
- Validate identifiers before interpolating into SQLite PRAGMA queries
- Reduce PostgreSQL credential exposure through CLI process listing
- Pin minimum dependency versions for reproducible builds
- Suppress raw exception details from CLI output

**Non-Goals:**
- No behavioral changes to the introspection logic
- No new user-facing features
- No changes to the OKF document format or schema
- No breaking changes — all existing CLI usage patterns continue to work

## Decisions

### 1. Path Traversal: Validate + Guard

Two-layer defense:
1. **Segment validation** in `concept_id_to_path()` — reuse the existing `_SEGMENT_RE` regex (`^[a-zA-Z][a-zA-Z0-9_\-.]*$`) to reject any concept ID segment containing `../`, null bytes, or shell-special characters.
2. **Real-path containment** in `generate_bundle()` — resolve `os.path.realpath()` on both `out_dir` and the final write path, then verify the write path starts with the output directory.

Alternative considered: Stripping/replacing `../` instead of rejecting. Rejected because silent normalization could still allow unexpected writes and creates ambiguity during debugging.

### 2. SQLite Identifier Quoting: Validate, Don't Escape

Apply the same `_SEGMENT_RE` regex to table/schema names in `_quote()` before they enter PRAGMA queries. Rejecting invalid identifiers entirely (rather than attempting to escape embedded quotes) is safer and simpler.

Alternative considered: Properly escaping embedded `"` as `""` in the SQLite dialect. Rejected because table names from database metadata should never contain such characters in practice, and rejection catches the real attack vector (crafted malicious database) more decisively.

### 3. PostgreSQL Password Exposure: Document + Environment Variable

Update the CLI help text for the `url` argument to recommend `PGPASSWORD` environment variable instead of embedding passwords in the URL. The URL-parsing code remains unchanged (backwards-compatible) but usage is now discouraged.

Alternative considered: Adding a `--password` flag with `getpass` prompt to hide input. Rejected because psycopg2 already supports `PGPASSWORD`, `.pgpass`, and `PG*` environment variables natively — reinventing that is unnecessary scope.

### 4. Error Message Hardening

Replace bare `print(f"Error: {e}", file=sys.stderr)` with a user-facing message and move the detail behind an optional `--verbose` flag. The `argparse` parser gets a `--verbose` flag added to the `introspect` subparser.

### 5. Dependency Pinning

Pin `pyyaml>=6.0` (safe_load was added in 6.0 — `yaml.load()` without Loader was removed) and `psycopg2-binary>=2.9` (stable modern baseline). No upper bounds to avoid conflicts.

## Risks / Trade-offs

- **Rejecting identifiers** → If a legitimate database contains table names with characters outside `[a-zA-Z][a-zA-Z0-9_\-.]*`, it would fail. In practice, SQLite and PostgreSQL already restrict identifiers to alphanumeric + underscore, so this is safe.
- **PGPASSWORD recommendation** → Existing users embedding passwords in URLs continue to work. Migration is opt-in via documentation.
- **Verbose flag** → `--verbose` is added only to the `introspect` subparser to keep scope contained; other subcommands (if added later) would need their own.
