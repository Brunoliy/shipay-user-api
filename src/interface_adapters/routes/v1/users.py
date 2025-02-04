from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from domain.ports.users import RolesOutputPort, UsersOutputPort
from domain.use_cases.add_user import AddUserUseCase
from domain.use_cases.get_all_user_info import GetAllUserInfoUseCase
from domain.use_cases.get_role_by_id import GetRoleByIdUseCase
from domain.use_cases.get_user_by_id_sql import GetUserByIdSqlUseCase
from frameworks.container import FrameworkContainer
from interface_adapters.dtos.users import AddUserInputDTO

users_route = APIRouter()


@users_route.get("/users/user/info")
@inject
async def get_user_info(
    user_id: int,
    use_case: GetAllUserInfoUseCase = Depends(
        Provide[FrameworkContainer.get_all_user_info_use_case]
    ),
) -> UsersOutputPort:
    """Route to fetch user basic info by the user_id."""
    return await use_case(user_id=user_id)

@users_route.get("/users/user/sqlinfo")
@inject
async def get_user_info_sql(
    user_id: int,
    use_case: GetUserByIdSqlUseCase = Depends(
        Provide[FrameworkContainer.get_user_by_id_sql_use_case]
    ),
) -> UsersOutputPort:
    """Route to fetch user basic info by the user_id."""
    return await use_case(user_id=user_id)

@users_route.get("/users/role/info")
@inject
async def get_role_by_id(
    role_id: int,
    use_case: GetRoleByIdUseCase = Depends(
        Provide[FrameworkContainer.get_role_by_id_use_case]
    ),
) -> RolesOutputPort:
    """Route to fetch user basic info by the user_id."""
    return await use_case(role_id=role_id)


@users_route.post("/users/create/")
@inject
async def create_user(
    input_dto: AddUserInputDTO,
    use_case: AddUserUseCase = Depends(Provide[FrameworkContainer.add_user_use_case]),
):
    """Route to add a new user."""
    input_use_case = AddUserInputDTO(
        name=input_dto.name,
        email=input_dto.email,
        role_id=input_dto.role_id,
        claims=[claim for claim in input_dto.claims],
        password=input_dto.password,
    )

    await use_case(input_use_case)
    return input_dto
