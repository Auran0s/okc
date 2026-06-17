import pytest

from okc.bundle.document import OKFDocument, ValidationError


def test_serialize_basic():
    doc = OKFDocument(
        frontmatter={"type": "Table", "title": "users"},
        body="# Schema\n\n| col | type |",
    )
    result = doc.serialize()
    assert result.startswith("---")
    assert "type: Table" in result
    assert "title: users" in result
    assert "---" in result
    assert "# Schema" in result


def test_serialize_empty_body():
    doc = OKFDocument(frontmatter={"type": "Table", "title": "users"})
    result = doc.serialize()
    assert "type: Table" in result


def test_parse_roundtrip():
    text = """---
type: Table
title: users
---

# Schema

| Name | Type |
"""
    doc = OKFDocument.parse(text)
    assert doc.frontmatter["type"] == "Table"
    assert doc.frontmatter["title"] == "users"
    assert "# Schema" in doc.body

    serialized = doc.serialize()
    doc2 = OKFDocument.parse(serialized)
    assert doc2.frontmatter == doc.frontmatter
    assert doc2.body.strip() == doc.body.strip()


def test_parse_no_frontmatter():
    with pytest.raises(ValidationError, match="Missing frontmatter"):
        OKFDocument.parse("just some text")


def test_validate_ok():
    doc = OKFDocument(frontmatter={"type": "Table", "title": "x", "timestamp": "now"})
    doc.validate()


def test_validate_missing_type():
    doc = OKFDocument(frontmatter={"title": "x"})
    with pytest.raises(ValidationError, match="type"):
        doc.validate()


def test_validate_missing_title():
    doc = OKFDocument(frontmatter={"type": "Table"})
    with pytest.raises(ValidationError, match="title"):
        doc.validate()
