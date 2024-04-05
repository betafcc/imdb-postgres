from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Iterable

from imdblib.table import Table, TableName


@dataclass
class Psql:
    username: str
    password: str
    dbname: str
    host: str = "127.0.0.1"
    port: int = 5432

    def table(
        self,
        *,
        table: None | Table = None,
        name: None | TableName = None,
    ) -> PsqlTable:
        if table is None:
            assert name is not None
            table = Table.from_name(name)
        return PsqlTable(psql=self, table=table)

    def all_tables(self):
        return [self.table(table=table) for table in Table.all()]

    def createdb(self):
        return subprocess.run(
            # fmt: off
            [
                "createdb",
                "--username", self.username,
                "--host", self.host,
                "--port", str(self.port),
                self.dbname,
            ],
            # fmt: on
            env={**os.environ, "PGPASSWORD": self.password},
            check=True,
            text=True,
        )

    def command(self, command: str):
        return subprocess.run(
            # fmt: off
            [
                "psql",
                "--username", self.username,
                "--host", self.host,
                "--port", str(self.port),
                "--dbname", self.dbname,
                "--command", command,
            ],
            # fmt: on
            env={**os.environ, "PGPASSWORD": self.password},
            check=True,
            text=True,
        )

    def upload(self, table: str, rows: Iterable[str]):
        with subprocess.Popen(
            # fmt: off
            [
                "psql",
                "--username", self.username,
                "--host", self.host,
                "--port", str(self.port),
                "--dbname", self.dbname,
                "--command", f"\\copy {table} from stdin (FORMAT csv, DELIMITER E'\\t', HEADER false)",
            ],
            # fmt: on
            env={**os.environ, "PGPASSWORD": self.password},
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # bufsize=1,
            text=True,
        ) as process:
            assert process.stdin is not None and process.stderr is not None
            for row in rows:
                r = process.stdin.write(row)
                process.stdin.flush()

                # check if process failed
                if r == 0:
                    process.stdin.close()
                    raise Exception(process.stderr.read())

            process.stdin.close()

            ret = process.wait()
            if ret != 0:
                # raise subprocess.CalledProcessError(
                #     ret, process.args, process.stderr.read()
                # )
                raise Exception(process.stderr.read())


@dataclass
class PsqlTable:
    psql: Psql
    table: Table

    @property
    def name(self):
        return self.table.name

    def create(self):
        return self.psql.command(self.table.create)

    def drop(self):
        return self.psql.command(self.table.drop)

    def add_primary_key(self):
        return self.psql.command(self.table.add_primary_key)

    def add_references(self):
        return self.psql.command(self.table.add_references)

    def upload(self, *, file: str | None = None, stdin: bool = False):
        from itertools import islice
        from pathlib import Path

        if file is not None:
            file_path = Path(file)

            if file_path.suffix == ".tsv":
                with open(file, "r") as f:
                    return self.psql.upload(self.table.name, islice(f, 1, None))
            elif file_path.suffix == ".gz":
                with subprocess.Popen(
                    f"pv {file} | gzip -d",
                    shell=True,
                    stdout=subprocess.PIPE,
                    text=True,
                ) as process:
                    assert process.stdout is not None
                    return self.psql.upload(
                        self.table.name, islice(process.stdout, 1, None)
                    )
        elif stdin is True:
            import sys
            return self.psql.upload(self.table.name, sys.stdin)
        else:
            return self.psql.upload(self.table.name, self.table.fetch_processed())

    def fetch(self, *, quiet: bool = False):
        return self.table.fetch(quiet=quiet)

    def fetch_processed(self):
        return self.table.fetch_processed()
