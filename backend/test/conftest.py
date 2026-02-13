import os
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session

from server.business.auth.auth_verifier import AuthVerifier
from server.business.auth.password import hash_password
from server.data.models.user import User
from server.shared.config import Config, Env
from server.shared.databasemanager import DatabaseManager


@pytest.fixture(scope="session")
def database_url() -> str:
    return os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://hi:dev@127.0.0.1/hi_interview_test",
    )


@pytest.fixture(scope="session")
def config(database_url: str) -> Config:
    return Config(
        env=Env.TEST,
        database_url=database_url,
        access_token_secret_key="test-secret-key",
    )


@pytest.fixture(scope="session")
def auth_verifier(config: Config) -> AuthVerifier:
    return AuthVerifier(config)


@pytest.fixture(scope="session")
def create_database_if_not_exists(database_url: str) -> None:
    default_db_url = database_url.rsplit("/", 1)[0] + "/postgres"
    default_engine = create_engine(default_db_url)

    db_name = database_url.rsplit("/", 1)[1]

    with default_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as conn:
        result = conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        )
        exists = result.scalar() is not None

        if not exists:
            conn.execute(text(f"CREATE DATABASE {db_name}"))

    default_engine.dispose()


@pytest.fixture(scope="session")
def engine(config: Config, create_database_if_not_exists: None) -> Engine:
    return create_engine(config.database_url)


@pytest.fixture(scope="session")
def migrated_database(engine: Engine, config: Config) -> Generator[Engine, None, None]:
    alembic_cfg = AlembicConfig()
    alembic_cfg.set_main_option(
        "script_location",
        os.path.join(os.path.dirname(__file__), "..", "db"),
    )

    # Drop and recreate the public schema, do this before tests (rather than as
    # cleanup) so that the database will still contain the schema after tests,
    # incase you want to inspect it or run queries against it.
    with DatabaseManager(engine).create_session() as session:
        session.execute(text("DROP SCHEMA public CASCADE;"))
        session.execute(text("CREATE SCHEMA public;"))
        session.commit()

    os.environ["DATABASE_URL"] = config.database_url
    alembic_cfg.set_main_option("sqlalchemy.url", config.database_url)
    command.upgrade(alembic_cfg, "head")

    yield engine


@pytest.fixture(scope="session")
def database(migrated_database: Engine) -> DatabaseManager:
    return DatabaseManager(migrated_database)


@pytest.fixture
def session(database: DatabaseManager) -> Generator[Session, None, None]:
    with database.create_session() as session:
        yield session
        session.rollback()


@pytest.fixture(scope="session")
def user_id(database: DatabaseManager) -> str:
    with database.create_session() as session:
        user = User(
            email="testuser@example.com",
            password_hashed=hash_password("testpassword"),
        )
        session.add(user)
        session.commit()
        return user.id
