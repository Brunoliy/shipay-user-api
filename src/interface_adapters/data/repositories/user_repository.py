import random
import string

from domain.ports.users import UsersOutputPort
from frameworks.database.postgres_manager import PostgresqlManager
from interface_adapters.data.models.users import UserModel


class UserRepository:
    """Repository to handle with mood capture uploads."""

    def __init__(self, database_service: PostgresqlManager) -> None:
        self._db = database_service

    def generate_password(self, length: int = 8) -> str:
        """Gera uma senha aleatória se não fornecida."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    async def add(self, user: UserModel) -> None:
        """Add a new user to the database."""
        # Se a senha não for fornecida, gera uma senha
        if not user.user_password:
            user.user_password = self.generate_password()

        async with self._db.session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

    async def find_info_by_id(self, user_id: int) -> UsersOutputPort:
        """Get happy location by user."""
        await self._db.connect()
        async with self._db.session() as session:
            user_id = await UserModel.find_info_by_id(session=session, user_id=user_id)
        return await user_id

    async def find_by_role_id(self, role_id: int) -> UsersOutputPort:
        ...

