from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.epic_area import get_session


@pytest.mark.order(3)
def test_post_epic_area(client):
    response = client.post(
        "/api/epic_areas/",
        json={
            "epic_id": 1,
            "name": "graphics",
            "is_active": True,
            "created_at": "2022-04-21T08:57:31.591Z",
            "updated_at": "2022-04-21T08:57:31.591Z"
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
            "id":1,
            "epic_id": 1,
            "name": "graphics",
            "is_active": True,
            "created_at": "2022-04-21T08:57:31.591000",
            "updated_at": "2022-04-21T08:57:31.591000"
        }

def test_get_epic_areas_list(client):
    response = client.get("/api/epic_areas/")
    data = response.json()
    assert response.status_code == 200
    assert data == [
        {
            "id":1,
            "epic_id": 1,
            "name": "graphics",
            "is_active": True,
            "created_at": "2022-04-21T08:57:31.591000",
            "updated_at": "2022-04-21T08:57:31.591000"
        }
    ]

def test_deactivate_epic_area(client):
    response = client.put("/api/epic_areas/graphics/deactivate")
    assert response.status_code == 200

def test_activate_epic_area(client):
    response = client.put("api/epic_areas/graphics/activate")
    assert response.status_code == 200

def test_update_epic_area(client):
    response = client.put("/api/epic_areas/?id=1&new_name=graphics&is_active=True&new_epic_id=2")
    data = response.json()
    assert response.status_code == 200

