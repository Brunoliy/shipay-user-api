# pylint: disable=R0801,R0902
from __future__ import annotations

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

from interface_adapters.data.models.base import Model


class UserModel(Model):
    """Database representation for table user"""

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    user_email = Column(String)
    user_password = Column(String)
    role_id = Column(Integer, Foreign_key="roles.role_id")

    @classmethod
    async def add(cls, session: AsyncSession, user: UserModel) -> None:
        """Add a new user."""
        await session.add(user)
        await session.commit()

    @classmethod
    async def find_info_by_id(cls, session: AsyncSession, user_id: int) -> UserModel:
        ...

    @classmethod
    async def find_by_role_id(cls, session: AsyncSession, role_id: int) -> UserModel:
        """Find by its id."""
        # query: Select = select(cls).filter(cls.role_id == role_id)
        # result: Result = await session.execute(query)
        # user = result.scalars().first()
        # return user.user_id if user else None


