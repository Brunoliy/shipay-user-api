from abc import ABC, abstractmethod

from .input_port import InputPort
from .output_port import OutputPort


class UseCase(ABC):
    """Interface for UseCase classes."""

    @abstractmethod
    async def __call__(self, input_port: InputPort) -> OutputPort:
        """Process an use case."""
