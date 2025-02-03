from pydantic import BaseModel  # pylint: disable=E0611
from pydantic import Field  # pylint: disable=E0611


class RolesDTO(BaseModel):
    """Roles DTO"""

    role_id: int = Field(default=None)
    role_description: str = Field(default=None)

class ClaimsDTO(BaseModel):
    """Claims DTO"""

    claim_id: int = Field(default=None)
    claim_description: str = Field(default=None)
    active: bool = Field(default=None)

class AddUserInputDTO(BaseModel):
    """AddUser DTO"""

    user_name: str = Field(default=None)
    user_email: str = Field(default=None)
    user_password: str = Field(default=None)
    role_id: int = Field(default=None)


class UserOutputDTO(BaseModel):
    """UserOutput DTO"""

    user_name: str = Field(default=None)
    user_email: str = Field(default=None)
    roles: list[RolesDTO] = Field(default=None)
    claims: list[ClaimsDTO] = Field(default=None)


