from dataclasses import dataclass, field
from typing import Optional
import yaml


REQUIRED_FRONTMATTER_FIELDS = ["type", "title", "timestamp"]


class ValidationError(Exception):
    pass


@dataclass
class OKFDocument:
    frontmatter: dict = field(default_factory=dict)
    body: str = ""

    def serialize(self) -> str:
        header = yaml.dump(self.frontmatter, default_flow_style=False, allow_unicode=True).strip()
        return f"---\n{header}\n---\n\n{self.body.strip()}\n"

    @classmethod
    def parse(cls, text: str) -> "OKFDocument":
        text = text.strip()
        if not text.startswith("---"):
            raise ValidationError("Missing frontmatter delimiters")
        _, raw_fm, rest = text.split("---", 2)
        frontmatter = yaml.safe_load(raw_fm) or {}
        body = rest.strip()
        return cls(frontmatter=frontmatter, body=body)

    def validate(self) -> None:
        for field_name in REQUIRED_FRONTMATTER_FIELDS:
            if field_name not in self.frontmatter:
                raise ValidationError(f"Missing required frontmatter field: {field_name}")
