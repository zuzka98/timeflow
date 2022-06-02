import requests
import json
from typing import List, TypedDict, Dict, Optional

from ..config import base_url
from .common import Select
from datetime import date, datetime


class Epic(TypedDict):
    short_name: str
    name: str
    team_id: int
    sponsor_id: int
    start_date: str
    is_active: bool
    created_at: str
    updated_at: str


def to_epic(
    short_name: str,
    name: str,
    team_id: int,
    sponsor_id: int,
    start_date: str,
    is_active: bool,
    created_at: str,
    updated_at: str,
):
    """Posts data to epics table

    Args:
        short_name (str): new epic's short name
        name (str): new epic's full name
        team_id (int): team id new epic is for
        sponsor_id (int): sponsor id new epic is for
        start_date (str): date of epic's start
        is_active (bool): set to True on post
        created_at (str): datetime string of when the epic was created
        updated_at (str): datetime string of when the epic was updated
    """
    data = Epic(
        short_name=short_name,
        name=name,
        team_id=team_id,
        sponsor_id=sponsor_id,
        start_date=start_date,
        is_active=is_active,
        created_at=created_at,
        updated_at=updated_at,
    )
    respone = requests.post(
        f"{base_url}/api/epics",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def epics_names(is_active: bool = None, label="select epic") -> List[Select]:
    """Gets list of active epics by name and id
    Returns a list of dictionaries
    """
    api = f"{base_url}/api/epics/"
    params = {"is_active": is_active}
    response = requests.get(api, params=params)
    epic_name_rows = [Select(value="", display_value=label)]
    for item in response.json():
        d = Select(value=item["epic_id"], display_value=item["epic_name"])
        epic_name_rows.append(d)
    return epic_name_rows


def epics_all() -> List[Dict]:
    api = f"{base_url}/api/epics/"
    params = {"is_active": None}
    response = requests.get(api, params=params)
    rows = []
    for item in response.json():
        d = {
            "epic id": item["epic_id"],
            "epic name": item["epic_name"],
            "epic short name": item["short_name"],
            "team name": item["team_name"],
            "sponsor name": item["sponsor_short_name"],
            "start date": item["start_date"],
            "is active": item["is_active"],
        }
        rows.append(d)
    return rows


def epics_by_team_sponsor(team_id: int, sponsor_id: int) -> List[Select]:
    """gets epics by team and sponsor

    Args:
        team_id (int): id of the team an epic is filtered with
        sponsor_id (int): id of the sponsor an epic is filtered with
    """
    api = f"{base_url}/api/epics/teams/{team_id}/sponsors/{sponsor_id}/"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "epic id": item["epic_id"],
            "short name": item["short_name"],
            "epic name": item["epic_name"],
            "team name": item["team_name"],
            "sponsor name": item["sponsor_short_name"],
            "start date": item["start_date"],
        }
        rows.append(d)
    return rows


def client_name_by_epic_id(epic_id) -> Select:
    """Gets client name by given id"""
    api_client_name_id = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name_id = requests.get(api_client_name_id)
    r = response_client_name_id.json()
    client_name = r.get("client_name")
    client_id = r.get("client_id")
    d = Select(value=client_id, display_value=client_name)
    return d


def epic_activate(epic_id):
    api = f"{base_url}/api/epics/{epic_id}/activate"
    response = requests.put(api)
    return True


def epic_deactivate(epic_id):
    api = f"{base_url}/api/epics/{epic_id}/deactivate"
    response = requests.put(api)
    return True


def update_epic(
    epic_id: int,
    new_epic_name: Optional[str] = None,
    new_short_name: Optional[str] = None,
    new_team_id: Optional[int] = None,
    new_sponsor_id: Optional[int] = None,
    new_start_date: Optional[date] = None,
):
    api = f"{base_url}/api/epics/{epic_id}/"
    params = {
        "new_epic_name": new_epic_name,
        "new_short_name": new_short_name,
        "new_team_id": new_team_id,
        "new_sponsor_id": new_sponsor_id,
        "new_start_date": new_start_date,
    }

    api_params = params.copy()

    for param in params.keys():
        if api_params[param] == "":
            api_params.pop(param)

    response = requests.put(api, params=api_params)
    return True
