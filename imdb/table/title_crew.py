from imdb import parse

name = "title_crew"

docs = r"""
title.crew.tsv.gz

tconst (string) - alphanumeric unique identifier of the title
directors (array of nconsts) - director(s) of the given title
writers (array of nconsts) – writer(s) of the given title
"""

create = r"""
CREATE TABLE title_crew (
    tconst INTEGER NOT NULL,
    directors INTEGER [] DEFAULT NULL,
    writers INTEGER [] DEFAULT NULL
);
"""

add_primary_key = r"""
ALTER TABLE title_crew ADD PRIMARY KEY (tconst);
"""

add_references = r"""
ALTER TABLE title_crew ADD CONSTRAINT fk_title_crew_tconst FOREIGN KEY (tconst) REFERENCES title_basics (tconst);
"""


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]),  # tconst INTEGER PRIMARY KEY,
        parse.id_list_nullable(row[1]),  # directors INTEGER [],
        parse.id_list_nullable(row[2]),  # writers INTEGER [],
    ]
    # fmt: on
