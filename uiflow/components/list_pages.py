from idom import html, use_state, component, event
from typing import List
from turtle import title

@component
def ListPages(
    current_page, set_current_page, set_isOpen, pages: List[str]
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