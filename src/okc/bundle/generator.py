import os
from datetime import datetime, timezone

from okc.bundle.document import OKFDocument
from okc.bundle.index import regenerate_indexes
from okc.bundle.paths import concept_id_to_path
from typing import Optional

from okc.sources.base import Source, ForeignKey


def generate_bundle(source: Source, out_dir: str) -> None:
    concepts = source.list_concepts()
    concepts.sort(key=lambda c: c.id)

    all_fks = source.read_foreign_keys()

    outgoing: dict[tuple[str, ...], list[ForeignKey]] = {}
    incoming: dict[tuple[str, ...], list[ForeignKey]] = {}

    for fk in all_fks:
        src_id = _parse_fk_table_ref(fk.source_table, concepts)
        tgt_id = _parse_fk_table_ref(fk.target_table, concepts)
        if src_id:
            outgoing.setdefault(src_id, []).append(fk)
        if tgt_id:
            incoming.setdefault(tgt_id, []).append(fk)

    for ref in concepts:
        title = ref.id[-1]
        description = _build_description(source, ref)
        tags = [ref.schema or "default", ref.kind]

        frontmatter = {
            "type": ref.type,
            "title": title,
            "description": description,
            "resource": getattr(source, "_url", ""),
            "tags": tags,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        body_parts: list[str] = []

        schema_info = source.read_schema(ref)
        if schema_info.columns:
            body_parts.append("## Schema\n")
            body_parts.append("| Name | Type | Nullable | Default | Description |")
            body_parts.append("|------|------|----------|---------|-------------|")
            for col in schema_info.columns:
                desc = col.comment or ""
                body_parts.append(f"| {col.name} | {col.data_type} | {'YES' if col.nullable else 'NO'} | {col.default or ''} | {desc} |")
            body_parts.append("")

        if ref.kind == "table":
            constraints = source.read_constraints(ref)
            if constraints:
                body_parts.append("## Constraints\n")
                for c in constraints:
                    cols = ", ".join(c.columns)
                    body_parts.append(f"- **{c.kind}**: {c.name} ({cols})")
                body_parts.append("")

            indexes = source.read_indexes(ref)
            if indexes:
                body_parts.append("## Indexes\n")
                body_parts.append("| Name | Columns | Unique | Method |")
                body_parts.append("|------|---------|--------|--------|")
                for idx in indexes:
                    cols = ", ".join(idx.columns)
                    body_parts.append(f"| {idx.name} | {cols} | {'YES' if idx.unique else 'NO'} | {idx.method} |")
                body_parts.append("")

        src_fks = outgoing.get(ref.id, [])
        if src_fks:
            body_parts.append("## Relationships\n")
            for fk in src_fks:
                tgt_id = _parse_fk_table_ref(fk.target_table, concepts)
                if tgt_id:
                    tgt_path = concept_id_to_path(tgt_id)
                    src_cols = ", ".join(fk.source_columns)
                    tgt_cols = ", ".join(fk.target_columns)
                    body_parts.append(f"- {src_cols} → [{fk.target_table}](/{tgt_path}) ({tgt_cols})")
            body_parts.append("")

        tgt_fks = incoming.get(ref.id, [])
        if tgt_fks:
            body_parts.append("## Referenced by\n")
            for fk in tgt_fks:
                src_id = _parse_fk_table_ref(fk.source_table, concepts)
                if src_id:
                    src_path = concept_id_to_path(src_id)
                    src_cols = ", ".join(fk.source_columns)
                    body_parts.append(f"- [{fk.source_table}](/{src_path}) via {src_cols}")
            body_parts.append("")

        doc = OKFDocument(frontmatter=frontmatter, body="\n".join(body_parts))

        rel_path = concept_id_to_path(ref.id)
        full_path = os.path.join(out_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(doc.serialize())

    regenerate_indexes(out_dir)


def _build_description(source: Source, ref) -> str:
    if ref.comment:
        return ref.comment
    schema_info = source.read_schema(ref)
    col_count = len(schema_info.columns)
    return f"{ref.kind.title()} with {col_count} column{'s' if col_count != 1 else ''}"


def _parse_fk_table_ref(table_ref: str, concepts: list) -> Optional[tuple[str, ...]]:
    for c in concepts:
        if c.id[-1] == table_ref or ".".join(c.id[1:]) == table_ref:
            return c.id
    parts = table_ref.replace(".", "/").split("/")
    for i in range(len(parts)):
        candidate = tuple(parts[i:])
        for c in concepts:
            if c.id[-len(candidate):] == candidate:
                return c.id
    return None
