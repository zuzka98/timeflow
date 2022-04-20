from array import array
from turtle import title
from typing import List
from idom import html, run, use_state, component, event, vdom
from idom.web import module_from_url, export
<<<<<<< HEAD:frontend/components/sidebar.py
from components.layout import Container
from config import get_user
from components.collapse import Collapse
from components.list_pages import ListPages

=======
>>>>>>> 436e9ff2b7745329386c30122c2e7d501bd54f64:uiflow/components/sidebar.py

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
def Sidebar(
    current_page,
    set_current_page,
    pages: List[str],
    isOpen,
    set_isOpen,
<<<<<<< HEAD:frontend/components/sidebar.py
=======
    user_role: str,
    logout,
    title: str = "",
>>>>>>> 436e9ff2b7745329386c30122c2e7d501bd54f64:uiflow/components/sidebar.py
    user_welcome: str = "",
    menu_items: object = {}
):
<<<<<<< HEAD:frontend/components/sidebar.py
    collapse, set_collapse = use_state(True)
    user_role = get_user()
    heading = 'Admin'
    btn_class = f"""text-nav text-left px-4 py-2 mt-2 text-nav rounded-lg focus:text-gray-900 focus:bg-active-sidebarfocus:outline-none focus:shadow-outline"""
    pages_dropdown = []
    for key, value in menu_items.items():
        pages_dropdown.append(value)
=======
    # user_role = get_user()
    h3Class = f"""text-nav text-left px-4 py-2 mt-2 text-nav rounded-lg focus:text-gray-900 focus:bg-active-sidebarfocus:outline-none focus:shadow-outline"""
    btn_class = f"""text-nav text-left px-4 py-2 mt-2 text-nav bg-transparent rounded-lg 
                focus:text-gray-900 hover:bg-active-sidebar focus:bg-active-sidebar
                focus:outline-none focus:shadow-outline
                """
>>>>>>> 436e9ff2b7745329386c30122c2e7d501bd54f64:uiflow/components/sidebar.py
    return html.div(
        {
            "class": mainDivClassOpen if isOpen else mainDivClass,
        },
        Container(
<<<<<<< HEAD:frontend/components/sidebar.py
            html.h1({"class": h1Class}, 'timeflow UI'),
            html.h3({"class": btn_class}, user_welcome),
=======
            html.h1({"class": h1Class}, title),
            html.h3({"class": h3Class}, user_welcome),
>>>>>>> 436e9ff2b7745329386c30122c2e7d501bd54f64:uiflow/components/sidebar.py
            html.nav(
                {"class": navClass},
                ListPages(
                    current_page, set_current_page, set_isOpen, pages=pages
                ),
                Collapse(heading, collapse, set_collapse)
                if (user_role == "admin" or user_role == None)
                else "",
                '' if collapse else ListPages(current_page, set_current_page, set_isOpen, pages=pages_dropdown) ,
            ),
            html.h3({"class": btn_class}, logout),
        ),
    )
