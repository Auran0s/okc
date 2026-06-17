import sqlite3
from typing import Optional

from okc.sources.base import (
    ColumnInfo,
    ConceptRef,
    Constraint,
    ForeignKey,
    Index,
    SchemaInfo,
    Source,
)


_SKIP_TABLES = frozenset({
    "sqlite_sequence",
    "sqlite_stat1",
    "sqlite_stat2",
    "sqlite_stat3",
    "sqlite_stat4",
})


class SQLiteSource(Source):
    def __init__(self, url: str) -> None:
        self._url = url
        self._path = _parse_sqlite_url(url)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.execute("PRAGMA journal_mode=OFF")
        return conn

    def list_concepts(self) -> list[ConceptRef]:
        concepts: list[ConceptRef] = []
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') ORDER BY name"
            ).fetchall()
            for name, kind in rows:
                if kind == "table" and name.startswith("sqlite_"):
                    continue
                if name in _SKIP_TABLES:
                    continue
                if kind == "table":
                    type_label = "SQLite Table"
                    concept_id = ("tables", name)
                else:
                    type_label = "SQLite View"
                    concept_id = ("views", name)
                concepts.append(ConceptRef(
                    id=concept_id,
                    type=type_label,
                    kind=kind,
                ))
        return concepts

    def read_schema(self, ref: ConceptRef) -> SchemaInfo:
        table_name = ref.id[-1]
        columns: list[ColumnInfo] = []
        with self._connect() as conn:
            rows = conn.execute(f"PRAGMA table_info({_quote(table_name)})").fetchall()
            for cid, name, dtype, notnull, default, pk in rows:
                columns.append(ColumnInfo(
                    name=name,
                    data_type=dtype,
                    nullable=not notnull,
                    default=default,
                ))
        return SchemaInfo(columns=columns)

    def read_constraints(self, ref: ConceptRef) -> list[Constraint]:
        table_name = ref.id[-1]
        constraints: list[Constraint] = []
        if ref.kind != "table":
            return constraints
        with self._connect() as conn:
            pk_cols = []
            table_info = conn.execute(f"PRAGMA table_info({_quote(table_name)})").fetchall()
            for cid, name, dtype, notnull, default, pk in table_info:
                if pk:
                    pk_cols.append((pk, name))
            if pk_cols:
                pk_cols.sort(key=lambda x: x[0])
                constraints.append(Constraint(
                    name="",
                    kind="PRIMARY KEY",
                    columns=[c[1] for c in pk_cols],
                ))

            rows = conn.execute(f"PRAGMA index_list({_quote(table_name)})").fetchall()
            for seqno, name, unique, origin, partial in rows:
                if origin == "u":
                    info = conn.execute(
                        f"PRAGMA index_info({_quote(name)})"
                    ).fetchall()
                    cols = [row[2] for row in info]
                    constraints.append(Constraint(
                        name=name,
                        kind="UNIQUE",
                        columns=cols,
                    ))
        return constraints

    def read_indexes(self, ref: ConceptRef) -> list[Index]:
        table_name = ref.id[-1]
        indexes: list[Index] = []
        if ref.kind != "table":
            return indexes
        with self._connect() as conn:
            rows = conn.execute(f"PRAGMA index_list({_quote(table_name)})").fetchall()
            for seqno, name, unique, origin, partial in rows:
                if origin in ("pk", "u"):
                    continue
                info = conn.execute(
                    f"PRAGMA index_info({_quote(name)})"
                ).fetchall()
                cols = [row[2] for row in info]
                indexes.append(Index(
                    name=name,
                    columns=cols,
                    unique=bool(unique),
                    method="btree",
                ))
        return indexes

    def read_foreign_keys(self) -> list[ForeignKey]:
        fks: list[ForeignKey] = []
        with self._connect() as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchall()
            for (tname,) in tables:
                if tname in _SKIP_TABLES:
                    continue
                rows = conn.execute(f"PRAGMA foreign_key_list({_quote(tname)})").fetchall()
                for row in rows:
                    fks.append(ForeignKey(
                        name=row[2] or f"fk_{tname}_{row[3]}",
                        source_table=tname,
                        source_columns=[row[3]],
                        target_table=row[2],
                        target_columns=[row[4]],
                    ))
        return fks


def _parse_sqlite_url(url: str) -> str:
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///"):]
    if url.startswith("sqlite://"):
        return url[len("sqlite://"):]
    if url.startswith("sqlite:"):
        return url[len("sqlite:"):]
    return url


def _quote(name: str) -> str:
    return f'"{name}"'
