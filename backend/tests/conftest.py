# A file containing fixtures for testing
# Fixtures defined here are available for the whole scope
from fastapi.testclient import TestClient
import pytest
import os
from ..main import app
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session


local_test_con_str = f"postgresql://test_user:password@127.0.0.1:5434/pytest_db"
local_test_engine = create_engine(local_test_con_str, echo=True, pool_size=20)


# @pytest.fixture(name="timeflow_env")
# def dev_test_env():
#     os.environ["TIMEFLOW_DEV"] = "true"
#     return True


@pytest.fixture(scope="session", name="session")
def session_fixture():
    with Session(local_test_engine) as session:
        yield session


@pytest.fixture(scope="session", name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="create_db", scope="session")
def create_db():
    # setup
    SQLModel.metadata.create_all(test_engine)
    yield
    # teardown
    os.remove(db_name)


@pytest.fixture(name="session")
def session_fixture(create_db):
    create_db

    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
