import requests
import json
from typing import List

from uiflow.components.input import display_value

from ..config import base_url
from datetime import datetime
from .common import Select


def post_sponsor(name: str, short_name: str, client_id: int):
    data = {
        "name": name,
        "short_name": short_name,
        "client_id": client_id,
        "is_active": True,
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
    }
    response = requests.post(
        f"{base_url}/api/sponsors",
        data=json.dumps(data),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )


def get_active_sponsor_rows():
    """Get all active sponsor and store them in a list."""
    api = f"{base_url}/api/sponsors/"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Sponsor id": item["id"],
            "Sponsor name": item["sponsor_name"],
            "Sponsor short name": item["sponsor_short_name"],
            "Client name": item["client_name"],
            "Is active": item["is_active"],
        }
        rows.append(d)

    return rows


def sponsor_names(is_active: bool = None, label="select sponsor") -> List[Select]:
    api = f"{base_url}/api/sponsors/"
    params = {"is_active": is_active}
    response = requests.get(api, params=params)
    sponsors_rows = [Select(value="", display_value=label)]
    for item in response.json():
        d = Select(value=item["id"], display_value=item["sponsor_name"])
        sponsors_rows.append(d)
    return sponsors_rows


def sponsors_id_name() -> List[Select]:
    """Gets list of sponsors by short_name and id

    api get: /api/sponsors/active
    Returns:
        List[Select]: list of dictionaries
    """
    api = f"{base_url}/api/sponsors/"
    params = {"is_active": True}
    response = requests.get(api, params=params)
    rows = [Select(value="", display_value="select sponsor")]
    for item in response.json():
        d = Select(value=item["id"], display_value=item["sponsor_name"])
        rows.append(d)
    return rows


def sponsor_activation(name_to_activ) -> bool:
    api = f"{base_url}/api/sponsors/{name_to_activ}/activate"
    response = requests.put(api)
    return True


def sponsor_deactivation(name_to_deact) -> bool:
    api = f"{base_url}/api/sponsors/{name_to_deact}/deactivate"
    response = requests.put(api)
    return True
