from imdblib import parse

docs = r"""
title.ratings.tsv.gz

tconst (string) - alphanumeric unique identifier of the title
averageRating – weighted average of all the individual user ratings
numVotes - number of votes the title has received
"""

create = r"""
CREATE TABLE title_ratings (
    -- unique identifier of the title
    tconst INTEGER NOT NULL,
    -- weighted average of all the individual user ratings
    average_rating NUMERIC NOT NULL,
    -- number of votes the title has received
    num_votes INTEGER NOT NULL
);
"""

drop = r"""
DROP TABLE IF EXISTS title_ratings;
"""

add_primary_key = r"""
ALTER TABLE title_ratings ADD PRIMARY KEY (tconst);
"""

add_references = r"""
ALTER TABLE title_ratings ADD CONSTRAINT fk_title_ratings_tconst FOREIGN KEY (tconst) REFERENCES title_basics (tconst);
"""


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]),
        row[1],
        row[2],
    ]
    # fmt: on
