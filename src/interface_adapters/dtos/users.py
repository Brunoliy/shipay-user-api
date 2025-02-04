from pydantic import BaseModel  # pylint: disable=E0611
from pydantic import Field  # pylint: disable=E0611


class AddUserInputDTO(BaseModel):
    """AddUser DTO"""

    name: str = Field(default=None)
    email: str = Field(default=None)
    role_id: int = Field(default=None)
    claims: list[int] = Field(default=None)
    password: str | None = Field(default=None)
