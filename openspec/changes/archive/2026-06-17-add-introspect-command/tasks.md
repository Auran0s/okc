## 1. Project Setup

- [x] 1.1 Create `pyproject.toml` at repo root with `project` metadata, build config, and dependencies (`pyyaml`, `psycopg2-binary`)
- [x] 1.2 Create `src/okc/` package directory with `__init__.py` and `__main__.py`
- [x] 1.3 Create subdirectories: `sources/`, `bundle/` under `src/okc/`

## 2. OKF Bundle Layer

- [x] 2.1 Implement `bundle/document.py`: `OKFDocument` dataclass with `frontmatter: dict` and `body: str`, plus `serialize()`, `parse(text)`, and `validate()` methods
- [x] 2.2 Implement `bundle/paths.py`: `concept_id_to_path()`, `path_to_concept_id()`, and `parse_concept_id()` with valid path segment naming rules
- [x] 2.3 Implement `bundle/index.py`: `regenerate_indexes()` that walks the bundle tree bottom-up, groups concepts by frontmatter `type`, and writes `index.md` files with formatted listings

## 3. Source Abstraction

- [x] 3.1 Implement `sources/base.py`: `ConceptRef` dataclass (id, type, kind, schema, comment) and `Source` ABC with abstract methods `list_concepts()`, `read_schema()`, `read_constraints()`, `read_indexes()`, `read_foreign_keys()`
- [x] 3.2 Implement `sources/base.py`: `SchemaInfo`, `Constraint`, `Index`, `ForeignKey` dataclasses for structured schema data
- [x] 3.3 Implement `sources/base.py`: `ColumnInfo` dataclass (name, data_type, nullable, default, comment)

## 4. SQLite Source

- [x] 4.1 Implement `sources/sqlite.py`: `list_concepts()` querying `sqlite_master` for tables and views
- [x] 4.2 Implement `sources/sqlite.py`: `read_schema()` using `PRAGMA table_info()` for column metadata
- [x] 4.3 Implement `sources/sqlite.py`: `read_constraints()` using `PRAGMA index_list` + `PRAGMA index_info` for primary/unique, `PRAGMA foreign_key_list` for FKs
- [x] 4.4 Implement `sources/sqlite.py`: `read_indexes()` using `PRAGMA index_list` + `PRAGMA index_info`
- [x] 4.5 Implement `sources/sqlite.py`: `read_foreign_keys()` using `PRAGMA foreign_key_list` across all tables

## 5. PostgreSQL Source

- [x] 5.1 Implement `sources/postgres.py`: `list_concepts()` querying `pg_catalog.pg_class` + `pg_catalog.pg_namespace` for tables, views, and materialized views
- [x] 5.2 Implement `sources/postgres.py`: `read_schema()` querying `pg_catalog.pg_attribute`, `pg_catalog.pg_type`, `pg_catalog.pg_description` for column metadata and comments
- [x] 5.3 Implement `sources/postgres.py`: `read_constraints()` querying `pg_catalog.pg_constraint` for PK, UK, CHECK, EXCLUSION constraints
- [x] 5.4 Implement `sources/postgres.py`: `read_indexes()` querying `pg_catalog.pg_index` + `pg_catalog.pg_class`
- [x] 5.5 Implement `sources/postgres.py`: `read_foreign_keys()` querying `pg_catalog.pg_constraint` with `confrelid`/`confkey` for FK relationships

## 6. Bundle Generator

- [x] 6.1 Implement `bundle/generator.py`: `generate_bundle(source, out_dir)` that orchestrates the full pipeline — list concepts, read metadata, collect FKs, build OKFDocument objects with cross-links, write to disk
- [x] 6.2 Implement cross-link computation: collect all FKs, group by target table, annotate each OKFDocument with both outgoing `# Relationships` and incoming `# Referenced by` sections
- [x] 6.3 Generate frontmatter for each concept: compute `type`, `title`, `description`, `resource`, `tags`, `timestamp` according to OKF v0.1 spec

## 7. CLI

- [x] 7.1 Implement `cli.py`: `main()` with `argparse`, `okc introspect` subcommand, `--out` flag with default, positional URL argument, and `--version` flag
- [x] 7.2 Implement URL parsing: detect backend from URL scheme, construct appropriate Source instance, handle unsupported schemes with error message
- [x] 7.3 Wire CLI to `generate_bundle()` with progress output (table count, file count)

## 8. Tests

- [x] 8.1 Create `tests/` directory with `conftest.py` and a small SQLite test fixture (schema with tables, views, FKs, indexes)
- [x] 8.2 Write unit tests for `bundle/document.py`: OKFDocument serialization, parsing, validation
- [x] 8.3 Write unit tests for `bundle/index.py`: index generation from bundle structure
- [x] 8.4 Write integration tests for SQLite source: introspect the test fixture, verify output OKF structure
- [x] 8.5 Add `pytest` to optional dev dependencies in `pyproject.toml`

## 9. Polish

- [x] 9.1 Add progress output to CLI (e.g., "Introspecting... found 12 tables, 3 views")
- [x] 9.2 Add error handling for connection failures, permission errors, empty databases
- [x] 9.3 Add `--help` output that explains usage, supported backends, and OKF format
- [x] 9.4 Update root `README.md` with installation and usage instructions for `okc introspect`
