from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

from . import (
    name_basics,
    title_akas,
    title_basics,
    title_crew,
    title_principals,
    title_ratings,
)

type TableName = Literal[
    "name_basics",
    "title_akas",
    "title_basics",
    "title_crew",
    "title_principals",
    "title_ratings",
]

modules = {
    "name_basics": name_basics,
    "title_akas": title_akas,
    "title_basics": title_basics,
    "title_crew": title_crew,
    "title_principals": title_principals,
    "title_ratings": title_ratings,
}


@dataclass
class Table:
    name: str
    docs: str
    create: str
    add_primary_key: str
    add_references: str
    process: Callable[[list[str]], list[str]]

    @classmethod
    def from_name(cls, name: TableName) -> Table:
        module = modules[name]

        return cls(
            module.name,
            module.docs,
            module.create,
            module.add_primary_key,
            module.add_references,
            module.process,
        )
