# pylint: disable=R0801,R0902
from pydantic.dataclasses import dataclass

from domain.interfaces.output_port import OutputPort


@dataclass
class Role:
    """Object to describe the role of a user."""
    description: str

@dataclass
class Claims:
    """Object to describe the claims of a user."""
    description: str
    is_active: bool

@dataclass
class UsersOutputPort(OutputPort):
    """Object to describe the result of mood upload."""

    user_name: str
    user_email: str
    roles: list[Role]
    claims: list[Claims]
