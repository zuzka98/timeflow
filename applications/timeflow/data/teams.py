import requests
import json
from typing import List

from uiflow.components.input import display_value

from ..config import base_url
from datetime import datetime
from .common import Select


def post_team(name: str, short_name: str, lead_user_id: int):
    data = {
        "name": name,
        "short_name": short_name,
        "lead_user_id": lead_user_id,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    response = requests.post(
        f"{base_url}/api/teams",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def get_active_team_rows():
    """Get all active teams and store them in a list."""
    api = f"{base_url}/api/teams/"
    params = {"is_active": None}
    response = requests.get(api, params=params)

    rows = []
    for item in response.json():
        d = {
            "Team name": item["team_name"],
            "Team short name": item["team_short_name"],
            "User lead": item["username"],
            "Is active": item["is_active"],
        }
        rows.append(d)
    return rows


def teams_names(is_active: bool = None, label="select team") -> List[Select]:
    api_team = f"{base_url}/api/teams/"
    params = {"is_active": is_active}
    response = requests.get(api_team, params=params)
    team_rows = [Select(value="", display_value=label)]
    for item in response.json():
        d = Select(value=item["team_name"], display_value=item["team_name"])
        team_rows.append(d)
    return team_rows


def teams_id_name(label="select team", no_team: bool = False) -> List[Select]:
    """Gets list of teams by short_name and id

    get endpoint: /api/teams/active
    Returns:
        List[Select]: list of dictionaries
    """

    api = f"{base_url}/api/teams/active"
    response = requests.get(api)
    rows = [Select(value="", display_value=label)]
    if no_team is True:
        rows.append(Select(value="", display_value="no team"))
    for item in response.json():
        d = Select(value=item["id"], display_value=item["team_short_name"])
        rows.append(d)
    return rows


def team_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/teams/{name_to_activ}/activate"
    response = requests.put(api)
    return True


def team_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/teams/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True
