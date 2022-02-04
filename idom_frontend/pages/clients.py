import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
import requests
from sanic import Sanic, response

from components.input import Input
from components.layout import Row, Column, Container, FlexContainer
from components.lists import ListSimple
from components.table import SimpleTable

base_url = "http://127.0.0.1:8000"


@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    deleted_name, set_deleted_name = use_state("")
    is_changed, set_is_changed = use_state(False)

    return FlexContainer(
        Column(width="3/12"),
        Column(
            create_client_form(name, set_name, set_submitted_name),
            Column(
                Row(list_clients(submitted_name, is_changed)),
            ),
            Row(delete_client(is_changed, set_is_changed)),
            width="6/12",
        ),
        Column(width="3/12"),
    )


@component
def create_client_form(name, set_name, set_submitted_name):
    """
    endpoint: /api/clients
    schema: {
      "name": "string",
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {"name": name}
        print("here", data)
        response = requests.post(
            f"{base_url}/api/clients",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    inp_name = Input(value=name, set_value=set_name, label="name")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            inp_name,
        ),
        Row(btn),
    )


@component
def list_clients(name, is_changed):
    api = f"{base_url}/api/clients"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "id": item["id"],
            "name": item["name"],
        }
        rows.append(d)
    return SimpleTable(rows=rows)


@component
def delete_client(deleted_name, set_deleted_name):
    client_id, set_client_id = use_state("")
    client_name, set_client_name = use_state("")

    def delete_client(event):
        api = f"{base_url}/api/clients/{client_id}?client_name={client_name}"
        response = requests.delete(api)
        set_deleted_name(client_name)
        # set_is_changed(True)

    inp_client_id = Input(
        value=client_id, set_value=set_client_id, label="delete client:id input"
    )
    inp_client_name = Input(
        value=client_name, set_value=set_client_name, label="delete client:name input"
    )
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_client,
        },
        "Submit",
    )
    return Column(Row(inp_client_id, inp_client_name), Row(btn))
