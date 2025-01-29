import os
import sys
from signal import SIG_DFL, SIGPIPE, signal

from imdblib.psql import Psql

psql = Psql(
    username=os.environ.get("POSTGRES_USER", "admin"),
    password=os.environ.get("POSTGRES_PASSWORD", "password"),
    dbname="imdb",
    host="127.0.0.1",
    port=5432,
)


def main(argv: list[str]):
    match argv:
        case ["help"]:
            print(
                r"""
            imdb <table_name> upload
                $ ./imdb title_basics upload
            imdb <table_name> upload --file <file>
                $ ./imdb title_basics upload --file ./title.basics.tsv.gz
            imdb <table_name> upload --stdin
                $ pv ./title.basics.tsv.gz | gzip -d | ./imdb title_basics upload --stdin
                $ wget -O - "https://datasets.imdbws.com/title.basics.tsv.gz" | gzip -d | ./imdb title_basics upload --stdin
            """
            )

        case ["db", "create"]:
            psql.createdb()

        case ["db", "drop"]:
            psql.dropdb()

        case ["all"]:
            # try:
            #     psql.createdb()
            # except:
            #     print("Database already exists")

            tables = psql.all_tables()

            print()
            print("Will download tables:")
            for table in tables:
                print("-", table.table.name)
            print()

            for i, table in enumerate(tables):
                main([table.table.name, "all"])
                print(f"Done downloading {i + 1}/{len(tables)}")

            # I got error 'Key (tconst)=(35557166) is not present in table "title_basics".'
            # possibly because this is a new show (checked on imdb site),
            # and maybe was inserted during the upload process.
            # since references prob won't help with speed in queries anyway, skip it

            # print("Adding references")
            # for table in psql.all_tables():
            #     table.add_references()

        case ["all", "list"]:
            for table in psql.all_tables():
                print(table.table.name)

        case ["all", command, *rest]:
            for table in psql.all_tables():
                main([table.table.name, command, *rest])

        case [table_name, command, *rest]:
            table = psql.table(name=table_name)  # type: ignore

            match command:
                case "url":
                    print(table.table.url)

                case "all":
                    table.create()
                    table.upload()
                    table.add_primary_key()

                case "create":
                    table.create()

                case "drop":
                    table.drop()

                case "add_primary_key":
                    table.add_primary_key()

                case "add_references":
                    table.add_references()

                case "process":
                    for line in sys.stdin:
                        sys.stdout.write(table.table.process_line(line))
                        sys.stdout.flush()

                case "fetch":
                    table = psql.table(name=table_name)  # type: ignore
                    lines = iter(table.fetch(quiet="--quiet" in rest))

                    if "--headers" in rest and "--processed" in rest:
                        next(lines)
                        sys.stdout.write(
                            "\t".join(table.table.name for table in psql.all_tables())
                            + "\n"
                        )
                        sys.stdout.flush()
                    elif "--headers" in rest:
                        sys.stdout.write(next(lines))
                        sys.stdout.flush()
                    else:
                        next(lines)

                    for line in lines:
                        if "--processed" in rest:
                            sys.stdout.write(table.table.process_line(line))
                        else:
                            sys.stdout.write(line)

                        sys.stdout.flush()

                case "upload" if "--fetch" in rest:
                    table.upload()  # type: ignore

                case "upload" if "--file" in rest:
                    table.upload(file=rest[rest.index("--file") + 1])

                case "upload":
                    table.upload(stdin=True)

                case _:
                    main(["help"])

        case _:
            main(["help"])


signal(SIGPIPE, SIG_DFL)
main(sys.argv[1:])
