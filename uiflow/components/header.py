from idom import component, html, use_state

from .sidebar import Sidebar


@component
<<<<<<< HEAD:frontend/components/header.py
def Header(current_page, set_current_page, pages, title, user_welcome, menu_items):
=======
def Header(current_page, set_current_page, pages, user_role, title, user_welcome):
>>>>>>> 436e9ff2b7745329386c30122c2e7d501bd54f64:uiflow/components/header.py

    isOpen, set_isOpen = use_state(False)

    def handleOpenSidebar(event):
        set_isOpen(not isOpen)

    return html.div(
        html.header(
            {
                "class": "bg-header-bg fixed z-10 top-0 w-full xl:w-60 xl:h-screen xl:px-6 xl:fixed"
            },
            html.div(
                {"class": "w-full px-4 flex justify-between items-center py-4 xl:py-6"},
                html.img({"src": "../static/img/svg/logo.svg"}),
                html.a(
                    {
                        "href": "javascript:void(0)",
                        "class": "xl:hidden",
                        "onClick": handleOpenSidebar,
                    },
                    html.img({"src": "../static/img/svg/Burger.svg", "class": "w-8"}),
                ),
            ),
            Sidebar(
                current_page,
                set_current_page,
                pages,
                isOpen,
                set_isOpen,
<<<<<<< HEAD:frontend/components/header.py
=======
                user_role,
                html.a({"href": "/logout"}, "Log Out"),
                title,
>>>>>>> 436e9ff2b7745329386c30122c2e7d501bd54f64:uiflow/components/header.py
                user_welcome,
                menu_items
            ),
        )
    )
