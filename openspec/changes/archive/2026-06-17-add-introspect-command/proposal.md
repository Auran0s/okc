## Why

OKC needs a first real command. The project is scaffolding with zero code. Adding `okc introspect` gives users an immediate, useful CLI: point it at a SQLite or Postgres database and get a conformant Open Knowledge Format (OKF) bundle — a directory of markdown files describing every table, view, column, constraint, index, and foreign-key relationship. This is the foundational producer for the okc ecosystem.

## What Changes

- Add `okc introspect <url> --out <dir>` subcommand
- New `src/okc/` package with CLI entry point (`cli.py`)
- Source backends: `sources/base.py` (ABC), `sources/sqlite.py`, `sources/postgres.py`
- Bundle layer: `bundle/document.py` (OKFDocument), `bundle/index.py`, `bundle/generator.py`
- Update root `pyproject.toml` with project metadata and dependencies
- No breaking changes (nothing existed before)

## Capabilities

### New Capabilities

- `db-introspect`: Read a SQLite or Postgres database URL, introspect its schema (tables, views, columns, constraints, indexes, foreign keys, extended comments), and produce a conformant OKF v0.1 bundle directory with cross-linked concept documents and index files.

### Modified Capabilities

*(none)*

## Impact

- New Python package `okc` at repo root with a `pyproject.toml`
- New `src/okc/` source tree (~8 files)
- Dependencies added: `pyyaml`, `psycopg2-binary`
- No existing code is modified (greenfield feature)
