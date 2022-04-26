import pytest
from fastapi.testclient import TestClient
from ..main import app, session


@pytest.mark.order(2)
def test_post_sponsor(client):
    response = client.post(
        "/api/sponsors/",
        json={
            "client_id": 1,
            "name": "facebook",
            "short_name": "fb",
            "is_active": True,
            "created_at": "2022-04-20T14:40:17.413Z",
            "updated_at": "2022-04-20T14:40:17.413Z"
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 1,
        "name": "facebook",
        "short_name": "fb",
        "is_active": True,
        "created_at": "2022-04-20T14:40:17.413000",
        "updated_at": "2022-04-20T14:40:17.413000"
    }

def test_get_sponsors_list(client):
    response = client.get("/api/sponsors/")
    data = response.json()
    assert data == [
        {
        "id": 1,
        "client_id": 1,
        "name": "facebook",
        "short_name": "fb",
        "is_active": True,
        "created_at": "2022-04-20T14:40:17.413000",
        "updated_at": "2022-04-20T14:40:17.413000"
    }
    ]

def test_read_sponsors(client):
    response = client.get("/api/sponsors/facebook")
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "client_id": 1,
        "name": "facebook",
        "short_name": "fb",
        "is_active": True,
        "created_at": "2022-04-20T14:40:17.413000",
        "updated_at": "2022-04-20T14:40:17.413000"
    }


def test_update_sponsor(client):
    response = client.put(
        "api/sponsors/?id=1&new_client_id=2&new_name=twitter&new_short_name=tw"
    )
    data = response.json()
    assert response.status_code == 200




def test_deactivate_sponsors(client):
    response = client.put("/api/sponsors/1/deactivate")
    assert response.status_code == 200
