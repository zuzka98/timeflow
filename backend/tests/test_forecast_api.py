from fastapi.testclient import TestClient
import pytest
import os
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session


@pytest.mark.order(3)
def test_post_forecast(client):
    response = client.post(
        "/api/forecasts/",
        json={
            "user_id": 1,
            "epic_id": 1,
            "days": 10,
            "month": 5,
            "year": 2022,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "user_id": 1,
        "epic_id": 1,
        "days": 10,
        "month": 5,
        "year": 2022,
    }


def test_get_forecasts(client):
    response = client.get("/api/forecasts")
    assert response.json() == [
        {
            "id": 1,
            "user_id": 1,
            "epic_id": 1,
            "days": 10,
            "month": 5,
            "year": 2022,
        }
    ]



# def test_get_forecasts_users(client):
#     response = client.get("/api/forecasts/?user_id=1")
#     assert response.json() == [
#         {
#             "id": 1,
#             "user_id": 1,
#             "epic_id": 1,
#             "days": 10,
#             "month": 5,
#             "year": 2022,
#         }
#     ]


# @pytest.mark.order(-1)
def test_delete_forecasts(client):
    response = client.delete("/api/forecasts/?forecast_id=1")
    assert response.status_code == 200
