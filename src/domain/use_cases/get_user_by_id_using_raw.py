from fastapi import HTTPException

from domain.interfaces.use_case import UseCase
from domain.ports.users import UsersOutputPort
from interface_adapters.data.repositories.user_repository import UserRepository


class GetUserByIdUsingRawUseCase(UseCase):
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, user_id: int) -> UsersOutputPort:
        """Get all user info."""
        if not (result := await self._repository.find_user_by_id_using_raw(user_id=user_id)):
            raise HTTPException(status_code=400, detail="User not found")
        return result