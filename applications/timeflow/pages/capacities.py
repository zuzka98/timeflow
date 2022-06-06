from idom import html, use_state, component, event

from .utils import switch_state

from uiflow.components.input import Input, Selector2
from uiflow.components.layout import Row, Column, Container

from uiflow.components.table import SimpleTable
from uiflow.components.controls import Button

from ..data.common import year_month_dict_list
from ..data.capacities import (
    capacities_by_team,
    capacity_days,
    to_capacity,
    capacities_by_user_team_year_month,
    capacity_deletion,
    capacities_all,
    capacities_by_user,
    capacities_by_user_team,
    capacities_by_team,
)
from ..data.users import users_names
from ..data.teams import teams_id_name


@component
def page():
    """Creates a page for capacities"""
    user_id, set_user_id = use_state("")
    team_id, set_team_id = use_state("")
    year_month, set_year_month = use_state("")
    days, set_days = use_state("")
    is_event, set_is_event = use_state(False)
    return html.div(
        {"class": "w-full"},
        Row(
            create_capacity_form(
                user_id,
                set_user_id,
                team_id,
                set_team_id,
                year_month,
                set_year_month,
                days,
                set_days,
                is_event,
                set_is_event,
            ),
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(capacities_table(user_id, team_id)),
            ),
            Row(delete_capacity(is_event, set_is_event)),
        ),
    )


@component
def create_capacity_form(
    user_id,
    set_user_id,
    team_id,
    set_team_id,
    year_month,
    set_year_month,
    days,
    set_days,
    is_event,
    set_is_event,
):
    """Generates capacity form to submit capacities and filter capacity by month user and team"""

    @event(prevent_default=True)
    async def handle_submit(event):
        """
        schema:
        {
            "user_id": 0,
            "team_id": 0,
            "year": 0,
            "month": 0,
            "days": 0,
            "created_at": "2022-03-15T15:25:44.266Z",
            "updated_at": "2022-03-15T15:25:44.266Z",
            "is_locked": false
        }"""
        to_capacity(
            user_id=user_id,
            team_id=team_id,
            year_month=year_month,
            days=days,
        )
        switch_state(is_event, set_is_event)

    selector_user_id = Selector2(
        set_value=set_user_id,
        data=users_names(is_active=True),
        width="24%",
        md_width="24%",
    )

    selector_team_id = Selector2(
        set_value=set_team_id, data=teams_id_name(), width="24%", md_width="24%"
    )
    selector_year_month = Selector2(
        set_value=set_year_month,
        data=year_month_dict_list(),
        width="24%",
        md_width="24%",
    )

    selector_days = Selector2(
        set_value=set_days, data=capacity_days(), width="24%", md_width="24%"
    )

    is_disabled = True
    if user_id != "" and team_id != "" and year_month != "" and days != "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Submit")

    return Container(
        Column(
            Row(
                selector_user_id,
                selector_team_id,
                selector_year_month,
                selector_days,
                justify="justify-between",
            ),
            Row(btn),
        )
    )


@component
def capacities_table(user_id, team_id):
    """Generates a table component with capacity days by year month user and team"""
    if (user_id and team_id) != "":
        rows = capacities_by_user_team(user_id, team_id)
    elif user_id != "":
        rows = capacities_by_user(user_id)
    elif team_id != "":
        rows = capacities_by_team(team_id)
    else:
        rows = capacities_all()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_capacity(is_event, set_is_event):
    """Generates an input for capacity id to delete"""
    capacity_to_del, set_capacity_to_del = use_state("")

    def handle_delete(event):
        capacity_deletion(capacity_to_del)
        switch_state(is_event, set_is_event)

    inp_capacity = Input(
        set_value=set_capacity_to_del,
        label="capacity id to delete",
        width="full",
        md_width="full",
    )
    return Column(Row(inp_capacity), Row(Button(False, handle_delete, label="Delete")))
