import logging
import sys

from fastapi import APIRouter, FastAPI

from interface_adapters.routes.health_check import system_state_router
from interface_adapters.routes.v1.users import users_route

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(filename)s %(funcName)s: %(message)s",
    level=logging.INFO,
)


class FastApiManager:
    """Fast Api handler"""

    def __init__(self, app: FastAPI) -> None:
        self._app = app
        self._logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def initialize_cors(self) -> None:
        """Fast API cors"""

    def initialize_limiter(self) -> None:
        """Limiter initalizer"""

    def initialize_routers(self) -> None:
        """Fast API routes"""
        self._logger.info("Adding routes...")
        api_router = APIRouter()
        api_router.include_router(
            system_state_router, prefix="/v1", tags=["System State"]
        )
        api_router.include_router(users_route, prefix="/v1", tags=["Post"])

        self._app.include_router(api_router)

    def get_instance(self) -> FastAPI:
        """Fast Api instance"""
        return self._app
