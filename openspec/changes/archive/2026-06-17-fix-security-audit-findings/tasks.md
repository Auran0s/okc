## 1. Path Traversal Prevention

- [x] 1.1 Add segment validation to `concept_id_to_path()` in `src/okc/bundle/paths.py` — reuse `_SEGMENT_RE` regex to reject segments containing `..`, `/`, or other traversal characters before joining
- [x] 1.2 Add real-path containment guard in `generate_bundle()` in `src/okc/bundle/generator.py` — resolve `os.path.realpath()` on both `out_dir` and the write path, and verify the write path stays within the output directory

## 2. SQLite Identifier Quoting Hardening

- [x] 2.1 Add identifier validation in `_quote()` in `src/okc/sources/sqlite.py` — validate the name against `_SEGMENT_RE` and raise `ValueError` for invalid identifiers before wrapping in double quotes

## 3. PostgreSQL Credential Exposure

- [x] 3.1 Update the `url` argument help text in `src/okc/cli.py` — add note recommending `PGPASSWORD` environment variable instead of embedding passwords in the URL

## 4. Dependency Version Pinning

- [x] 4.1 Pin `pyyaml>=6.0` and `psycopg2-binary>=2.9` in `pyproject.toml`’s `dependencies` list

## 5. Verbose Error Message Hardening

- [x] 5.1 Suppress raw exception messages in `_handle_introspect()` in `src/okc/cli.py` — replace bare `error(str(e))` with a generic user-facing message when `--json` is not set; keep raw message only in JSON output or debug scenarios

## 6. Test & Verify

- [x] 6.1 Run existing tests with `python -m pytest` to confirm no regressions
- [x] 6.2 Lint with `ruff check src/` to verify code quality
