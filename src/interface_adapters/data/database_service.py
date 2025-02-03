from abc import ABCMeta, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Union

from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseService(metaclass=ABCMeta):
    """A service to give access to database client features."""

    @asynccontextmanager
    @abstractmethod
    async def session(self) -> AsyncIterator[Union[AsyncSession, Any]]:
        """Return an object that create a session within a context scope
        with database.session() as session:
        See also: https://docs.sqlalchemy.org/en/14/orm/session_api.html?highlight=transaction#sqlalchemy.orm.Session.transaction"""  # noqa:E501
        yield None

    @asynccontextmanager
    @abstractmethod
    async def transaction(self) -> AsyncIterator[Union[AsyncSession, Any]]:
        """https://docs.sqlalchemy.org/en/14/orm/session_api.html?highlight=transaction#sqlalchemy.orm.Session.transaction"""  # noqa:E501
        yield None
