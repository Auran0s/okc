<div align="center">

# okc — Open Knowledge CLI

*Deterministic database introspection to structured markdown knowledge bundles*

</div>

**okc** reads a database schema and produces an **OKF (Open Knowledge Format)** bundle — a directory of cross-linked markdown documents that turn your schema into a navigable knowledge graph.

> [!NOTE]
> **OKF** is a specification for representing structured metadata as markdown files with YAML frontmatter. This project implements OKF v0.1.

## Features

- **Deterministic output** — same database, same schema, identical bundle every time
- **Multi-backend** — introspect SQLite and PostgreSQL databases (with a shared `Source` interface for adding more)
- **Standards-based** — generates valid OKF v0.1 documents with `type`, `title`, `description`, `resource`, `tags`, and `timestamp` frontmatter
- **Cross-linked** — foreign key relationships become navigable markdown links across documents
- **Auto-indexed** — `index.md` files are generated for every directory, listing both subdirectories and typed entries
- **Zero-config** — point it at a database URL and get a bundle; no config files needed

## Installation

Install from source:

```bash
git clone https://github.com/Auran0s/okc
cd okc
pip install -e .
```

For development, include the optional dev dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

Introspect a SQLite database and generate an OKF bundle:

```bash
okc introspect sqlite:///path/to/database.db --out ./my-bundle
```

This produces a directory tree like:

```
my-bundle/
├── index.md
├── tables/
│   ├── index.md
│   ├── users.md
│   ├── orders.md
│   └── products.md
└── views/
    ├── index.md
    └── active_orders.md
```

Each `.md` document contains YAML frontmatter and human-readable sections for the schema, constraints, indexes, and relationships — all cross-linked.

## Usage

### CLI Reference

```
okc introspect <url> [--out <dir>]
okc --version
```

| Argument / Flag | Required | Default | Description |
|---|---|---|---|
| `url` | Yes | — | Database URL (see [Supported Backends](#supported-backends)) |
| `--out` | No | `./okf-bundle` | Output directory for the generated bundle |
| `--version` | No | — | Print the version and exit |

### Examples

```bash
# Introspect a SQLite database
okc introspect sqlite:///path/to/database.db

# Introspect with a custom output directory
okc introspect sqlite:///path/to/database.db --out ./docs/database

# Introspect a PostgreSQL database
okc introspect postgresql://user:password@localhost:5432/mydb --out ./pg-bundle

# Show version
okc --version
```

## Supported Backends

| Backend | URL Scheme | Example |
|---|---|---|
| SQLite | `sqlite:///path/to/file.db` | `sqlite:///./data/mydb.sqlite` |
| PostgreSQL | `postgresql://user@host/db` | `postgresql://admin:secret@localhost:5432/mydb` |

> [!TIP]
> For PostgreSQL, you can use either `postgresql://` or `postgres://` scheme.

## OKF Bundle Format

Each concept document captures one database object (table, view, or materialized view). For PostgreSQL, schemas produce an additional nesting level.

### Document structure

```
my-bundle/
├── index.md                          # Root index: links to tables/, views/ + top-level docs
├── tables/
│   ├── index.md                      # Index of all table documents
│   ├── users.md                      # Document for the "users" table
│   ├── orders.md
│   └── products.md
└── views/
    ├── index.md                      # Index of all view documents
    └── active_orders.md              # Document for the "active_orders" view
```

For PostgreSQL databases with multiple schemas:

```
my-bundle/
└── tables/
    ├── index.md
    ├── public/
    │   ├── index.md
    │   ├── users.md
    │   └── orders.md
    └── audit/
        ├── index.md
        └── log.md
```

### Document metadata

Each `.md` file contains YAML frontmatter with:

```yaml
---
type: table
title: users
description: Registered user accounts
resource: sqlite:///path/to/database.db
tags: []
timestamp: "2026-06-17T12:00:00Z"
---
```

### Document body sections

- **## Schema** — columns table (name, type, nullable, default, description)
- **## Constraints** — primary keys, UNIQUE, CHECK, EXCLUSION constraints (tables only)
- **## Indexes** — index name, columns, uniqueness, index method (tables only)
- **## Relationships** — outgoing foreign keys with markdown cross-links to target tables
- **## Referenced by** — incoming foreign keys with markdown cross-links from source tables

## Development

### Setup

```bash
git clone https://github.com/Auran0s/okc
cd okc
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

The test suite includes self-contained tests using an in-memory SQLite database that exercises all schema features:

| Test file | Coverage |
|---|---|
| `tests/test_document.py` | OKFDocument serialization, parsing, and validation |
| `tests/test_index.py` | Index regeneration for flat and nested directory trees |
| `tests/test_sqlite_source.py` | SQL source introspection and end-to-end bundle generation |

> [!TIP]
> PostgreSQL tests require a running PostgreSQL instance and are not included in the default suite. Extend `tests/test_postgres_source.py` following the SQLite test pattern.

### Architecture

```
okc
├── cli.py            — argparse entry point, URL routing
├── sources/
│   ├── base.py       — Source ABC + dataclasses (ColumnInfo, Constraint, Index, ForeignKey, ...)
│   ├── sqlite.py     — SQLiteSource (stdlib sqlite3)
│   └── postgres.py   — PostgresSource (psycopg2)
└── bundle/
    ├── document.py   — OKFDocument dataclass (frontmatter + body, serialize/parse/validate)
    ├── generator.py  — generate_bundle(): concept list → FK maps → document writing
    ├── paths.py      — concept_id ↔ filesystem path conversion
    └── index.py      — regenerate_indexes(): recursive index.md generation
```

## Resources

- [OKF Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)

---

### Further reading

- The test fixtures in `tests/conftest.py` provide a good reference for the expected output format
- The `Source` ABC in `src/okc/sources/base.py` documents the interface for adding new backends
