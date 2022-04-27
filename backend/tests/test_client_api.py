from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.client import get_session


@pytest.mark.order(1)
def test_post_client(client):
    response1 = client.post(
        "/api/clients/",
        json={"name": "dyvenia",
        "is_active":True,
        "created_at":"2022-04-20T13:57:03.466Z",
        "updated_at": "2022-04-20T13:57:03.466Z"},
    )
    data1 = response1.json()
    assert response1.status_code == 200
    assert data1 == {"id":1,
        "name": "dyvenia",
        "is_active":True,
        "created_at":"2022-04-20T13:57:03.466000",
        "updated_at": "2022-04-20T13:57:03.466000"}


def test_read_clients_all(client):
    response = client.get("/api/clients/")
    data = response.json()
    assert data == [{"id":1,
        "name": "dyvenia",
        "is_active":True,
        "created_at":"2022-04-20T13:57:03.466000",
        "updated_at": "2022-04-20T13:57:03.466000"}]


def test_read_client_id(client):
    response1 = client.get("/api/clients/1")
    data1 = response1.json()
    assert data1 =={"id":1,
        "name": "dyvenia",
        "is_active":True,
        "created_at":"2022-04-20T13:57:03.466000",
        "updated_at": "2022-04-20T13:57:03.466000"}
    response2 = client.get("/api/clients/0")
    data2 = response2.json()
    assert data2 == "There is no client with id = 0"

def test_deactivate_clients(client):
    response = client.put("api/clients/1?is_active=false")
    data = response.json()
    assert response.status_code == 200

def test_activate_clients(client):
    response = client.put("api/clients/1?is_active=true")
    data = response.json()
    assert response.status_code == 200


def test_update_clients(client):
    response = client.put("api/clients/1/new-name?new_client_name=dyvenia")
    data = response.json()
    assert response.status_code == 200


