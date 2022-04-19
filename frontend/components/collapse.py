from idom import html, use_state, component, event
from typing import List
from turtle import title
from .icons import arrow_down, arrow_up
from components.list_pages import ListPages


@component
def Collapse(current_page, set_current_page, set_isOpen, heading, menu_items):
    is_down, set_value = use_state(True)

    def handle_click(event):
        if is_down:
            set_value(False)
        else:
            set_value(True)

    btn_class = """ flex text-nav text-left px-4 py-2 mt-2 text-nav rounded-lg 
                focus:text-gray-900 hover:bg-active-sidebar focus:bg-active-sidebar
                focus:outline-none focus:shadow-outline
                    """
    if is_down:
        btn = html.button(
            {
                "class": " w-full flex align-center text-nav py-2 text-left rounded-lg px-4 hover:bg-active-sidebar",
                "onClick": handle_click,
            },
            html.span(heading),
            arrow_down,
        )
        return html.div({"class": "relative"}, btn)
    else:
        btn = html.button(
            {
                "class": " w-full flex align-center text-nav py-2 text-left rounded-lg px-4 hover:bg-active-sidebar",
                "onClick": handle_click,
            },
            html.span(heading),
            arrow_up,
        )
        anchors = []
        pages = []
        for key, value in menu_items.items():
            anchors.append(html.a({"class": btn_class}, key)),
            pages.append(value)

        return html.div(
            {"class": "relative"},
            btn,
            html.div(
                {
                    "class": "right-0 w-full overflow-auto h-[60vh] mt-2 origin-top-right rounded-md shadow-lg"
                },
                html.div(
                    {
                        "class": "px-2 py-2 bg-white rounded-md shadow dark-mode:bg-gray-800"
                    },
                    ListPages(current_page, set_current_page,
                              set_isOpen, pages=pages),
                ),
            ),
        )






