from imdb import parse

name = "title_principals"

docs = r"""
title.principals.tsv.gz

tconst (string) - alphanumeric unique identifier of the title
ordering (integer) – a number to uniquely identify rows for a given titleId
nconst (string) - alphanumeric unique identifier of the name/person
category (string) - the category of job that person was in
job (string) - the specific job title if applicable, else '\N'
characters (string) - the name of the character played if applicable, else '\N'
"""

create = r"""
-- cat ./data/raw/title.principals.tsv.gz | gzip -d | tail +2 | cut -f4 -d$'\t' | sort | uniq -c | sort -n -r
CREATE TYPE CATEGORY AS ENUM (
    'actor',
    'actress',
    'self',
    'writer',
    'director',
    'producer',
    'editor',
    'cinematographer',
    'composer',
    'production_designer',
    'casting_director',
    'archive_footage',
    'archive_sound'
);
CREATE TABLE title_principals (
    tconst INTEGER NOT NULL,
    ordering INTEGER NOT NULL,
    nconst INTEGER NOT NULL,
    category CATEGORY NOT NULL,
    job TEXT DEFAULT NULL,
    characters TEXT [] DEFAULT NULL
);
"""

add_primary_key = r"""
ALTER TABLE title_principals ADD PRIMARY KEY (tconst, ordering);
"""

add_references = r"""
ALTER TABLE title_principals ADD CONSTRAINT fk_title_principals_tconst FOREIGN KEY (tconst) REFERENCES title_basics (tconst);
ALTER TABLE title_principals ADD CONSTRAINT fk_title_principals_nconst FOREIGN KEY (nconst) REFERENCES name_basics (nconst);
"""


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]),  # tconst INTEGER NOT NULL,
        row[1],  # ordering INTEGER NOT NULL,
        parse.id(row[2]),  # nconst INTEGER NOT NULL,
        row[3],  # category CATEGORY NOT NULL,
        parse.text_nullable(row[4]),  # job TEXT DEFAULT NULL,
        parse.characters(row[5]),  # characters TEXT [] DEFAULT NULL
    ]
    # fmt: on
