from typing import (
    Protocol,
    Any,
    Union,
    Sequence,
    Tuple,
    Optional,
    Mapping,
    Iterator,
    Type,
    TypeVar,
    AsyncIterator,
    Awaitable,
)

import pydantic


class Cursor(Protocol):
    rowcount: int

    def fetchone(self) -> Mapping[str, Any]:
        pass

    def fetchmany(self, size: int = None) -> Sequence[Mapping[str, Any]]:
        pass

    def fetchall(self) -> Sequence[Mapping[str, Any]]:
        pass

    def __iter__(self) -> Iterator[Mapping[str, Any]]:
        pass

    def __len__(self) -> int:
        pass


T = TypeVar("T", bound=pydantic.BaseModel)


class Connection(Protocol):
    def execute(self, query: str, *params: Any) -> Cursor:
        pass

    def execute_none(self, query: str, *params: Any) -> None:
        pass

    def execute_rowcount(self, query: str, *params: Any) -> int:
        pass

    def execute_one(self, query: str, *params: Any) -> Any:
        pass

    def execute_one_model(
        self, model: Type[T], query: str, *params: Any
    ) -> Optional[T]:
        pass

    def execute_many(self, query: str, *params: Any) -> Iterator[Any]:
        pass

    def execute_many_model(
        self, model: Type[T], query: str, *params: Any
    ) -> Iterator[T]:
        pass


class AsyncCursor(Protocol):
    async def fetch(
        self, n: int, *, timeout: float = None
    ) -> Sequence[Mapping[str, Any]]:
        pass

    async def fetchrow(self, *, timeout: float = None) -> Mapping[str, Any]:
        pass

    async def forward(self, n: int, *, timeout: float = None) -> int:
        pass


class AsyncConnection(Protocol):
    async def execute(self, query: str, *params: Any) -> AsyncCursor:
        pass

    async def execute_none(self, query: str, *params: Any) -> None:
        pass

    async def execute_rowcount(self, query: str, *params: Any) -> int:
        pass

    async def execute_one(self, query: str, *params: Any) -> Any:
        pass

    async def execute_one_model(
        self, model: Type[T], query: str, *params: Any
    ) -> Optional[T]:
        pass

    def execute_many(self, query: str, *params: Any) -> AsyncIterator[Any]:
        pass

    def execute_many_model(
        self, model: Type[T], query: str, *params: Any
    ) -> AsyncIterator[T]:
        pass


GenericConnection = Union[Connection, AsyncConnection]
GenericCursor = Union[Cursor, AsyncCursor]

RT = TypeVar("RT")
ReturnType = Union[RT, Awaitable[RT]]
IteratorReturn = Union[Iterator[RT], AsyncIterator[RT]]
