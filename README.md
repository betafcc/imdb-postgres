imdb-postgres
-------------

Docker image that downloads the [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/) and serves on postgres

Usage
-----


### Run the container

```sh
docker run \
  --name imdb \
  -p 5432:5432 \
  -v imdb_data:/var/lib/postgresql/data \
  betafcc/imdb-postgres:latest
```

This will download all the data and mount it to a volume `imdb_data` so that it persists across container restarts.

The total size is around 20GB.

To delete the volume, use `docker volume rm imdb_data`.

### Connect to the running container

After the initial setup you can connect to the database using your favorite client.

User is 'imdb' and db is 'imdb', no password is needed.

Using the connection url `postgresql://imdb@localhost:5432/imdb`


Table documentation
-------------------

```sql
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

--

CREATE TABLE title_akas (
    -- a tconst, an unique identifier of the title
    title_id INTEGER NOT NULL,
    -- a number to uniquely identify rows for a given titleId
    ordering INTEGER NOT NULL,
    -- the localized title
    title TEXT NOT NULL,
    -- the region for this version of the title
    region VARCHAR (4) DEFAULT NULL,
    -- the language of the title
    language VARCHAR (3) DEFAULT NULL,
    -- Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
    types TEXT [] DEFAULT NULL,
    -- Additional terms to describe this alternative title, not enumerated
    attributes TEXT [] DEFAULT NULL,
    -- false: not original title; true: original title
    is_original_title BOOLEAN NOT NULL
);

--

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
    -- unique identifier of the title
    tconst INTEGER NOT NULL,
    -- the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
    title_type TITLE_TYPE NOT NULL,
    -- the more popular title / the title used by the filmmakers on promotional materials at the point of release
    primary_title TEXT NOT NULL,
    -- original title, in the original language
    original_title TEXT NOT NULL,
    -- false: non-adult title; true: adult title
    is_adult BOOLEAN NOT NULL,
    -- represents the release year of a title. In the case of TV Series, it is the series start year
    start_year INTEGER DEFAULT NULL,
    -- TV Series end year. '\N' for all other title types
    end_year INTEGER DEFAULT NULL,
    -- primary runtime of the title, in minutes
    runtime_minutes INTEGER DEFAULT NULL,
    -- includes up to three genres associated with the title
    genres GENRE [] DEFAULT NULL
);

--

CREATE TABLE title_crew (
    -- unique identifier of the title
    tconst INTEGER NOT NULL,
    -- director(s) of the given title
    directors INTEGER [] DEFAULT NULL,
    -- writer(s) of the given title
    writers INTEGER [] DEFAULT NULL
);

--

CREATE TABLE title_episode (
    -- identifier of episode
    tconst INTEGER NOT NULL,
    -- alphanumeric identifier of the parent TV Series
    parent_tconst INTEGER NOT NULL,
    -- season number the episode belongs to
    season_number INTEGER DEFAULT NULL,
    -- episode number of the tconst in the TV series
    episode_number INTEGER DEFAULT NULL
);

--

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
    -- unique identifier of the title
    tconst INTEGER NOT NULL,
    -- a number to uniquely identify rows for a given titleId
    ordering INTEGER NOT NULL,
    -- alphanumeric unique identifier of the name/person
    nconst INTEGER NOT NULL,
    -- the category of job that person was in
    category CATEGORY NOT NULL,
    -- the specific job title if applicable, else NULL
    job TEXT DEFAULT NULL,
    -- the name of the character played if applicable, else NULL
    characters TEXT DEFAULT NULL
);

--

CREATE TABLE title_ratings (
    -- unique identifier of the title
    tconst INTEGER NOT NULL,
    -- weighted average of all the individual user ratings
    average_rating NUMERIC NOT NULL,
    -- number of votes the title has received
    num_votes INTEGER NOT NULL
);
```