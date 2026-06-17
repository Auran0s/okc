from typing import Optional
from urllib.parse import urlparse

from okc.sources.base import (
    ColumnInfo,
    ConceptRef,
    Constraint,
    ForeignKey,
    Index,
    SchemaInfo,
    Source,
)


class PostgresSource(Source):
    def __init__(self, url: str) -> None:
        self._url = url
        self._dsn = _parse_postgres_url(url)

    def _conn(self):
        import psycopg2
        return psycopg2.connect(**self._dsn)

    def list_concepts(self) -> list[ConceptRef]:
        concepts: list[ConceptRef] = []
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    n.nspname AS schema_name,
                    c.relname AS relname,
                    c.relkind
                FROM pg_catalog.pg_class c
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                  AND c.relkind IN ('r', 'v', 'm')
                  AND pg_catalog.pg_table_is_visible(c.oid)
                ORDER BY n.nspname, c.relname
            """)
            for schema_name, relname, relkind in cur.fetchall():
                if relkind == "r":
                    type_label = "PostgreSQL Table"
                    kind = "table"
                    dir_name = "tables"
                elif relkind == "v":
                    type_label = "PostgreSQL View"
                    kind = "view"
                    dir_name = "views"
                elif relkind == "m":
                    type_label = "PostgreSQL Materialized View"
                    kind = "materialized_view"
                    dir_name = "views"
                else:
                    continue
                concept_id = (dir_name, schema_name, relname)
                concepts.append(ConceptRef(
                    id=concept_id,
                    type=type_label,
                    kind=kind,
                    schema=schema_name,
                ))
        return concepts

    def read_schema(self, ref: ConceptRef) -> SchemaInfo:
        schema_name, relname = ref.id[1], ref.id[2]
        columns: list[ColumnInfo] = []
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    a.attname AS col_name,
                    pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                    a.attnotnull AS not_null,
                    pg_catalog.pg_get_expr(d.adbin, d.adrelid) AS default_expr,
                    d.oid IS NOT NULL AS has_default,
                    des.description
                FROM pg_catalog.pg_attribute a
                JOIN pg_catalog.pg_class c ON c.oid = a.attrelid
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
                LEFT JOIN pg_catalog.pg_description des ON des.objoid = a.attrelid AND des.objsubid = a.attnum
                WHERE n.nspname = %s
                  AND c.relname = %s
                  AND a.attnum > 0
                  AND NOT a.attisdropped
                ORDER BY a.attnum
            """, (schema_name, relname))
            for col_name, data_type, not_null, default_expr, has_default, description in cur.fetchall():
                columns.append(ColumnInfo(
                    name=col_name,
                    data_type=data_type,
                    nullable=not not_null,
                    default=default_expr if has_default else None,
                    comment=description,
                ))
        return SchemaInfo(columns=columns)

    def read_constraints(self, ref: ConceptRef) -> list[Constraint]:
        schema_name, relname = ref.id[1], ref.id[2]
        constraints: list[Constraint] = []
        if ref.kind != "table":
            return constraints
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    con.conname AS con_name,
                    con.contype AS con_type,
                    ARRAY(
                        SELECT a.attname
                        FROM pg_catalog.pg_attribute a
                        WHERE a.attrelid = con.conrelid
                          AND a.attnum = ANY(con.conkey)
                        ORDER BY a.attnum
                    ) AS con_cols
                FROM pg_catalog.pg_constraint con
                JOIN pg_catalog.pg_class c ON c.oid = con.conrelid
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname = %s
                  AND c.relname = %s
                  AND con.contype IN ('p', 'u', 'c', 'x')
                ORDER BY con.conname
            """, (schema_name, relname))
            kind_map = {"p": "PRIMARY KEY", "u": "UNIQUE", "c": "CHECK", "x": "EXCLUSION"}
            for con_name, con_type, con_cols in cur.fetchall():
                constraints.append(Constraint(
                    name=con_name,
                    kind=kind_map.get(con_type, con_type),
                    columns=list(con_cols),
                ))
        return constraints

    def read_indexes(self, ref: ConceptRef) -> list[Index]:
        schema_name, relname = ref.id[1], ref.id[2]
        indexes: list[Index] = []
        if ref.kind != "table":
            return indexes
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    i.relname AS index_name,
                    ARRAY(
                        SELECT a.attname
                        FROM pg_catalog.pg_attribute a
                        WHERE a.attrelid = idx.indrelid
                          AND a.attnum = ANY(idx.indkey)
                          AND a.attnum > 0
                        ORDER BY a.attnum
                    ) AS index_cols,
                    idx.indisunique AS is_unique,
                    am.amname AS index_method
                FROM pg_catalog.pg_index idx
                JOIN pg_catalog.pg_class i ON i.oid = idx.indexrelid
                JOIN pg_catalog.pg_class c ON c.oid = idx.indrelid
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                JOIN pg_catalog.pg_am am ON am.oid = i.relam
                WHERE n.nspname = %s
                  AND c.relname = %s
                  AND NOT idx.indisprimary
                ORDER BY i.relname
            """, (schema_name, relname))
            for index_name, index_cols, is_unique, index_method in cur.fetchall():
                indexes.append(Index(
                    name=index_name,
                    columns=list(index_cols),
                    unique=is_unique,
                    method=index_method,
                ))
        return indexes

    def read_foreign_keys(self) -> list[ForeignKey]:
        fks: list[ForeignKey] = []
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT
                    con.conname AS fk_name,
                    ns_src.nspname AS src_schema,
                    c_src.relname AS src_table,
                    ARRAY(
                        SELECT a.attname
                        FROM pg_catalog.pg_attribute a
                        WHERE a.attrelid = con.conrelid
                          AND a.attnum = ANY(con.conkey)
                        ORDER BY a.attnum
                    ) AS src_cols,
                    ns_tgt.nspname AS tgt_schema,
                    c_tgt.relname AS tgt_table,
                    ARRAY(
                        SELECT a.attname
                        FROM pg_catalog.pg_attribute a
                        WHERE a.attrelid = con.confrelid
                          AND a.attnum = ANY(con.confkey)
                        ORDER BY a.attnum
                    ) AS tgt_cols
                FROM pg_catalog.pg_constraint con
                JOIN pg_catalog.pg_class c_src ON c_src.oid = con.conrelid
                JOIN pg_catalog.pg_namespace ns_src ON ns_src.oid = c_src.relnamespace
                JOIN pg_catalog.pg_class c_tgt ON c_tgt.oid = con.confrelid
                JOIN pg_catalog.pg_namespace ns_tgt ON ns_tgt.oid = c_tgt.relnamespace
                WHERE con.contype = 'f'
                  AND pg_catalog.pg_table_is_visible(c_src.oid)
                ORDER BY con.conname
            """)
            for fk_name, src_schema, src_table, src_cols, tgt_schema, tgt_table, tgt_cols in cur.fetchall():
                fks.append(ForeignKey(
                    name=fk_name,
                    source_table=f"{src_schema}.{src_table}",
                    source_columns=list(src_cols),
                    target_table=f"{tgt_schema}.{tgt_table}",
                    target_columns=list(tgt_cols),
                ))
        return fks


def _parse_postgres_url(url: str) -> dict:
    parsed = urlparse(url)
    dsn = {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "user": parsed.username or "",
        "password": parsed.password or "",
        "dbname": parsed.path.lstrip("/") or "",
    }
    return {k: v for k, v in dsn.items() if v}
