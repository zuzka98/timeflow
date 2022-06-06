from applications.timeflow.pages.utils import switch_state
from idom import html, use_state, component, event
from idom.backend import fastapi
import requests
from datetime import datetime

from uiflow.components.input import Input, Selector2, InputDate
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable
from uiflow.components.controls import Button
from ..config import base_url

from ..data.teams import teams_id_name
from ..data.sponsors import sponsors_id_name, sponsor_names
from ..data.epics import (
    to_epic,
    epics_by_team_sponsor,
    epics_all,
    epics_names,
    epic_activate,
    epic_deactivate,
    update_epic,
)
from ..data.common import year_month_dict_list, days_in_month


@component
def page():
    short_name, set_short_name = use_state("")
    name, set_name = use_state("")
    team_id, set_team_id = use_state("")
    sponsor_id, set_sponsor_id = use_state("")
    start_date, set_start_date = use_state("")
    submitted_name, set_submitted_name = use_state("")
    deact_epic, set_deact_epic = use_state("")
    activ_epic, set_activ_epic = use_state("")
    is_event, set_is_event = use_state(True)
    return html.div(
        {"class": "w-full"},
        Row(
            Container(
                create_epic_form(
                    short_name,
                    set_short_name,
                    name,
                    set_name,
                    team_id,
                    set_team_id,
                    sponsor_id,
                    set_sponsor_id,
                    start_date,
                    set_start_date,
                    is_event,
                    set_is_event,
                ),
            ),
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(list_epics(team_id, sponsor_id, is_event)),
            ),
            Row(update_epics(is_event, set_is_event)),
            Row(
                deactivate_epic(is_event, set_is_event),
                activate_epic(is_event, set_is_event),
            ),
        ),
    )


@component
def create_epic_form(
    short_name,
    set_short_name,
    name,
    set_name,
    team_id,
    set_team_id,
    sponsor_id,
    set_sponsor_id,
    start_date,
    set_start_date,
    is_event,
    set_is_event,
):
    """Create a form that allows the admin to create a new epic
    post endpoint: /api/epics
    schema: {
        "id": 0,
        "short_name": "string",
        "name": "string",
        "team_id": 0,
        "sponsor_id": 0,
        "start_date": "2022-03-09",
        "is_active": true,
        "created_at": "2022-03-09T12:44:58.203Z",
        "updated_at": "2022-03-09T12:44:58.203Z"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        """Calls a post request for the given epic when given event is triggered."""
        to_epic(
            short_name=short_name,
            name=name,
            team_id=team_id,
            sponsor_id=sponsor_id,
            start_date=start_date,
            is_active=True,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
        )
        # Triggers state change
        switch_state(is_event, set_is_event)

    inp_short_name = Input(
        set_short_name,
        "Short epic's name",
        placeholder="",
        width="[14%]",
        md_width="[32%]",
    )
    inp_name = Input(
        set_name, "Full epic's name", placeholder="", width="[14%]", md_width="[32%]"
    )
    selector_team = Selector2(set_team_id, teams_id_name(), width="14%", md_width="32%")
    selector_sponsor = Selector2(
        set_sponsor_id, sponsors_id_name(), width="14%", md_width="32%"
    )
    input_date = InputDate(set_start_date)
    is_disabled = True
    if (
        short_name != ""
        and name != ""
        and team_id != ""
        and sponsor_id != ""
        and start_date != ""
    ):
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return html.div(
        {"class": "bg-filter-block-bg py-4 text-sm"},
        Column(
            Row(
                inp_short_name,
                inp_name,
                selector_team,
                selector_sponsor,
                input_date,
                justify="justify-between",
                wrap="flex-wrap",
            ),
            Row(btn),
        ),
    )


@component
def list_epics(team_id, sponsor_id, is_event):
    """Calls a list of epics filtered by selected team id and sponsor id"""
    rows = epics_all()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_epic(is_event, set_is_event):
    """Deactivate an epic without deleting it."""
    epic_to_deact, set_epic_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given epic's is_active column to False."""
        epic_deactivate(epic_to_deact)
        switch_state(is_event, set_is_event)

    inp_deact_epic = Selector2(
        set_epic_to_deact,
        data=epics_names(is_active=True, label="select epic to deactivate"),
        width="96%",
        md_width="96%",
    )

    is_disabled = True
    if epic_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(inp_deact_epic), Row(btn))


@component
def activate_epic(is_event, set_is_event):
    """Activate an inactivated epic"""
    epic_to_activ, set_epic_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic's is_active column to True."""
        epic_activate(epic_to_activ)
        switch_state(is_event, set_is_event)

    inp_activ_epic = Selector2(
        set_epic_to_activ,
        data=epics_names(is_active=False, label="select epic to activate"),
        width="96%",
        md_width="96%",
    )

    is_disabled = True
    if epic_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(inp_activ_epic), Row(btn))


@component
def update_epics(is_event, set_is_event):
    new_epic_name, set_new_epic_name = use_state("")
    new_short_name, set_new_short_name = use_state("")
    new_team_id, set_new_team_id = use_state("")
    new_sponsor_id, set_new_sponsor_id = use_state("")
    new_start_date, set_new_start_date = use_state("")
    update_epic_id, set_update_epic_id = use_state("")

    @event(prevent_default=True)
    def handle_update(event):
        update_epic(
            epic_id=update_epic_id,
            new_epic_name=new_epic_name,
            new_short_name=new_short_name,
            new_team_id=new_team_id,
            new_sponsor_id=new_sponsor_id,
            new_start_date=new_start_date,
        )
        switch_state(value=is_event, set_value=set_is_event)

    epic_selector = Selector2(
        set_update_epic_id,
        data=epics_names(is_active=True, label="select epic to update"),
        width="48%",
        md_width="48%",
    )

    epic_name_input = Input(
        set_new_epic_name,
        label="new epic name",
        width="[48%]",
        md_width="[48%]",
    )

    epic_short_name_input = Input(
        set_new_short_name,
        label="new epic short name",
        width="[48%]",
        md_width="[48%]",
    )

    team_selector = Selector2(
        set_new_team_id,
        data=teams_id_name(label="select new team"),
        width="48%",
        md_width="48%",
    )

    sponsor_selector = Selector2(
        set_new_sponsor_id,
        data=sponsor_names(is_active=True, label="select new sponsor"),
        width="48%",
        md_width="48%",
    )

    start_date_input = InputDate(set_new_start_date)

    is_disabled = False
    btn = Button(is_disabled, handle_update, label="Update")

    return Column(
        Row(epic_selector),
        Row(
            epic_name_input,
            epic_short_name_input,
            justify="justify-between",
        ),
        Row(sponsor_selector, team_selector, justify="justify-between"),
        Row(start_date_input),
        Row(btn),
    )
