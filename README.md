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


Example queries
---------------

#### 1. Top 10 highest-rated movies (with at least 10,000 votes)

```sql
SELECT b.primary_title,
       r.average_rating,
       r.num_votes
FROM title_basics AS b
JOIN title_ratings AS r ON b.tconst = r.tconst
WHERE b.title_type = 'movie'
  AND r.num_votes >= 10000
ORDER BY r.average_rating DESC
LIMIT 10;
```

| primary_title                                 | average_rating | num_votes |
| --------------------------------------------- | -------------- | --------- |
| Attack on Titan the Movie: The Last Attack    | 9.3            | 10882     |
| The Shawshank Redemption                      | 9.3            | 2998114   |
| The Godfather                                 | 9.2            | 2092537   |
| Ramayana: The Legend of Prince Rama           | 9.2            | 16081     |
| The Chaos Class                               | 9.2            | 44019     |
| 12 Angry Men                                  | 9.0            | 907900    |
| The Lord of the Rings: The Return of the King | 9.0            | 2051541   |
| The Godfather Part II                         | 9.0            | 1410759   |
| The Silence of Swastika                       | 9.0            | 10601     |
| Schindler's List                              | 9.0            | 1502465   |

#### 2. Most prolific actors/actresses (by number of credited titles)

```sql
SELECT n.primary_name AS name,
       COUNT(*)       AS title_count
FROM title_principals AS p
JOIN name_basics      AS n ON p.nconst = n.nconst
WHERE p.category IN ('actor', 'actress')
GROUP BY n.nconst, n.primary_name
ORDER BY title_count DESC
LIMIT 10;
```

| name              | title_count |
| ----------------- | ----------- |
| Kenjirô Ishimaru  | 10982       |
| Vic Sotto         | 10659       |
| Tito Sotto        | 9999        |
| Sameera Sherief   | 9905        |
| Dee Bradley Baker | 9355        |
| Delhi Kumar       | 8634        |
| David Kaye        | 8205        |
| Manuela do Monte  | 8163        |
| Arnold Clavio     | 8027        |
| Pia Arcangel      | 8025        |


#### 3. Most common genres in the dataset

```sql
SELECT unnest(genres) AS genre,
       COUNT(*)       AS count
FROM title_basics
WHERE genres IS NOT NULL
GROUP BY unnest(genres)
ORDER BY count DESC;
```

| genre       | count   |
| ----------- | ------- |
| Drama       | 3216838 |
| Comedy      | 2228311 |
| Talk-Show   | 1411121 |
| Short       | 1221605 |
| Documentary | 1089506 |
| News        | 1073869 |
| Romance     | 1064419 |
| Family      | 843980  |
| Reality-TV  | 637962  |
| Animation   | 568493  |
| Action      | 472887  |
| Crime       | 472720  |
| Adventure   | 435285  |
| Game-Show   | 432265  |
| Music       | 425407  |
| Adult       | 364373  |
| Sport       | 284124  |
| Fantasy     | 241510  |
| Mystery     | 232211  |
| Horror      | 217486  |
| Thriller    | 189022  |
| History     | 169734  |
| Biography   | 122530  |
| Sci-Fi      | 118513  |
| Musical     | 93299   |
| War         | 39226   |
| Western     | 31127   |
| Film-Noir   | 868     |

#### 4. Top-rated TV Series episodes (with at least 1000 votes)

```sql
SELECT b.primary_title AS episode_title,
       parent_b.primary_title AS series_title,
       r.average_rating,
       r.num_votes
FROM title_basics AS b
JOIN title_episode  AS e ON b.tconst = e.tconst
JOIN title_basics  AS parent_b ON e.parent_tconst = parent_b.tconst
JOIN title_ratings AS r ON b.tconst = r.tconst
WHERE b.title_type = 'tvEpisode'
  AND r.num_votes >= 1000
ORDER BY r.average_rating DESC
LIMIT 10;
```

| episode_title                  | series_title                  | average_rating | num_votes |
| ------------------------------ | ----------------------------- | -------------- | --------- |
| Ozymandias                     | Breaking Bad                  | 10.0           | 237629    |
| Felina                         | Breaking Bad                  | 9.9            | 152114    |
| The View from Halfway Down     | BoJack Horseman               | 9.9            | 24196     |
| Dream: To See It to the End    | Legend of the Galactic Heroes | 9.9            | 1538      |
| The Magician Doesn't Come Back | Legend of the Galactic Heroes | 9.9            | 1720      |
| 13. Bolum                      | Gönülçelen                    | 9.9            | 1308      |
| Connor's Wedding               | Succession                    | 9.9            | 38817     |
| Somewhere in the Woods         | Gravity Falls                 | 9.9            | 3380      |
| Battle of the Bastards         | Game of Thrones               | 9.9            | 235736    |
| Episode #1.19                  | Asi                           | 9.9            | 1095      |

#### 5. Average runtime per genre (movies only)

```sql
SELECT unnest(genres) AS genre,
       AVG(runtime_minutes)::INT AS avg_runtime
FROM title_basics
WHERE title_type = 'movie'
  AND runtime_minutes IS NOT NULL
  AND genres IS NOT NULL
GROUP BY unnest(genres)
ORDER BY avg_runtime DESC;
```

| genre       | avg_runtime |
| ----------- | ----------- |
| Action      | 101         |
| Romance     | 99          |
| Musical     | 99          |
| Drama       | 96          |
| Thriller    | 96          |
| Crime       | 95          |
| War         | 95          |
| History     | 94          |
| Mystery     | 94          |
| Adventure   | 93          |
| Fantasy     | 93          |
| Comedy      | 93          |
| Family      | 92          |
| Sci-Fi      | 91          |
| Animation   | 90          |
| Sport       | 89          |
| Biography   | 89          |
| Music       | 88          |
| Horror      | 88          |
| Talk-Show   | 86          |
| Reality-TV  | 85          |
| Film-Noir   | 82          |
| Adult       | 79          |
| Documentary | 78          |
| Western     | 76          |
| News        | 75          |
| Game-Show   | 67          |


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