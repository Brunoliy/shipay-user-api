# pylint: disable=R0902
import logging
import os
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from interface_adapters.data.database_service import DatabaseService


class ConnectionUnavailable(RuntimeError):
    """Exception used to signal that a connection has not been established yet"""


class PostgresqlManager(DatabaseService):
    """Postgres implementation for single connection"""

    def __init__(self) -> None:
        self._host: str = os.environ.get("DB_HOST", "localhost")
        self._port: str = os.environ.get("DB_PORT", "5435")
        self._database: str = os.environ.get("DB_DATABASE", "shipay_users_db")
        self._user: str = os.environ.get("DB_USER", "postgres")
        self._password: str = os.environ.get("DB_PASSWORD", "postgres")
        self._engine: AsyncEngine = None
        self._session_factory: async_scoped_session = None
        self._logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    async def connect(self) -> None:
        """Connect to a Postgres cluster."""
        await self.close()
        url = self._create_url()
        self._engine = create_async_engine(url)
        self._session_factory = async_scoped_session(
            sessionmaker(
                self._engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            ),
            scopefunc=current_task,
        )
        self._logger.info("Connected to database.")

    async def close(self) -> None:
        """Close the current database connection."""
        if self._engine:
            await self._engine.dispose()
            self._logger.info("Closed database connection.")

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSession]:
        async with self.session() as session:
            async with session.begin():
                yield session

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_factory is None:
            raise ConnectionUnavailable("There is no data source connection.")
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    def _create_url(self) -> URL:
        self._logger.info(
            "Connecting to %s (%s) as %s.",
            self._database,
            self._host,
            self._user,
        )
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self._user,
            password=self._password,
            database=self._database,
            host=self._host,
            port=self._port,
        )
