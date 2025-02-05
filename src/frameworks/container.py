from dependency_injector import containers, providers

from domain.use_cases.add_user import AddUserUseCase
from domain.use_cases.get_all_user_info import GetAllUserInfoUseCase
from domain.use_cases.get_role_by_id import GetRoleByIdUseCase
from domain.use_cases.get_user_by_id_using_raw import GetUserByIdUsingRawUseCase
from frameworks.database.postgres_manager import PostgresqlManager
from interface_adapters.data.repositories.user_repository import UserRepository


class FrameworkContainer(containers.DeclarativeContainer):
    """Framework container"""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "interface_adapters.routes.health_check",
            "interface_adapters.routes.v1.users",
            "main",
        ],
    )

    database_manager: PostgresqlManager = providers.Factory(PostgresqlManager)

    # Repositories
    user_repository: UserRepository = providers.Factory(
        UserRepository, database_service=database_manager
    )

    # use cases
    get_all_user_info_use_case: GetAllUserInfoUseCase = providers.Factory(
        GetAllUserInfoUseCase, repository=user_repository
    )
    add_user_use_case: AddUserUseCase = providers.Factory(
        AddUserUseCase, repository=user_repository
    )
    get_role_by_id_use_case: GetRoleByIdUseCase = providers.Factory(
        GetRoleByIdUseCase, repository=user_repository
    )
    get_user_by_id_using_raw_use_case: GetUserByIdUsingRawUseCase = providers.Factory(
        GetUserByIdUsingRawUseCase, repository=user_repository
    )

