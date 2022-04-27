from cProfile import label
import json
from idom import html, use_state, component, event
import requests
from datetime import datetime

from uiflow.components.input import Input
from uiflow.components.layout import Row, Column, FlexContainer
from uiflow.components.table import SimpleTable, SubmitTable
from uiflow.components.controls import Button

from ..config import base_url
from ..data.clients import client_is_active

from .utils import switch_state
@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    deleted_name, set_deleted_name = use_state("")
    is_event, set_is_event = use_state(True)
    return FlexContainer(
        Column(width="3/12"),
        Column(
            Row(
                create_client_form(name, set_name, set_submitted_name),
                bg="bg-filter-block-bg",
            ),
            Column(
                Row(list_clients(submitted_name)),
            ),
            Row(deactivate_client(is_event, set_is_event)),
            Row(activate_client(is_event, set_is_event)),
            width="6/12",
        ),
        Column(width="3/12"),
    )


@component
def create_client_form(name, set_name, set_submitted_name):
    """
        endpoint: /api/clients
        schema:
        {
      "name": "string",
      "active": True,
      "created_at": "2022-02-17T15:03:24.260Z",
      "updated_at": "2022-02-17T15:03:24.260Z"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {
            "name": name,
            "is_active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        print("here", data)
        response = requests.post(
            f"{base_url}/api/clients",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    inp_name = Input(set_value=set_name, label="name")
    is_disabled = True
    if name != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            inp_name,
        ),
        Row(btn),
    )


@component
def list_clients_by_name(rows):
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def list_clients(submitted_name):
    api = f"{base_url}/api/clients/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "id": item["id"],
            "name": item["name"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_client(set_deleted_name):
    client_id, set_client_id = use_state("")
    client_name, set_client_name = use_state("")

    def delete_client(event):
        api = f"{base_url}/api/clients/{client_id}?client_name={client_name}"
        response = requests.delete(api)
        set_deleted_name(client_name)

    inp_client_id = Input(set_value=set_client_id, label="delete client:id input")
    inp_client_name = Input(set_value=set_client_name, label="delete client:name input")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_client,
        },
        "Submit",
    )
    return Column(Row(inp_client_id, inp_client_name), Row(btn))

@component
def deactivate_client(is_event, set_is_event):
    del_client_id, set_del_client_id = use_state("")  
    def deactivate_client(event):
        client_is_active(client_id=del_client_id, is_active=False)
        switch_state(is_event, set_is_event)

    inp_deactivate_client = Input(set_value=set_del_client_id, label="Client id to be deactivated")
    btn = Button(False, deactivate_client, "Deactivate")
    return Column(inp_deactivate_client, btn)

@component
def activate_client(is_event, set_is_event):
    act_client_id, set_act_client_id = use_state("")  
    def activate_client(event):
        client_is_active(client_id=act_client_id, is_active=True)
        switch_state(is_event, set_is_event)

    inp_activate_client = Input(set_value=set_act_client_id, label="Client id to be activated")
    btn = Button(False, activate_client, "Activate")
    return Column(inp_activate_client, btn)
