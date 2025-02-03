from domain.interfaces.use_case import UseCase
from domain.ports.users import UsersOutputPort
from interface_adapters.data.models.users import UserModel
from interface_adapters.data.repositories.user_repository import UserRepository
from interface_adapters.dtos.users import AddUserInputDTO


class AddUserUseCase(UseCase):
    """Use case to handle user creation."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def __call__(self, user_dto: AddUserInputDTO) -> None:
        # Converter o DTO para o modelo UserModel
        user = UserModel(
            user_name=user_dto.user_name,
            user_email=user_dto.user_email,
            user_password=user_dto.user_password,
            role_id=user_dto.role_id
        )
        # Chamar o repositório para adicionar o usuário
        return await self._repository.add(user)