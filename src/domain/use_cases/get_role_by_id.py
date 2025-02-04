from fastapi import HTTPException

from domain.interfaces.use_case import UseCase
from domain.ports.users import UsersOutputPort
from interface_adapters.data.repositories.user_repository import (
    RolesOutputPort,
    UserRepository,
)


class GetRoleByIdUseCase(UseCase):
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, role_id: int) -> RolesOutputPort:
        """Get all user info."""
        if not (result := await self._repository.find_by_role_id(role_id=role_id)):
            raise HTTPException(status_code=400, detail="Role not found")
        return result