from fastapi.testclient import TestClient
import pytest
import os
from ..main import app
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session


@pytest.mark.order(10)
def test_post_timelog(client):
    # testing post
    response1 = client.post(
        "/api/timelogs/",
        json={
            "user_id": 1,
            "start_time": "2022-01-19T08:30:00.000Z",
            "end_time": "2022-01-19T10:50:00.000Z",
            "epic_id": 1,
            "count_hours": 0,
            "count_days": 0,
            "month": 1,
            "year": 2022,
        },
    )
    data1 = response1.json()
    assert data1 == {
            "id":1,
            "user_id": 1,
            "start_time": "2022-01-19T08:30:00",
            "end_time": "2022-01-19T10:50:00",
            "epic_id": 1,
            "count_hours": 2.33,
            "count_days": 0.29,
            "month": 1,
            "year": 2022,
        }
    # testing overlap
    response2 = client.post(
        "/api/timelogs/",
        json={
            "user_id": 1,
            "start_time": "2022-01-19T08:30:00",
            "end_time": "2022-01-19T10:50:00",
            "epic_id": 1,
            "count_hours": 2.33,
            "count_days": 0.29,
            "month": 1,
            "year": 2022,
        },
    )
    data2 = response2.json()
    assert data2 == "currently posted timelog overlaps another timelog"
    # testing start_time > end_time
    response3 = client.post(
        "/api/timelogs/",
        json={
            "id":1,
            "user_id": 1,
            "start_time": "2022-02-19T11:30:00",
            "end_time": "2022-02-19T10:50:00",
            "epic_id": 1,
            "count_hours": 2.33,
            "count_days": 0.29,
            "month": 1,
            "year": 2022,
        },
    )
    data3 = response3.json()
    assert response3.status_code == 422
    assert data3 == {
        "detail": [
            {
                "loc": ["body", "__root__"],
                "msg": "start_time must be smaller then end_time",
                "type": "assertion_error",
            }
        ]
    }

def test_get_timelogs_all(client):
    response = client.get("/api/timelogs/")
    data = response.json()
    assert data == [
        {
            "id":1,
            "username": "jsmith",
            "start_time": "2022-01-19T08:30:00",
            "end_time": "2022-01-19T10:50:00",
            "epic_name": "new_sn",
            "count_hours": 2.33,
            "count_days": 0.29,
        }
    ]


def test_get_timelog_by_id(client):
    response = client.get("api/timelogs/1")
    data = response.json()
    assert data == {
            "id":1,
            "user_id": 1,
            "start_time": "2022-01-19T08:30:00",
            "end_time": "2022-01-19T10:50:00",
            "epic_id": 1,
            "count_hours": 2.33,
            "count_days": 0.29,
            "month": 1,
            "year": 2022,
        }


def test_delete_timelogs(client):
    response = client.delete(
        "/api/timelogs/1"
    )
    data = response.json()
    assert data == True
