import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.business.auth.auth_verifier import AuthVerifier
from server.business.auth.token import create_access_token
from server.routes.routes import get_all_routes
from server.shared.config import Config
from server.shared.databasemanager import DatabaseManager


@pytest.fixture(scope="session")
def app(
    config: Config,
    database: DatabaseManager,
    auth_verifier: AuthVerifier,
) -> FastAPI:
    app = FastAPI()
    app.include_router(get_all_routes(config, database, auth_verifier))
    return app


@pytest.fixture
def unauthenticated_test_client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_client(app: FastAPI, user_id: str, config: Config) -> TestClient:
    client = TestClient(app)
    access_token = create_access_token(config, user_id)
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client
