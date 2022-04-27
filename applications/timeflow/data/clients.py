import requests
from ..config import base_url
from typing import List, TypedDict
from .common import Select
import json
from datetime import datetime

class Client(TypedDict):
    name: str
    is_active: bool
    created_at: str
    updated_at: str

def to_client(client_name: str,
    ) -> bool:
    data = Client(name=client_name,
    is_active=True,
    created_at=str(datetime.now()),
    updated_at=str(datetime.now())
)
    api=f"{base_url}/api/clients"    
    response = requests.post(api,
    data=json.dumps(dict(data)),
    headers={"accept": "application/json", "Content-Type": "application/json"},
    )


def clients_active() -> List[Select]:
    api = f"{base_url}/api/clients/active"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "id": item["id"],
            "name": item["name"],
        }
        rows.append(d)
    return rows

def clients_names() -> List[Select]:
    api_client_name = f"{base_url}/api/clients/active"
    response_client_name = requests.get(api_client_name)
    client_name_rows = [Select(value="", display_value="select client")]
    for item in response_client_name.json():
        d = Select(value=item["id"], display_value=item["name"])
        client_name_rows.append(d)
    return client_name_rows


def client_is_active(client_id, is_active) -> bool:
    api = f"{base_url}/api/clients/{client_id}"
    params = {"is_active": is_active}
    response= requests.put(api, params=params)
    return True

