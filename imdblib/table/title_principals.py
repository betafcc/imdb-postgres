from imdblib import parse

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
    characters TEXT DEFAULT NULL
);
"""
#    characters TEXT [] DEFAULT NULL

drop = r"""
DROP TABLE IF EXISTS title_principals;
DROP TYPE IF EXISTS CATEGORY;
"""

# add_primary_key = r"""
# ALTER TABLE title_principals ADD COLUMN characters_temp TEXT[];

# UPDATE title_principals
# SET characters_temp = 
#   CASE 
#     WHEN characters IS NOT NULL THEN array(
#       SELECT json_array_elements_text(characters::json)
#     )
#     ELSE NULL
#   END;

# ALTER TABLE title_principals DROP COLUMN characters;
# ALTER TABLE title_principals RENAME COLUMN characters_temp TO characters;

# ALTER TABLE title_principals ADD PRIMARY KEY (tconst, ordering);
# """


add_primary_key = r"""
CREATE TABLE title_principals_new AS
SELECT
    tconst,
    ordering,
    nconst,
    category,
    job,
  CASE
    WHEN characters IS NOT NULL THEN array(
      SELECT json_array_elements_text(characters::json)
    )
    ELSE NULL
  END AS characters
FROM title_principals;

BEGIN;

ALTER TABLE title_principals RENAME TO title_principals_old;
ALTER TABLE title_principals_new RENAME TO title_principals;

COMMIT;

DROP TABLE title_principals_old;

ALTER TABLE title_principals ADD PRIMARY KEY (tconst, ordering);
"""

add_references = r"""
ALTER TABLE title_principals ADD CONSTRAINT fk_title_principals_tconst FOREIGN KEY (tconst) REFERENCES title_basics (tconst);
ALTER TABLE title_principals ADD CONSTRAINT fk_title_principals_nconst FOREIGN KEY (nconst) REFERENCES name_basics (nconst);
"""


# def parse_characters(cell: str):
#     r"""
#     characters table is too hard to serialize, it contains a JSON array string
#     and some contain quote and comma on it, idk how to escape for postgres tsv

#     solution: https://briandfoy.github.io/importing-array-values-into-postgres-from-csv/

#     """
#     if cell == "\\N":
#         return ""

#     return cell.replace('"', '""')

# import json

# try:
#     arr = json.loads(cell)
# except Exception as _:
#     raise Exception(f"json failed loading: '{cell}'")

# formatted_elements: list[str] = []
# for element in arr:
#     # Escape double quotes and wrap the element in double quotes
#     formatted_element = '"""' + element + '"""'
#     formatted_elements.append(formatted_element)

# # Join the formatted elements into a PostgreSQL array string
# formatted_cell = '"{' + ",".join(formatted_elements) + '}"'

# return formatted_cell


# import json

# def format_json(cell: str) -> str:
#     r"""
#     Correctly formats a JSON array string for psql \copy command from a TSV source.
#     The function ensures that the JSON array is escaped and quoted correctly.

#     Args:
#     cell (str): A string that represents a JSON array, e.g., '["hello", "world"]'.

#     Returns:
#     str: A formatted JSON string ready for psql \copy.
#     """

#     if cell == "\\N":
#         return ""

#     return "{{}}".format(cell[1:-1].replace('"', '\\""'))

# # Convert the string back to a JSON object to remove any unwanted string escaping
# # and ensure it's a valid JSON.
# json_obj = json.loads(cell)

# # Convert the JSON object back to a string, ensuring proper JSON formatting.
# json_str = json.dumps(json_obj)

# # Escape double quotes for PostgreSQL string syntax.
# escaped_str = json_str.replace('"', '""')

# # Encapsulate in double quotes for CSV/TSV format.
# formatted_cell = f'"{escaped_str}"'

# return formatted_cell


def process(row: list[str]) -> list[str]:
    # fmt: off
    return [
        parse.id(row[0]),  # tconst INTEGER NOT NULL,
        row[1],  # ordering INTEGER NOT NULL,
        parse.id(row[2]),  # nconst INTEGER NOT NULL,
        row[3],  # category CATEGORY NOT NULL,
        parse.text_nullable(row[4]),  # job TEXT DEFAULT NULL,
        parse.text_nullable(row[5]), # characters TEXT DEFAULT NULL
    ]
    # fmt: on
