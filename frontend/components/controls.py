from idom import component, html
from typing import Callable
from components.icons import filter, done, delete, batch_action, edit


tableActionsClass = 'flex items-center mr-9 py-3'


@component
def Button(is_disabled: bool, handle_submit: Callable, label: str):
    button_status = "text-gray-50  border-secondary-200"
    # if is_disabled is False:
    # button_status = "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200 hover:bg-gray-50 hover:text-primary-500"
    return html.div(
        {'class': "w-full my-2 flex justify-center md:w-auto md:flex-1 md:justify-start 2xl:flex-none 2xl:w-auto"},
        html.button(
            {
                "class": "py-3 px-4 border-[1px] text-sm border-button-bg bg-button-bg text-button-text rounded-[3px] w-[145px] flex items-center justify-center font-black tracking-wider",
                "onClick": handle_submit,
                "disabled": is_disabled,
            },
            label,
        )
    )


@component
def submit_button(handle_submit, *fields):
    """Create a submit button that is active when all given fields are filled out"""
    is_disabled = False
    for field in fields:
        if field == "":
            is_disabled = True
    btn = Button(is_disabled, handle_submit, label="Submit")
    return btn


def activation_button(name_to_activ, handle_activation):
    is_disabled = True
    if name_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation,
                 label="Activate")
    return btn


def deactivation_button(name_to_deact, handle_deactivation):
    is_disabled = True
    if name_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation,
                 label="Deactivate")
    return btn


@component
def TableActions():
    return html.div(
        {'class': 'flex items-center flex-wrap md:justify-start text-filter-name'},
        html.button(
            {'href': 'javascript:void(0)',
             'class': tableActionsClass, 'disabled': True},
            batch_action,
            html.span('Batch actions')
        ),
        html.button(
            {'href': 'javascript:void(0)',
             'class': tableActionsClass, 'disabled': True},
            filter,
            html.span('Filter')
        ),
        html.button(
            {'href': 'javascript:void(0)',
             'class': tableActionsClass, 'disabled': True},
            edit,
            html.span('Edit selected')
        ),
        html.button(
            {'href': 'javascript:void(0)',
             'class': tableActionsClass, 'disabled': True},
            delete,
            html.span('Delete')
        ),
        html.button(
            {'href': 'javascript:void(0)',
             'class': tableActionsClass, 'disabled': True},
            done,
            html.span('Done')
        )
    )
