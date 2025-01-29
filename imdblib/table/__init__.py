from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, Iterable

from . import (
    name_basics,
    title_akas,
    title_basics,
    title_crew,
    title_episode,
    title_principals,
    title_ratings,
)

TableName = Literal[
    "name_basics",
    "title_akas",
    "title_basics",
    "title_crew",
    "title_episode",
    "title_principals",
    "title_ratings",
]


modules = {
    "name_basics": name_basics,
    "title_akas": title_akas,
    "title_basics": title_basics,
    "title_crew": title_crew,
    "title_episode": title_episode,
    "title_principals": title_principals,
    "title_ratings": title_ratings,
}

URL = "https://datasets.imdbws.com/{}.tsv.gz"


@dataclass
class Table:
    name: TableName
    docs: str
    create: str
    drop: str
    add_primary_key: str
    add_references: str
    process: Callable[[list[str]], list[str]]

    @classmethod
    def all(cls) -> list[Table]:
        return [cls.from_name(name) for name in modules.keys()]  # type: ignore

    @classmethod
    def from_name(cls, name: TableName) -> Table:
        module = modules[name]

        return cls(
            name,
            module.docs,
            module.create,
            module.drop,
            module.add_primary_key,
            module.add_references,
            module.process,
        )

    @property
    def url(self):
        return URL.format(self.name.replace("_", "."))

    def fetch(self, *, quiet: bool = False) -> Iterable[str]:
        import subprocess

        if quiet:
            command = f"wget -O - -q '{self.url}' | gzip -d"
        else:
            command = f"wget -O - '{self.url}' | gzip -d"

        with subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            text=True,
        ) as process:
            assert process.stdout is not None
            yield from process.stdout

    def process_line(self, line: str):
        return "\t".join(self.process(line.rstrip("\n").split("\t"))) + "\n"

    def fetch_processed(self) -> Iterable[str]:
        from itertools import islice

        for line in islice(self.fetch(), 1, None):  # skip header
            yield self.process_line(line)
