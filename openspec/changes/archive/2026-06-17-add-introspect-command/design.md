## Context

The `okc` repo is scaffolding-only (README, LICENSE, .gitignore, openspec config). This is the first real feature: a CLI command that introspects a SQLite or Postgres database and writes an OKF v0.1-conformant bundle. Google's reference enrichment agent exists but is LLM-heavy and BigQuery-only — this is a lean, deterministic alternative for SQLite and Postgres.

Key constraints:
- Zero AI dependencies (no Gemini, no ADK, no LLM calls)
- Only stdlib `sqlite3` + one external dep (`psycopg2-binary`) for Postgres
- Output must be strictly OKF v0.1 conformant

## Goals / Non-Goals

**Goals:**
- `okc introspect postgresql://user@host/db --out ./bundle` produces a valid OKF bundle
- `okc introspect sqlite:///path/to/db.sqlite --out ./bundle` produces a valid OKF bundle
- Captures tables, views, columns, types, nullability, defaults, constraints, indexes, foreign keys, and extended comments (`COMMENT ON`)
- Auto-detects backend from the URL scheme
- Generates cross-links between tables via foreign keys (bi-directional)
- Generates `index.md` files for progressive disclosure
- No LLM, no heavy framework dependencies

**Non-Goals:**
- Writing (modifying the database) — introspection only
- Other backends (MySQL, Snowflake, BigQuery) — future work
- OKF enrichment (LLM-generated prose, web crawl) — the reference agent handles that
- OKF consumption (visualization, querying) — future subcommands

## Decisions

### Backend auto-detection via URL scheme

Use Python's `urllib.parse.urlparse` to detect the backend from the URL scheme:

| Scheme | Backend |
|--------|---------|
| `sqlite:` | SQLite |
| `postgresql:` / `postgres:` | PostgreSQL |

This avoids a `--backend` flag. The URL is the single source of truth for what database to connect to.

### psycopg2-binary over psycopg (v3)

Selected `psycopg2-binary` because:
- Zero build-time dependencies (pre-compiled wheels)
- Battle-tested, widely deployed
- Synchronous-only is fine for a CLI tool — no benefit from psycopg v3's async support
- Simpler API for the schema introspection queries we need

### Source ABC pattern

```
Source (ABC)
├── list_concepts()         → list[ConceptRef]    # tables, views, matviews, with kind and schema
├── read_schema(ref)        → SchemaInfo          # columns, types, nullable, defaults, comments
├── read_constraints(ref)   → list[Constraint]    # PK, UK, CHECK, EXCLUSION
├── read_indexes(ref)       → list[Index]         # name, columns, unique, method
└── read_foreign_keys(db)   → list[ForeignKey]    # all FKs across the database (needs cross-table view)
```

`list_concepts` returns a `ConceptRef` with:
- `id: tuple[str, ...]` — hierarchical path, e.g. `("tables", "public", "users")`
- `type: str` — e.g. `"PostgreSQL Table"`
- `kind: str` — `"table"`, `"view"`, `"materialized_view"` (drives directory placement)
- `schema: str | None` — Postgres schema name, None for SQLite
- `comment: str | None` — extended property

`read_foreign_keys` operates on the full database (not a single table) so the generator can compute reverse references in a single pass.

### Nested directory structure for Postgres schemas

```
tables/
├── index.md
├── public/
│   ├── index.md
│   ├── users.md
│   └── orders.md
└── audit/
    ├── index.md
    └── change_log.md
```

For SQLite (no schemas), the structure collapses to a flat `tables/` directory.

### OKFDocument adapted from Google reference agent

The reference agent's `bundle/document.py` is clean and dependency-light. We adapt:
- `OKFDocument` dataclass with `frontmatter: dict` and `body: str`
- `serialize()` → string for file writing
- `parse(text)` → OKFDocument (useful for testing)
- `validate()` → raises on missing `type` field

### Cross-link generation

Two-phase:
1. Collect all foreign keys across the database
2. For each table, write `# Relationships` (outgoing FKs → target concept markdown links) and `# Referenced by` (incoming FKs ← source concept markdown links)

Links use bundle-absolute paths (`/tables/public/users.md`) per OKF's recommended form.

### Bundle generation pipeline

```
URL → URL parser → detect backend → Source instance
  → list_concepts() → for each concept:
      → read_schema(), read_constraints(), read_indexes() → OKFDocument
  → read_foreign_keys() → annotate each doc with cross-links
  → write all concept docs to disk
  → regenerate_indexes() bottom-up
```

## Risks / Trade-offs

- **SQLite constraint introspection is limited**: SQLite exposes indexes via `PRAGMA index_list` and `PRAGMA index_info`, but CHECK constraints are only available in SQLite 3.38+. Foreign keys require `PRAGMA foreign_key_list`. No `COMMENT ON` equivalent.
- **Postgres system catalog queries are version-sensitive**: `pg_catalog` queries for constraints and indexes vary subtly across PG versions. Stick to well-tested queries (`pg_class`, `pg_attribute`, `pg_constraint`, `pg_index`, `pg_description`).
- **No test database for CI**: Need to ship a small SQLite test fixture in the repo. Postgres tests require optional infra or mocking.
- **Large databases**: A schema with 500+ tables will produce 500+ files. OKF is designed for this, but the CLI should show progress output.
