import os
import tempfile

from okc.bundle.document import OKFDocument
from okc.bundle.generator import generate_bundle
from okc.sources.sqlite import SQLiteSource


def test_sqlite_list_concepts(sqlite_fixture):
    source = SQLiteSource(f"sqlite:///{sqlite_fixture}")
    concepts = source.list_concepts()
    table_names = {c.id[-1] for c in concepts if c.kind == "table"}
    view_names = {c.id[-1] for c in concepts if c.kind == "view"}

    assert "users" in table_names
    assert "orders" in table_names
    assert "products" in table_names
    assert "order_items" in table_names
    assert "active_orders" in view_names


def test_sqlite_read_schema(sqlite_fixture):
    source = SQLiteSource(f"sqlite:///{sqlite_fixture}")
    concepts = source.list_concepts()
    users_ref = next(c for c in concepts if c.id[-1] == "users")
    schema = source.read_schema(users_ref)

    col_names = {c.name for c in schema.columns}
    assert "id" in col_names
    assert "email" in col_names
    assert "name" in col_names
    assert "created_at" in col_names

    id_col = next(c for c in schema.columns if c.name == "id")
    assert id_col.data_type == "INTEGER"
    email_col = next(c for c in schema.columns if c.name == "email")
    assert not email_col.nullable
    name_col = next(c for c in schema.columns if c.name == "name")
    assert name_col.nullable


def test_sqlite_read_constraints(sqlite_fixture):
    source = SQLiteSource(f"sqlite:///{sqlite_fixture}")
    concepts = source.list_concepts()

    users_ref = next(c for c in concepts if c.id[-1] == "users")
    constraints = source.read_constraints(users_ref)
    assert len(constraints) >= 1
    pk_constraints = [c for c in constraints if c.kind == "PRIMARY KEY"]
    assert len(pk_constraints) >= 1


def test_sqlite_read_indexes(sqlite_fixture):
    source = SQLiteSource(f"sqlite:///{sqlite_fixture}")
    concepts = source.list_concepts()
    orders_ref = next(c for c in concepts if c.id[-1] == "orders")
    indexes = source.read_indexes(orders_ref)
    assert len(indexes) >= 1
    idx_names = {i.name for i in indexes}
    assert "idx_orders_user_id" in idx_names


def test_sqlite_read_foreign_keys(sqlite_fixture):
    source = SQLiteSource(f"sqlite:///{sqlite_fixture}")
    fks = source.read_foreign_keys()
    fk_targets = {fk.target_table for fk in fks}
    assert "users" in fk_targets
    assert "orders" in fk_targets or "products" in fk_targets


def test_generate_bundle_sqlite(sqlite_fixture):
    source = SQLiteSource(f"sqlite:///{sqlite_fixture}")
    with tempfile.TemporaryDirectory() as tmpdir:
        generate_bundle(source, tmpdir)

        tables_dir = os.path.join(tmpdir, "tables")
        assert os.path.isdir(tables_dir)

        table_files = {f for f in os.listdir(tables_dir) if f.endswith(".md")}
        assert "users.md" in table_files
        assert "orders.md" in table_files
        assert "products.md" in table_files
        assert "order_items.md" in table_files

        views_dir = os.path.join(tmpdir, "views")
        assert os.path.isdir(views_dir)
        view_files = {f for f in os.listdir(views_dir) if f.endswith(".md")}
        assert "active_orders.md" in view_files

        users_path = os.path.join(tables_dir, "users.md")
        with open(users_path) as f:
            content = f.read()
        assert "## Schema" in content
        assert "## Constraints" in content
        assert "## Referenced by" in content

        orders_path = os.path.join(tables_dir, "orders.md")
        with open(orders_path) as f:
            content = f.read()
        assert "## Schema" in content
        assert "## Indexes" in content
        assert "## Relationships" in content

        assert os.path.exists(os.path.join(tmpdir, "index.md"))
