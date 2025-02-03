from domain.interfaces.use_case import UseCase
from domain.ports.users import UsersOutputPort
from interface_adapters.data.repositories.user_repository import UserRepository


class GetAllUserInfoUseCase(UseCase):

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, user_id: int) -> UsersOutputPort:
        return await self._repository.find_info_by_id(user_id=user_id)