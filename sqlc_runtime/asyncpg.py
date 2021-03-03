from typing import Any, Type, Optional, AsyncIterator, TypeVar

import asyncpg
import pydantic

from sqlc_runtime import AsyncCursor, AsyncConnection

T = TypeVar("T", bound=pydantic.BaseModel)


def build_asyncpg_connection(conn: asyncpg.Connection) -> AsyncConnection:
    return AsyncpgConnection(conn)


class AsyncpgConnection:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def execute(self, query: str, *params: Any) -> AsyncCursor:
        return await self._conn.cursor(query, *params)

    async def execute_none(self, query: str, *params: Any) -> None:
        await self._conn.execute(query, *params)

    async def execute_rowcount(self, query: str, *params: Any) -> int:
        status = await self._conn.execute(query, *params)
        return int(status.split(" ")[-1])

    async def execute_one(self, query: str, *params: Any) -> Any:
        row = await self._conn.fetchrow(query, *params)
        return row[0] if row is not None else None

    async def execute_one_model(
        self, model: Type[T], query: str, *params: Any
    ) -> Optional[T]:
        row = await self._conn.fetchrow(query, *params)
        if row is None:
            return None
        return model.parse_obj(row)

    async def execute_many(self, query: str, *params: Any) -> AsyncIterator[Any]:
        async with self._conn.transaction():
            async for row in self._conn.cursor(query, *params):
                yield row[0]

    async def execute_many_model(
        self, model: Type[T], query: str, *params: Any
    ) -> AsyncIterator[T]:
        async with self._conn.transaction():
            async for row in self._conn.cursor(query, *params):
                yield model.parse_obj(row)
