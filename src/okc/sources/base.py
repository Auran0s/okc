from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConceptRef:
    id: tuple[str, ...]
    type: str
    kind: str
    schema: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool = True
    default: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class SchemaInfo:
    columns: list[ColumnInfo] = field(default_factory=list)


@dataclass
class Constraint:
    name: str
    kind: str
    columns: list[str] = field(default_factory=list)


@dataclass
class Index:
    name: str
    columns: list[str] = field(default_factory=list)
    unique: bool = False
    method: str = "btree"


@dataclass
class ForeignKey:
    name: str
    source_table: str
    source_columns: list[str]
    target_table: str
    target_columns: list[str]


class Source(ABC):

    @abstractmethod
    def list_concepts(self) -> list[ConceptRef]:
        ...

    @abstractmethod
    def read_schema(self, ref: ConceptRef) -> SchemaInfo:
        ...

    @abstractmethod
    def read_constraints(self, ref: ConceptRef) -> list[Constraint]:
        ...

    @abstractmethod
    def read_indexes(self, ref: ConceptRef) -> list[Index]:
        ...

    @abstractmethod
    def read_foreign_keys(self) -> list[ForeignKey]:
        ...
