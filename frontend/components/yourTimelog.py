from typing import Container
from idom import component, html, run, use_state
from components.layout import Container
from components.heading import H3
from components.input import SearchInput


@component
def YourTimelog():
    input_value, set_input_value = use_state('')
    return html.section(
        {'class': "py-6 xl:py-8"},
        html.div(
            {'class': 'flex flex-wrap justify-between items-center'},
            H3('Your Timelog'),
            SearchInput(input_value, set_input_value),
        )
    )
