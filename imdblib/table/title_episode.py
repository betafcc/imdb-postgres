from imdblib import parse

docs = r"""
title.episode.tsv.gz

tconst (string) - alphanumeric identifier of episode
parentTconst (string) - alphanumeric identifier of the parent TV Series
seasonNumber (integer) – season number the episode belongs to
episodeNumber (integer) – episode number of the tconst in the TV series
"""

create = r"""
CREATE TABLE title_episode (
    tconst INTEGER NOT NULL,
    parent_tconst INTEGER NOT NULL,
    season_number INTEGER DEFAULT NULL,
    episode_number INTEGER DEFAULT NULL
);
"""

drop = r"""
DROP TABLE IF EXISTS title_episode;
"""

add_primary_key = r"""
ALTER TABLE title_episode ADD PRIMARY KEY (tconst);
"""

add_references = r"""
ALTER TABLE title_episode ADD CONSTRAINT fk_title_episode_tconst FOREIGN KEY (parent_tconst) REFERENCES title_basics (tconst);
"""


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]),
        parse.id(row[1]),
        parse.int_nullable(row[2]),
        parse.int_nullable(row[3]),
    ]
    # fmt: on
