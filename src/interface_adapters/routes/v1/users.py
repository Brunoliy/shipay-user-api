from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from domain.use_cases.add_user import AddUserUseCase
from domain.use_cases.get_all_user_info import GetAllUserInfoUseCase
from frameworks.container import FrameworkContainer
from interface_adapters.dtos.users import AddUserInputDTO, UserOutputDTO

users_route = APIRouter()


@users_route.get(
    "/users/info", response_model=UserOutputDTO
)
@inject
async def get_user_info(
    user_id: int,
    use_case: GetAllUserInfoUseCase = Depends(
        Provide[FrameworkContainer.get_all_user_info_use_case]
    ),
) -> UserOutputDTO:
    """Route to upload a user mood"""
    try:
        output_use_case = await use_case(user_id=user_id)
        return UserOutputDTO(**output_use_case.dict())
    except Exception as error:
        return {"error": f"{error}"}

@users_route.post("/users/add/", response_model=UserOutputDTO)
@inject
async def add_user(
    input_dto: AddUserInputDTO,
    use_case: AddUserUseCase = Depends(Provide[FrameworkContainer.add_user_use_case]),
) -> UserOutputDTO:
    """Route to add a new user."""
    try:
        # Criar o objeto de entrada para o use case
        input_use_case = AddUserInputDTO(
            user_name=input_dto.user_name,
            user_email=input_dto.user_email,
            user_password=input_dto.user_password,
            role_id=input_dto.role_id
        )

        # Chamar o use case para adicionar o usuário
        output_use_case = await use_case(input_use_case)

        # Retornar o DTO de saída
        return UserOutputDTO(
            user_id=output_use_case.user_id,
            user_name=output_use_case.user_name,
            user_email=output_use_case.user_email,
            role_id=output_use_case.role_id
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
