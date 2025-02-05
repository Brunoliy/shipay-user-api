from unittest.mock import AsyncMock

import pytest
from dependency_injector.providers import Factory
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK

from domain.ports.users import ClaimsPort, UsersOutputPort
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

# Mock data
mock_user_output = UsersOutputPort(
    name="Jane Doe",
    email="jane@example.com",
    role="Admin",
    claims=[ClaimsPort(description="Read Access", active=True)],
)

mock_role_output = {"description": "Admin"}

mock_user_data = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "role_id": 2,
    "claims": [1],
    "password": "secure123",
}

# Test function
@pytest.mark.asyncio
async def test_create_user(client, mock_container):
    # Mock the use case to return mock data
    mock_use_case = mock_container.add_user_use_case()
    mock_use_case.return_value = None  # No actual return value

    response = client.post("/users/create/", json=mock_user_data)

    assert response.status_code == HTTP_200_OK
    assert response.json()["name"] == mock_user_data["name"]
    assert response.json()["email"] == mock_user_data["email"]
    assert response.json()["role_id"] == mock_user_data["role_id"]

@pytest.mark.asyncio
async def test_get_user_info(client, mock_container):
    # Mock the get_user_info_use_case to return mock_user_output
    mock_use_case = mock_container.get_all_user_info_use_case()
    mock_use_case.return_value = mock_user_output

    response = client.get("/users/user/info?user_id=1")

    assert response.status_code == HTTP_200_OK
    assert response.json()["name"] == mock_user_output.name
    assert response.json()["email"] == mock_user_output.email
    assert response.json()["role"] == mock_user_output.role
    assert response.json()["claims"][0]["description"] == mock_user_output.claims[0].description

@pytest.mark.asyncio
async def test_get_role_by_id(client, mock_container):
    # Mock the get_role_by_id_use_case to return mock_role_output
    mock_use_case = mock_container.get_role_by_id_use_case()
    mock_use_case.return_value = mock_role_output

    response = client.get("/users/role/info?role_id=2")

    assert response.status_code == HTTP_200_OK
    assert response.json()["description"] == mock_role_output["description"]