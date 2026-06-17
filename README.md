# okc - Open Knowledge CLI

Deterministic database introspection and OKF (Open Knowledge Format) bundle generation.

## Installation

```bash
pip install okc
```

Or from source:

```bash
git clone <repo-url>
cd okc
pip install -e .
```

## Usage

### Introspect a SQLite database

```bash
okc introspect sqlite:///path/to/database.db --out ./my-bundle
```

### Introspect a PostgreSQL database

```bash
okc introspect postgresql://user:password@localhost:5432/mydb --out ./my-bundle
```

### Default output directory

If `--out` is omitted, the bundle is written to `./okf-bundle`.

```bash
okc introspect sqlite:///path/to/database.db
```

## Output

The `okc introspect` command produces an OKF v0.1 bundle — a directory of markdown files:

```
okf-bundle/
├── index.md
├── tables/
│   ├── index.md
│   ├── users.md
│   └── orders.md
└── views/
    ├── index.md
    └── active_orders.md
```

Each concept document contains:
- YAML frontmatter with `type`, `title`, `description`, `resource`, `tags`, `timestamp`
- `# Schema` table with columns
- `# Constraints` (PK, UNIQUE, CHECK for tables)
- `# Indexes` for tables
- `# Relationships` (outgoing foreign keys)
- `# Referenced by` (incoming foreign keys)

## Supported Backends

| Backend     | URL Scheme                                      |
|-------------|-------------------------------------------------|
| SQLite      | `sqlite:///path/to/file.db`                     |
| PostgreSQL  | `postgresql://user@host/db`                     |

## Development

```bash
pip install -e ".[dev]"
pytest
```
