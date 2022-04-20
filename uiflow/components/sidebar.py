from turtle import title
from typing import List
from idom import html, run, use_state, component, event, vdom
from idom.web import module_from_url, export
from .collapse import Collapse
from .list_pages import ListPages

from .layout import Container
from .icons import arrow_down, arrow_up

aClass = ("text-nav py-2 text-left",)
btnClass = "text-nav py-2 flex"
mainDivClass = (
    "hidden absolute w-screen  h-fit bg-header-bg z-10 xl:w-full xl:block xl:static xl:h-auto",
)
mainDivClassOpen = (
    "absolute w-screen h-fit min-h-screen bg-header-bg z-10 xl:w-full xl:block xl:static xl:h-auto",
)
h1Class = (
    "text-general-heading font-black uppercase text-xl font-black tracking-[2px] my-4",
)
navClass = "flex flex-col pb-4"


@component
def ListPages(
    current_page, set_current_page, set_isOpen, pages: List[str], title: str = ""
):
    def btn_class(btn_bg: str):
        btn_class = f"""text-nav text-left px-4 py-2 mt-2 text-nav bg-{btn_bg} rounded-lg 
                focus:text-gray-900 hover:bg-active-sidebar focus:bg-active-sidebar
                focus:outline-none focus:shadow-outline
                """
        return btn_class

    @event(prevent_default=True)
    def handle_click(event):
        set_current_page(event["target"]["value"])
        set_isOpen(False)

    anchors = []
    for page in pages:
        if page == current_page:
            btn_bg = "active-sidebar"
        else:
            btn_bg = "transparent"
        anchors.append(
            html.button(
                {
                    "class": btn_class(btn_bg),
                    "href": f"#{page}",
                    "value": page,
                    "onClick": handle_click,
                },
                page,
            )
        )

    return html.div({"class": "flex flex-col"}, anchors)


@component
def Sidebar(
    current_page,
    set_current_page,
    pages: List[str],
    isOpen,
    set_isOpen,
    user_role: str,
    logout,
    title: str = "",
    user_welcome: str = "",
    menu_items: object = {}
):
    # user_role = get_user()
    h3Class = f"""text-nav text-left px-4 py-2 mt-2 text-nav rounded-lg focus:text-gray-900 focus:bg-active-sidebarfocus:outline-none focus:shadow-outline"""
    btn_class = f"""text-nav text-left px-4 py-2 mt-2 text-nav bg-transparent rounded-lg 
                focus:text-gray-900 hover:bg-active-sidebar focus:bg-active-sidebar
                focus:outline-none focus:shadow-outline
                """

    collapse, set_collapse = use_state(True)
    heading = 'Admin'
    btn_class = f"""text-nav text-left px-4 py-2 mt-2 text-nav rounded-lg focus:text-gray-900 focus:bg-active-sidebarfocus:outline-none focus:shadow-outline"""
    pages_dropdown = []
    for key, value in menu_items.items():
        pages_dropdown.append(value)
    return html.div(
        {
            "class": mainDivClassOpen if isOpen else mainDivClass,
        },
        Container(
            html.h1({"class": h1Class}, title),
            html.h3({"class": h3Class}, user_welcome),
            html.nav(
                {"class": navClass},
                ListPages(
                    current_page, set_current_page, set_isOpen, pages=pages, title=title
                ),
                Collapse(heading, collapse, set_collapse)
                if (user_role == "admin" or user_role == None)
                else "",
                '' if collapse else ListPages(current_page, set_current_page, set_isOpen, pages=pages_dropdown) ,
            ),
            html.h3({"class": btn_class}, logout),
        ),
    )
