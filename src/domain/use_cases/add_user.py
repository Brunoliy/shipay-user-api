import random
import string

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from domain.interfaces.use_case import UseCase
from interface_adapters.data.models.users import User
from interface_adapters.data.repositories.user_repository import UserRepository
from interface_adapters.dtos.users import AddUserInputDTO


class AddUserUseCase(UseCase):
    """Use case to handle user creation."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, user_dto: AddUserInputDTO):
        """Create a user."""
        user_pwd = user_dto.password if user_dto.password else self._generate_password()
        user_model = User(
            name=user_dto.name,
            email=user_dto.email,
            password=user_pwd,
            role_id=user_dto.role_id,
        )

        try:
            user = await self._repository.add_user(user_model)
            await self._repository.add_user_claims(user.id, user_dto.claims)
            return user

        except IntegrityError as e:
            if "unique constraint" in str(e.orig).lower():
                raise HTTPException(status_code=400, detail="Email already registered")
            raise HTTPException(status_code=500, detail="Database error occurred")


    def _generate_password(self, length: int = 8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for i in range(length))