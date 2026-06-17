import re
from typing import Optional


_SEGMENT_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_\-.]*$")
_SPLIT_RE = re.compile(r"[/\\]")


def concept_id_to_path(concept_id: tuple[str, ...]) -> str:
    return "/".join(concept_id) + ".md"


def path_to_concept_id(path: str) -> tuple[str, ...]:
    path = path.removesuffix(".md")
    return tuple(_SPLIT_RE.split(path))


def parse_concept_id(raw: str) -> Optional[tuple[str, ...]]:
    segments = _SPLIT_RE.split(raw)
    for seg in segments:
        if not _SEGMENT_RE.match(seg):
            return None
    return tuple(segments)
