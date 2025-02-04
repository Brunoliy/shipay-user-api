# pylint: disable=R0801,R0902
from pydantic.dataclasses import dataclass

from domain.interfaces.output_port import OutputPort


@dataclass
class ClaimsPort:
    """Object to describe the claims of a user."""

    description: str
    active: bool | None


@dataclass
class UsersOutputPort(OutputPort):
    """Object to describe user output port."""

    name: str
    email: str
    role: str
    claims: list[ClaimsPort]

@dataclass
class RolesOutputPort(OutputPort):
    """Object to describe role output port."""

    description: str
