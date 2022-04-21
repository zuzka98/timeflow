import pytest
from ..main import app, session


# @pytest.mark.order(1)
def test_post_team(client):
    response = client.post(
        "/api/teams/",
        json={
            "lead_user_id": 1,
            "name": "juniors",
            "short_name": "jrs",
            "is_active": True,
            "created_at": "2022-04-21T12:32:37.345Z",
            "updated_at": "2022-04-21T12:32:37.345Z"

        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "lead_user_id": 1,
        "name": "juniors",
        "short_name": "jrs",
        "is_active": True,
        "created_at": "2022-04-21T12:32:37.345000",
        "updated_at": "2022-04-21T12:32:37.345000"
    }

def test_get_teams_list(client):
    response = client.get("/api/teams/")
    data = response.json()
    assert data == [
        {
        "id": 1,
        "lead_user_id": 1,
        "name": "juniors",
        "short_name": "jrs",
        "is_active": True,
        "created_at": "2022-04-21T12:32:37.345000",
        "updated_at": "2022-04-21T12:32:37.345000"
    }
    ]

def test_read_teams(client):
    response = client.get("/api/teams/juniors")
    data = response.json()
    assert response.status_code == 200
    assert data ==  {
        "id": 1,
        "lead_user_id": 1,
        "name": "juniors",
        "short_name": "jrs",
        "is_active": True,
        "created_at": "2022-04-21T12:32:37.345000",
        "updated_at": "2022-04-21T12:32:37.345000"
    }


def test_update_team(client):
    response = client.put(
        "api/teams/?id=1&new_name=juniors&active=True&new_lead_user_id=2"
    )
    data = response.json()
    assert response.status_code == 200
    assert data == True

def test_deactivate_teams(client):
    response = client.put("/api/teams/juniors/deactivate")
    assert response.status_code == 200

def test_activate_teams(client):
    response = client.put("/api/teams/juniors/activate")
    assert response.status_code == 200
