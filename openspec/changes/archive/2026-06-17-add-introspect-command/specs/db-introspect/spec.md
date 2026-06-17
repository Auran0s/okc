## ADDED Requirements

### Requirement: CLI parses database URLs

The system SHALL accept a database URL as a positional argument and auto-detect the backend from the URL scheme.

#### Scenario: SQLite URL detection
- **WHEN** user runs `okc introspect sqlite:///var/data/prod.db --out ./bundle`
- **THEN** the SQLite backend is selected

#### Scenario: Postgres URL detection
- **WHEN** user runs `okc introspect postgresql://user:pass@localhost:5432/mydb --out ./bundle`
- **THEN** the PostgreSQL backend is selected

#### Scenario: Unsupported URL scheme
- **WHEN** user runs `okc introspect mysql://user@host/db --out ./bundle`
- **THEN** the system SHALL exit with a non-zero code and an error message listing supported backends

### Requirement: CLI accepts --out flag

The system SHALL accept `--out <path>` to specify the output bundle directory. If omitted, SHALL default to `./okf-bundle`.

#### Scenario: Custom output directory
- **WHEN** user runs `okc introspect sqlite:///db.db --out /tmp/my-bundle`
- **THEN** the bundle is written to `/tmp/my-bundle/`

#### Scenario: Default output directory
- **WHEN** user runs `okc introspect sqlite:///db.db`
- **THEN** the bundle is written to `./okf-bundle/`

### Requirement: Source introspects tables

The system SHALL enumerate all user tables in the database as OKF concept documents under a `tables/` subdirectory in the bundle.

#### Scenario: SQLite enumerates tables
- **WHEN** user runs `okc introspect sqlite:///test.db --out ./bundle`
- **THEN** a `tables/` directory is created with one `.md` file per table

#### Scenario: Postgres enumerates tables by schema
- **WHEN** user runs `okc introspect postgresql://host/db --out ./bundle`
- **THEN** tables are organized into subdirectories by Postgres schema (e.g., `tables/public/`, `tables/audit/`)

### Requirement: Source introspects views

The system SHALL enumerate all views in the database as OKF concept documents under a `views/` subdirectory (or `views/<schema>/` for Postgres). Views SHALL include schema columns but not constraints or indexes.

#### Scenario: SQLite has no views
- **WHEN** the database has no views
- **THEN** the `views/` directory SHALL be omitted from the bundle

#### Scenario: Postgres views with schemas
- **WHEN** the Postgres database has views in the `public` schema
- **THEN** a `views/public/` directory is created with one `.md` file per view

### Requirement: Concept documents include schema columns

Each table and view concept document SHALL include a `# Schema` markdown table with columns: name, type, nullable, default, description.

#### Scenario: Table with columns
- **WHEN** a table `users` has columns `id`, `email`, `created_at`
- **THEN** `tables/users.md` SHALL contain a `# Schema` section with a markdown table listing all columns

#### Scenario: Column comments captured
- **WHEN** a Postgres column has a comment set via `COMMENT ON COLUMN`
- **THEN** the comment SHALL appear in the `Description` column of the schema table

### Requirement: Concept documents include constraints

Table concept documents SHALL include a `# Constraints` section listing primary keys, unique constraints, check constraints, and exclusion constraints.

#### Scenario: Table has primary key
- **WHEN** table `users` has a primary key on `id`
- **THEN** `tables/users.md` SHALL list the primary key constraint with name and columns

#### Scenario: SQLite table has no explicit constraints
- **WHEN** SQLite table has only an implicit `rowid` and no explicit constraints
- **THEN** the `# Constraints` section SHALL be omitted

### Requirement: Concept documents include indexes

Table concept documents SHALL include an `# Indexes` section listing index name, columns, uniqueness, and index method (where available).

#### Scenario: Table has unique index
- **WHEN** table `users` has a unique index on `email`
- **THEN** `tables/users.md` SHALL list the index with `unqiue: yes`

### Requirement: Concept documents include foreign key relationships

Table concept documents SHALL include a `# Relationships` section for outgoing foreign keys and a `# Referenced by` section for incoming foreign keys. Each entry SHALL be a markdown cross-link to the related concept document using bundle-absolute paths.

#### Scenario: Table references another table
- **WHEN** `orders.user_id` references `users.id`
- **THEN** `tables/orders.md` SHALL list `user_id → [users](/tables/users.md)` under `# Relationships`

#### Scenario: Table is referenced by another table
- **WHEN** `orders.user_id` references `users.id`
- **THEN** `tables/users.md` SHALL list `[orders](/tables/orders.md) via user_id` under `# Referenced by`

### Requirement: Generated index files

The system SHALL generate `index.md` files for each directory in the bundle, listing contained concepts grouped by type.

#### Scenario: Root index
- **WHEN** the bundle has `tables/` and `views/` directories
- **THEN** the root `index.md` SHALL list each subdirectory with a brief description

#### Scenario: Schema-level index for Postgres
- **WHEN** Postgres has `tables/public/` with tables
- **THEN** `tables/public/index.md` SHALL be generated

### Requirement: OKF frontmatter

Each concept document SHALL have valid YAML frontmatter with required fields: `type`, `title`, `description`, `timestamp`.

#### Scenario: Frontmatter for a table
- **WHEN** a concept document is written for table `users`
- **THEN** the frontmatter SHALL include:
  - `type`: `SQLite Table` or `PostgreSQL Table`
  - `title`: the table name
  - `description`: a description derived from the table comment or a summary of columns
  - `resource`: the connection URL
  - `tags`: `[<schema>, table]`
  - `timestamp`: ISO 8608601 timestamp of generation

### Requirement: Frontmatter type values

The `type` field SHALL use backend-specific type names.

#### Scenario: SQLite table type
- **WHEN** introspecting a SQLite table
- **THEN** `type` SHALL be `SQLite Table`

#### Scenario: PostgreSQL table type
- **WHEN** introspecting a PostgreSQL table
- **THEN** `type` SHALL be `PostgreSQL Table`

#### Scenario: PostgreSQL view type
- **WHEN** introspecting a PostgreSQL view
- **THEN** `type` SHALL be `PostgreSQL View`
