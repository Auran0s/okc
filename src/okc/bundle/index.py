import os
from collections import defaultdict

from okc.bundle.document import OKFDocument


def regenerate_indexes(out_dir: str) -> None:
    _regenerate_for_directory(out_dir, out_dir)


def _regenerate_for_directory(dir_path: str, root: str) -> None:
    entries: list[dict] = []
    subdirs: list[str] = []
    for name in sorted(os.listdir(dir_path)):
        full = os.path.join(dir_path, name)
        if os.path.isdir(full):
            if name.startswith("."):
                continue
            subdirs.append(name)
            _regenerate_for_directory(full, root)
        elif name.endswith(".md") and name != "index.md":
            rel = os.path.relpath(full, root)
            with open(full) as f:
                doc = OKFDocument.parse(f.read())
            entries.append({
                "title": doc.frontmatter.get("title", name),
                "path": rel,
                "type": doc.frontmatter.get("type", "Unknown"),
            })

    if not entries and not subdirs:
        return

    body_parts: list[str] = []
    if entries:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for e in entries:
            grouped[e["type"]].append(e)
        for doc_type in sorted(grouped):
            body_parts.append(f"## {doc_type}\n")
            for e in grouped[doc_type]:
                body_parts.append(f"- [{e['title']}](/{e['path']})")
            body_parts.append("")

    if subdirs:
        body_parts.append("## Subdirectories\n")
        for sd in subdirs:
            rel = os.path.relpath(os.path.join(dir_path, sd), root)
            body_parts.append(f"- [{sd}/](/{rel}/)")

    dir_name = os.path.basename(dir_path) if dir_path != root else "Bundle Index"
    doc = OKFDocument(
        frontmatter={"type": "Index", "title": dir_name},
        body="\n".join(body_parts),
    )

    index_path = os.path.join(dir_path, "index.md")
    with open(index_path, "w") as f:
        f.write(doc.serialize())
