import re
from typing import Any, Type, Iterator, TypeVar, Optional, TYPE_CHECKING

import pydantic
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

from sqlc_runtime import Connection

T = TypeVar("T", bound=pydantic.BaseModel)
PSYCOPG2_PLACEHOLDER_REGEXP = re.compile(r"\B\$\d+\b")


def build_psycopg2_connection(conn: connection) -> Connection:
    return Psycopg2Connection(conn)


class Psycopg2Connection:
    def __init__(self, conn: connection):
        self._conn = conn

    def execute(self, query: str, *params: Any) -> DictCursor:
        query = PSYCOPG2_PLACEHOLDER_REGEXP.sub("%s", query)
        cur = self._conn.cursor(cursor_factory=DictCursor)
        cur.execute(query, params)
        return cur

    def execute_none(self, query: str, *params: Any) -> None:
        with self.execute(query, *params):
            return

    def execute_rowcount(self, query: str, *params: Any) -> int:
        with self.execute(query, *params) as cur:
            return cur.rowcount

    def execute_one(self, query: str, *params: Any) -> Any:
        with self.execute(query, *params) as cur:
            row = cur.fetchone()
            return row[0] if row is not None else None

    def execute_one_model(
        self, model: Type[T], query: str, *params: Any
    ) -> Optional[T]:
        with self.execute(query, *params) as cur:
            row = cur.fetchone()
            if row is None:
                return None
            return model.parse_obj(row)

    def execute_many(self, query: str, *params: Any) -> Iterator[Any]:
        with self.execute(query, *params) as cur:
            for row in cur:
                yield row[0]

    def execute_many_model(
        self, model: Type[T], query: str, *params: Any
    ) -> Iterator[T]:
        with self.execute(query, *params) as cur:
            for row in cur:
                yield model.parse_obj(row)
