import requests
import json

from applications.timeflow.pages.forecasts import display_value
from backend.models import role
from ..config import base_url
from typing import List, TypedDict
from datetime import datetime
from .common import Select


class Role(TypedDict):
    short_name: str
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


def to_role(
    short_name: str,
    name: str,
    created_at: datetime,
    updated_at: datetime,
    is_active: bool,
) -> bool:
    data = Role(
        short_name=short_name,
        name=name,
        created_at=created_at,
        updated_at=updated_at,
        is_active=True,
    )
    response = requests.post(
        f"{base_url}/api/roles",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )
    return True


def roles_active():
    api = f"{base_url}/api/roles/"
    params = {"is_active": None}
    response = requests.get(api, params=params)
    data = response.json()
    rows = []
    for item in data:
        d = {
            "id": item["id"],
            "full name": item["name"],
            "short_name": item["short_name"],
            "is active": item["is_active"],
        }
        rows.append(d)
    return rows


def roles_names_active(label="select user") -> List[Select]:
    api_role_id = f"{base_url}/api/roles"
    params = {"is_active": True}
    response_role_id = requests.get(api_role_id, params=params)
    role_id_rows = [Select(value="", display_value=label)]
    for item in response_role_id.json():
        d = Select(value=item["id"], display_value=item["id"])
        role_id_rows.append(d)
    return role_id_rows


def roles_names_inactive(label="select user") -> List[Select]:
    api_role_id = f"{base_url}/api/roles"
    params = {"is_active": False}
    response_role_id = requests.get(api_role_id, params=params)
    role_id_rows = [Select(value="", display_value=label)]
    for item in response_role_id.json():
        d = Select(value=item["id"], display_value=item["id"])
        role_id_rows.append(d)
    return role_id_rows


def role_update(id: int, new_name: str = None, new_short_name: str = None) -> bool:
    if new_name != "" and new_short_name != "":
        api = f"{base_url}/api/roles/?id={id}&new_name={new_name}&new_short_name={new_short_name}"
    elif new_name != "" and new_short_name == "":
        api = f"{base_url}/api/roles/?id={id}&new_name={new_name}"
    elif new_name == "" and new_short_name != "":
        api = f"{base_url}/api/roles/?id={id}&new_short_name={new_short_name}"
    response = requests.put(api)
    return True


def roles_id_name() -> List[Select]:
    """Gets list of roles by short_name and id

    api get: /api/roles/active
    Returns:
        List[Select]: list of dictionaries
    """
    api = f"{base_url}/api/roles/active"
    response = requests.get(api)
    rows = [Select(value="", display_value="select role")]
    for item in response.json():
        d = Select(value=item["id"], display_value=item["short_name"])
        rows.append(d)
    return rows
