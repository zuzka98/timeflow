from idom import html, use_state, component, event
from idom.backend import fastapi
import requests
from datetime import datetime
from uiflow.components.input import (
    Input,
    Selector2,
    display_value,
)
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable
from uiflow.components.controls import Button
from uiflow.components.heading import H3, H4
from uiflow.components.input import InputDateTime

from ..data.common import (
    username,
)

from ..data.epics import epics_names
from ..data.epic_areas import epic_areas_names_by_epic_id
from ..data.timelogs import to_timelog, timelog_by_user_id_month, timelogs_all_by_month
from ..data.users import get_user_id_by_username

from ..config import base_url
from uiflow.components.controls import TableActions
from uiflow.components.yourTimelog import YourTimelog
from .utils import switch_state


@component
def page(app_role: str, github_username: str):
    """
    Timelogs page.

    Parameters
    ----------
    app_role: str
        Role of user within the app.
    github_username: str
        GitHub username of user.
    """
    user_id, set_user_id = use_state("")
    epic_id, set_epic_id = use_state("")
    epic_area_id, set_epic_area_id = use_state("")
    is_event, set_is_event = use_state(True)
    start_datetime, set_start_datetime = use_state("")
    end_datetime, set_end_datetime = use_state("")
    deleted_timelog, set_deleted_timelog = use_state("")
    post_response, set_post_response = use_state("")

    admin = True if app_role == "admin" or app_role == None else False

    return html.div(
        {"class": "w-full"},
        Row(
            Container(
                create_timelog_form(
                    user_id,
                    set_user_id,
                    epic_id,
                    set_epic_id,
                    epic_area_id,
                    set_epic_area_id,
                    start_datetime,
                    set_start_datetime,
                    end_datetime,
                    set_end_datetime,
                    is_event,
                    set_is_event,
                    admin,
                    github_username,
                    post_response,
                    set_post_response,
                ),
            ),
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(
                    timelogs_table(
                        user_id, is_event, admin, github_username, start_datetime
                    )
                ),
            ),
            delete_timelog_input(set_deleted_timelog, admin, github_username),
        ),
    )


@component
def create_timelog_form(
    user_id,
    set_user_id,
    epic_id,
    set_epic_id,
    epic_area_id,
    set_epic_area_id,
    start_datetime,
    set_start_datetime,
    end_datetime,
    set_end_datetime,
    is_event,
    set_is_event,
    admin,
    github_username,
    post_response,
    set_post_response,
):
    """
    schema:
    {
    "user_id": 0,
    "start_time": "string",
    "end_time": "string",
    "epic_id": 0,
    "epic_area_id": 0,
    "count_hours": 0,
    "count_days": 0,
    "month": 0,
    "year": 0
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        year = start_datetime[0:4]
        month = start_datetime[5:7]

        start_time_post = start_datetime.replace("T", " ")
        end_time_post = end_datetime.replace("T", " ")
        response = to_timelog(
            start_time=start_time_post,
            end_time=end_time_post,
            user_id=user_id,
            epic_id=epic_id,
            epic_area_id=epic_area_id,
            month=month,
            year=year,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
        )
        set_post_response(response)
        switch_state(is_event, set_is_event)
        return response

    if admin == True:
        selector_user = Selector2(
            set_value=set_user_id,
            data=username(),
            set_sel_value=set_post_response,
            sel_value="",
        )
    elif admin == False:
        user_id = get_user_id_by_username(github_username)
        selector_user = display_value(user_id, github_username)

    selector_epic_id = Selector2(
        set_value=set_epic_id,
        set_sel_value=set_epic_area_id,
        sel_value="",
        set_sel_value2=set_post_response,
        sel_value2="",
        data=epics_names(is_active=True),
        width="14%",
        md_width="32%",
    )

    selector_epic_area_id = Selector2(
        set_value=set_epic_area_id,
        set_sel_value=set_post_response,
        sel_value="",
        data=epic_areas_names_by_epic_id(epic_id),
        width="14%",
        md_width="32%",
    )
    h_start = H3("from:", "bold")
    input_start_datetime = InputDateTime(
        set_start_datetime,
        set_sel_value=set_post_response,
        sel_value="",
    )
    h_end = H3("to:", "bold")
    input_end_datetime = InputDateTime(
        set_end_datetime,
        set_sel_value=set_post_response,
        sel_value="",
    )
    is_disabled = True
    if (
        admin == True
        and user_id != ""
        and epic_id != ""
        and epic_area_id != (0 or "")
        and start_datetime != ""
        and end_datetime != ""
    ):
        is_disabled = False
    elif (
        admin == False
        and epic_id != ""
        and epic_area_id != (0 or "")
        and start_datetime != ""
        and end_datetime != ""
    ):
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")
    return html.section(
        {"class": "bg-filter-block-bg py-4 text-sm"},
        Container(
            H3("Select timelog"),
            html.div(
                {
                    "class": "flex flex-wrap justify-between items-center md:justify-start 2xl:justify-between"
                },
                selector_user,
                selector_epic_id,
                selector_epic_area_id,
                h_start,
                input_start_datetime,
                h_end,
                input_end_datetime,
                btn,
            ),
            H4(post_response),
        ),
    )


@component
def timelogs_table(user_id, is_event, admin, github_username, start_datetime):
    """
    Returns a table component by current month

    Parameters
    ----------
    user_id: int
        Id of current or selected user
    is_event:
        Triggers table appearance while filtering
    app_role: str
        Role of user within the app.
    github_username: str
        GitHub username of user.
    """
    month = datetime.now().month
    if admin == False:
        user_id = get_user_id_by_username(github_username)
    if user_id != "":
        rows = timelog_by_user_id_month(user_id, month)
    else:
        if start_datetime != "":
            select_month = start_datetime[5:7]
        else:
            select_month = month
        rows = timelogs_all_by_month(select_month)
    return html.div(
        {"class": "w-full"}, YourTimelog(), TableActions(), SimpleTable(rows=rows)
    )


@component
def delete_timelog_input(set_deleted_timelog, admin, github_username):
    timelog_to_delete, set_timelog_to_delete = use_state("")
    """
    Delete a timelog by selected timelog id. 
    User can delete only his own timelogs (validation by user id)
    """

    def handle_delete(event):
        api = f"{base_url}/api/timelogs/{timelog_to_delete}"
        if admin:
            params = None
        else:
            user_id = get_user_id_by_username(github_username)
            params = {"user_id": user_id}
        response = requests.delete(api, params=params)
        set_deleted_timelog(timelog_to_delete)

    inp_username = Input(
        set_value=set_timelog_to_delete, label="timelog id to delete", width="full"
    )

    return Column(Row(inp_username), Button(False, handle_delete, "Submit"))
