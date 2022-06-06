from idom import html, use_state, component, event

from uiflow.components.controls import (
    activation_button,
    deactivation_button,
    submit_button,
    Button,
)
from uiflow.components.input import Input, Selector2
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable

from ..data.teams import (
    team_deactivation,
    team_activation,
    post_team,
    get_active_team_rows,
    teams_names,
)
from ..data.users import users_names


@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    short_name, set_short_name = use_state("")
    submitted_short_name, set_submitted_short_name = use_state("")
    lead_user_id, set_lead_user_id = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return html.div(
        {"class": "w-full"},
        Row(
            create_team_form(
                name,
                set_name,
                short_name,
                set_short_name,
                lead_user_id,
                set_lead_user_id,
                set_submitted_name,
                set_submitted_short_name,
            ),
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(list_teams(submitted_name, submitted_short_name)),
            ),
            Row(deactivate_team(set_deact_name)),
            Row(activate_team(set_activ_name)),
        ),
    )


@component
def create_team_form(
    name,
    set_name,
    short_name,
    set_short_name,
    lead_user_id,
    set_lead_user_id,
    set_submitted_name,
    set_submitted_short_name,
):
    """
    Create a form that allows admin to add a new team.

    post endpoint: /api/teams
    schema: {
        "epic_id": "int",
        "name": "string,
        "is_active": True
        "created_at": "2022-02-17T15:31:39.103Z",
        "updated_at": "2022-02-17T15:31:39.103Z"
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given team when given event is triggered."""
        post_team(name, short_name, lead_user_id)

        # Change the states
        set_submitted_name(name)
        set_submitted_short_name(short_name)

    # Create input field for the name of the team
    inp_name = Input(
        set_value=set_name, label="name of the team", width="[32%]", md_width="[32%]"
    )

    # Create input field for the short name of the team
    inp_short_name = Input(
        set_value=set_short_name,
        label="short name of the team",
        width="[32%]",
        md_width="[32%]",
    )

    # Create a dropdown of users which can then be selected
    selector_lead_user_id = Selector2(
        set_value=set_lead_user_id,
        data=users_names(is_active=True, label="select user lead"),
        width="32%",
        md_width="32%",
    )

    # Create submit button
    btn = submit_button(handle_submit, name, short_name, lead_user_id)

    return Container(
        Column(
            Row(
                inp_name,
                inp_short_name,
                selector_lead_user_id,
                justify="justify-between",
            ),
            Row(btn),
        )
    )


@component
def list_teams(submitted_name, submitted_short_name):
    """
    Return rows consisting of each team along with its leader (user).

    Obtain a json response from a get request to the users endpoint.
    Store in rows the names of the user and team, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    rows = get_active_team_rows()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_team(set_deact_name):
    """Deactivate a team without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given team's active column to False."""
        team_deactivation(name_to_deact)
        set_deact_name(name_to_deact)

    # Create selector field for name of team to be deactivated
    selector_team_deact = Selector2(
        set_name_to_deact,
        data=teams_names(is_active=True, label="team to be deactivated"),
        width="96%",
        md_width="96%",
    )

    # Create the deactivation button
    is_disabled = True
    if name_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(selector_team_deact), Row(btn))


@component
def activate_team(set_activ_name):
    """Activate a team."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic are'a active column to True."""
        team_activation(name_to_activ)
        set_activ_name(name_to_activ)

    # Create selector field for name of team to be activated
    selector_team_act = Selector2(
        set_name_to_activ,
        data=teams_names(is_active=False, label="team to be activated"),
        width="96%",
        md_width="96%",
    )

    # Create the activation button
    is_disabled = True
    if name_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(selector_team_act), Row(btn))
