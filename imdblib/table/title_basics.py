from imdblib import parse

docs = r"""
title.basics.tsv.gz

tconst (string) - alphanumeric unique identifier of the title
titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
originalTitle (string) - original title, in the original language
isAdult (boolean) - 0: non-adult title; 1: adult title
startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
endYear (YYYY) – TV Series end year. ‘\N’ for all other title types
runtimeMinutes – primary runtime of the title, in minutes
genres (string array) – includes up to three genres associated with the title
"""

create = r"""
-- cat ./data/raw/title.basics.tsv.gz | gzip -d | cut -f 2 -d $'\t' | tail +2 | uniq | sort | uniq
CREATE TYPE TITLE_TYPE AS ENUM (
    'movie',
    'short',
    'tvEpisode',
    'tvMiniSeries',
    'tvMovie',
    'tvPilot',
    'tvSeries',
    'tvShort',
    'tvSpecial',
    'video',
    'videoGame'
);
-- cat ./data/raw/title.basics.tsv.gz | gzip -d | tail +2 | cut -f9 -d$'\t' | tr ',' '\n' | uniq | sort | uniq
CREATE TYPE GENRE AS ENUM (
    'Action',
    'Adult',
    'Adventure',
    'Animation',
    'Biography',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Family',
    'Fantasy',
    'Film-Noir',
    'Game-Show',
    'History',
    'Horror',
    'Music',
    'Musical',
    'Mystery',
    'News',
    'Reality-TV',
    'Romance',
    'Sci-Fi',
    'Short',
    'Sport',
    'Talk-Show',
    'Thriller',
    'War',
    'Western'
);
CREATE TABLE title_basics (
    tconst INTEGER NOT NULL,
    title_type TITLE_TYPE NOT NULL,
    primary_title TEXT NOT NULL,
    original_title TEXT NOT NULL,
    is_adult BOOLEAN NOT NULL,
    start_year INTEGER DEFAULT NULL,
    end_year INTEGER DEFAULT NULL,
    runtime_minutes INTEGER DEFAULT NULL,
    genres GENRE [] DEFAULT NULL
);
"""

drop = r"""
DROP TABLE IF EXISTS title_basics;
DROP TYPE IF EXISTS TITLE_TYPE;
DROP TYPE IF EXISTS GENRE;
"""


add_primary_key = r"""
ALTER TABLE title_basics ADD PRIMARY KEY (tconst);
"""

add_references = ""


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]), # tconst INTEGER PRIMARY KEY,
        row[1], # title_type TITLE_TYPE NOT NULL,
        parse.text(row[2]), # primary_title TEXT NOT NULL,
        parse.text(row[3]), # original_title TEXT NOT NULL,
        row[4], # is_adult BOOLEAN NOT NULL,
        parse.int_nullable(row[5]), # start_year INTEGER DEFAULT NULL,
        parse.int_nullable(row[6]), # end_year INTEGER DEFAULT NULL,
        parse.int_nullable(row[7]), # runtime_minutes INTEGER DEFAULT NULL,
        parse.list_nullable(row[8]), # genres GENRE [] DEFAULT NULL
    ]
    # fmt: on
