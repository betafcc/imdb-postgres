import subprocess
from dataclasses import dataclass
from typing import Iterable

URL = "https://datasets.imdbws.com/{}.tsv.gz"


def fetch(table: str) -> Iterable[str]:
    url = URL.format(table.replace("_", "."))

    with subprocess.Popen(
        f"wget -O - -o '{url}' | gzip -d", shell=True, stdout=subprocess.PIPE, text=True
    ) as process:
        if process.stdout is not None:
            for line in process.stdout:
                yield line


@dataclass
class Psql:
    username: str
    password: str
    dbname: str
    host: str = "127.0.0.1"
    port: int = 5432

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
            env={"PGPASSWORD": self.password},
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
            env={"PGPASSWORD": self.password},
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
            env={"PGPASSWORD": self.password},
            stdin=subprocess.PIPE,
            text=True,
        ) as process:
            assert process.stdin is not None
            for row in rows:
                process.stdin.write(row)
                process.stdin.flush()
            process.stdin.close()

            ret = process.wait()
            if ret != 0:
                raise Exception(f"Subprocess failed with return code: {ret}")
