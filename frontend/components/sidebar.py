from array import array
from turtle import title
from typing import List
from idom import html, run, use_state, component, event, vdom
from idom.web import module_from_url, export
from components.layout import Container
from config import get_user
from components.collapse import Collapse, ListPages


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
def Sidebar(
    current_page,
    set_current_page,
    pages: List[str],
    isOpen,
    set_isOpen,
    user_welcome: str = "",
    menu_items: array = []
):
    user_role = get_user()
    heading = 'Admin'
    btn_class = f"""text-nav text-left px-4 py-2 mt-2 text-nav rounded-lg focus:text-gray-900 focus:bg-active-sidebarfocus:outline-none focus:shadow-outline"""
    return html.div(
        {
            "class": mainDivClassOpen if isOpen else mainDivClass,
        },
        Container(
            html.h1({"class": h1Class}, 'timeflow UI'),
            html.h3({"class": btn_class}, user_welcome),
            html.nav(
                {"class": navClass},
                ListPages(
                    current_page, set_current_page, set_isOpen, pages=pages,
                ),
                Collapse(current_page, set_current_page,
                         set_isOpen, heading, menu_items)
                if (user_role == "admin" or user_role == None)
                else "",
            ),
        ),
    )
