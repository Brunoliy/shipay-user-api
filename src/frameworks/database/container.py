from dependency_injector.containers import (  # pylint: disable=no-name-in-module
    DeclarativeContainer,
    WiringConfiguration,
)
from dependency_injector.providers import Singleton  # pylint: disable=no-name-in-module

from frameworks.database.postgres_manager import PostgresqlManager


class FrameworkDatabase(DeclarativeContainer):
    """Dependency Container for Database Frameworks"""

    wiring_config = WiringConfiguration(
        modules=["main", __name__],
    )

    manager: PostgresqlManager = Singleton(
        PostgresqlManager,
    )
