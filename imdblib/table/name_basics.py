from imdblib import parse

docs = r"""
name.basics.tsv.gz

nconst (string) - alphanumeric unique identifier of the name/person
primaryName (string)– name by which the person is most often credited
birthYear – in YYYY format
deathYear – in YYYY format if applicable, else '\N'
primaryProfession (array of strings)– the top-3 professions of the person
knownForTitles (array of tconsts) – titles the person is known for
"""

create = r"""
CREATE TABLE name_basics (
    -- unique identifier of the name/person
    nconst INTEGER NOT NULL,
    -- name by which the person is most often credited
    primary_name TEXT,
    -- in YYYY format
    birth_year INTEGER,
    -- in YYYY format if applicable, else NULL
    death_year INTEGER,
    -- the top-3 professions of the person
    primary_profession TEXT [],
    -- titles the person is known for
    known_for_titles INTEGER []
);
"""


drop = r"""
DROP TABLE IF EXISTS name_basics;
"""

add_primary_key = r"""
ALTER TABLE name_basics ADD PRIMARY KEY (nconst);
"""

add_references = ""


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]),
        parse.text(row[1]),
        parse.int_nullable(row[2]),
        parse.int_nullable(row[3]),
        parse.list_nullable(row[4]),
        parse.id_list_nullable(row[5]),
    ]
    # fmt: on
