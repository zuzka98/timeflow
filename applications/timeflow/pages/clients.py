from cProfile import label
import json
from idom import html, use_state, component, event
import requests
from datetime import datetime

from uiflow.components.input import Input, Selector2
from uiflow.components.layout import Row, Column, FlexContainer
from uiflow.components.table import SimpleTable, SubmitTable
from uiflow.components.controls import Button

from ..config import base_url
from ..data.clients import to_client, clients_active, client_is_active, clients_names

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
        to_client(name)
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
    rows = clients_active()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_client(is_event, set_is_event):
    del_client_id, set_del_client_id = use_state("")

    def handle_deactivation(event):
        client_is_active(client_id=del_client_id, is_active=False)
        switch_state(is_event, set_is_event)

    selector_deactivate_client = Selector2(
        set_del_client_id,
        data=clients_names(is_active=True, label="Client id to be deactivated"),
        width="96%",
        md_width="96%",
    )
    is_disabled = True
    if del_client_id != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(selector_deactivate_client), Row(btn))


@component
def activate_client(is_event, set_is_event):
    act_client_id, set_act_client_id = use_state("")

    def handle_activation(event):
        client_is_active(client_id=act_client_id, is_active=True)
        switch_state(is_event, set_is_event)

    selector_activate_client = Selector2(
        set_act_client_id,
        data=clients_names(is_active=False, label="Client id to be activated"),
        width="96%",
        md_width="96%",
    )
    is_disabled = True
    if act_client_id != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Deactivate")
    return Column(Row(selector_activate_client), Row(btn))
