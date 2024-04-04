from imdb import parse

name = "title_akas"

docs = r"""
title.akas.tsv.gz

titleId (string) - a tconst, an alphanumeric unique identifier of the title
ordering (integer) – a number to uniquely identify rows for a given titleId
title (string) – the localized title
region (string) - the region for this version of the title
language (string) - the language of the title
types (array) - Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
attributes (array) - Additional terms to describe this alternative title, not enumerated
isOriginalTitle (boolean) – 0: not original title; 1: original title
"""

create = r"""
CREATE TABLE title_akas (
    title_id INTEGER NOT NULL,
    ordering INTEGER NOT NULL,
    title TEXT NOT NULL,
    region VARCHAR (4) DEFAULT NULL,
    language VARCHAR (3) DEFAULT NULL,
    types TEXT [] DEFAULT NULL,
    attributes TEXT [] DEFAULT NULL,
    is_original_title BOOLEAN NOT NULL
);
"""

add_primary_key = r"""
ALTER TABLE title_akas ADD PRIMARY KEY (title_id, ordering);
"""

add_references = r"""
ALTER TABLE title_akas ADD CONSTRAINT fk_title_akas_title_id
    FOREIGN KEY (title_id)
    REFERENCES title_basics (title_id);
"""


def process(line: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(line[0]), # title_id INTEGER NOT NULL
        line[1],  # ordering INTEGER NOT NULL,
        line[2],  # title TEXT NOT NULL,
        parse.text_nullable(line[3]),  # region VARCHAR (4) DEFAULT NULL,
        parse.text_nullable(line[4]),  # language VARCHAR (3) DEFAULT NULL,
        parse.list_nullable(line[5]),  # types TEXT [] DEFAULT NULL,
        parse.list_nullable(line[6]),  # attributes TEXT [] DEFAULT NULL,
        line[7],  # is_original_title BOOLEAN NOT NULL,
    ]
    # fmt: on
