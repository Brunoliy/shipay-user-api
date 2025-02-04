from unittest.mock import AsyncMock

import pytest
from dependency_injector.providers import Factory
from fastapi import FastAPI
from fastapi.testclient import TestClient

from frameworks.container import FrameworkContainer
from interface_adapters.routes.v1.users import users_route

app = FastAPI()
container = FrameworkContainer()
app.container = container
app.include_router(users_route)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_container():
    container = FrameworkContainer()
    container.get_all_user_info_use_case.override(Factory(lambda: AsyncMock()))
    container.get_user_by_id_sql_use_case.override(Factory(lambda: AsyncMock()))
    container.get_role_by_id_use_case.override(Factory(lambda: AsyncMock()))
    container.add_user_use_case.override(Factory(lambda: AsyncMock()))
    return container


@pytest.mark.asyncio
async def test_create_user(client, mock_container):
    mock_use_case = mock_container.add_user_use_case()
    mock_use_case.return_value = None

    user_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "role_id": 2,
        "claims": [1],
        "password": "secure123"
    }

    response = client.post("/users/create/", json=user_data)

    assert response.status_code == 200
    assert response.json() == user_data
