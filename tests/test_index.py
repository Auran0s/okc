import os
import tempfile

from okc.bundle.document import OKFDocument
from okc.bundle.index import regenerate_indexes


def _write_doc(dir_path: str, rel_path: str, type_label: str, title: str):
    full_path = os.path.join(dir_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    doc = OKFDocument(
        frontmatter={"type": type_label, "title": title},
        body=f"# {title}",
    )
    with open(full_path, "w") as f:
        f.write(doc.serialize())


def test_regenerate_indexes_creates_root_index():
    with tempfile.TemporaryDirectory() as tmpdir:
        _write_doc(tmpdir, "tables/users.md", "SQLite Table", "users")
        _write_doc(tmpdir, "tables/orders.md", "SQLite Table", "orders")

        regenerate_indexes(tmpdir)

        index_path = os.path.join(tmpdir, "index.md")
        assert os.path.exists(index_path)
        with open(index_path) as f:
            content = f.read()
        assert "tables/" in content

        tables_index = os.path.join(tmpdir, "tables", "index.md")
        assert os.path.exists(tables_index)
        with open(tables_index) as f:
            content = f.read()
        assert "SQLite Table" in content
        assert "users" in content
        assert "orders" in content


def test_regenerate_indexes_with_subdirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        _write_doc(tmpdir, "tables/public/users.md", "PostgreSQL Table", "users")
        _write_doc(tmpdir, "tables/public/orders.md", "PostgreSQL Table", "orders")
        _write_doc(tmpdir, "tables/audit/log.md", "PostgreSQL Table", "log")

        regenerate_indexes(tmpdir)

        assert os.path.exists(os.path.join(tmpdir, "index.md"))
        assert os.path.exists(os.path.join(tmpdir, "tables", "index.md"))
        assert os.path.exists(os.path.join(tmpdir, "tables", "public", "index.md"))
        assert os.path.exists(os.path.join(tmpdir, "tables", "audit", "index.md"))
