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

from ..data.epics import epics_names
from ..data.epic_areas import (
    epic_area_activation,
    epic_area_deactivation,
    epic_areas_names_by_epic_id,
    get_active_epic_area_rows,
    post_epic_area,
    epic_areas_names,
    update_epic_area,
)
from .utils import switch_state


@component
def page():
    epic_id, set_epic_id = use_state("")
    name, set_name = use_state("")
    is_event, set_is_event = use_state(True)
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return html.div(
        {"class": "w-full"},
        Row(
            Container(
                create_epic_area_form(
                    epic_id,
                    set_epic_id,
                    name,
                    set_name,
                    is_event,
                    set_is_event,
                )
            ),
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(list_epic_areas(is_event)),
            ),
            Row(update_epic_areas(is_event, set_is_event)),
            Row(
                deactivate_epic_area(is_event, set_is_event),
                activate_epic_area(is_event, set_is_event),
            ),
        ),
    )


@component
def create_epic_area_form(epic_id, set_epic_id, name, set_name, is_event, set_is_event):
    """
    Create a form that allows admin to add a new epic area.

    post endpoint: /api/epic_areas
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
        """Call a post request for the given epic area when given event is triggered."""
        post_epic_area(epic_id, name)

        # Change the states
        switch_state(is_event, set_is_event)

    # Create dropdown of active epics which can then be selected
    selector_epic_id = Selector2(
        set_value=set_epic_id,
        data=epics_names(is_active=True),
        width="48%",
        md_width="48%",
    )

    # Create input field for the name of the epic area
    inp_name = Input(set_value=set_name, label="name", width="[48%]")

    # Create submit button
    btn = submit_button(handle_submit, epic_id, name)

    return html.div(
        {"class": "bg-filter-block-bg py-4 text-sm"},
        Column(
            Row(selector_epic_id, inp_name, justify="justify-between"),
            Row(btn),
        ),
    )


@component
def list_epic_areas(is_event):
    """
    Return rows consisting of each epic area along with its epic.

    Obtain a json response from a get request to the active epic areas endpoint.
    Store in rows the names of the epic and epic area, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    rows = get_active_epic_area_rows()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_epic_area(is_event, set_is_event):
    """Deactivate an epic area without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given epic area's active column to False."""
        epic_area_deactivation(name_to_deact)
        switch_state(is_event, set_is_event)

    # Create input field for id of epic area to be deactivated
    selector_deact_name = Selector2(
        set_name_to_deact,
        data=epic_areas_names(is_active=True, label="epic area to be deactivated"),
        width="96%",
        md_width="96%",
    )

    # Create the deactivation button
    is_disabled = True
    if name_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(selector_deact_name), Row(btn))


@component
def activate_epic_area(is_event, set_is_event):
    """Activate an epic area."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic area's active column to True."""
        epic_area_activation(name_to_activ)
        switch_state(is_event, set_is_event)

    # Create input field for name of epic area to be activated
    selector_act_name = Selector2(
        set_name_to_activ,
        data=epic_areas_names(is_active=False, label="epic area to be activated"),
        width="96%",
        md_width="96%",
    )

    # Create the activation button
    is_disabled = True
    if name_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(selector_act_name), Row(btn))


@component
def update_epic_areas(is_event, set_is_event):
    new_name, set_new_name = use_state("")
    new_epic_id, set_new_epic_id = use_state("")
    update_id, set_update_id = use_state("")

    @event(prevent_default=True)
    def handle_update(event):
        update_epic_area(
            id=update_id,
            new_name=new_name,
            new_epic_id=new_epic_id,
        )
        switch_state(value=is_event, set_value=set_is_event)

    epic_area_selector = Selector2(
        set_update_id,
        data=epic_areas_names(is_active=True, label="select epic area to update"),
        width="48%",
        md_width="48%",
    )

    epic_id_selector = Selector2(
        set_new_epic_id,
        data=epics_names(is_active=True, label="select new epic name"),
        width="48%",
        md_width="48%",
    )

    epic_area_name_input = Input(
        set_value=set_new_name,
        label="new epic area name",
        width="[48%]",
        md_width="[48%]",
    )
    is_disabled = False
    btn = Button(is_disabled, handle_update, label="Update")
    return Column(
        Row(epic_area_selector),
        Row(epic_id_selector, epic_area_name_input, justify="justify-between"),
        Row(btn),
    )
