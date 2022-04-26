from idom import html, use_state, component, event
from .icons import arrow_down, arrow_up


@component
def Collapse(heading, collapse_class, collapse, set_collapse):
    

    def handle_click(event):
        set_collapse(not collapse)

    if collapse:
        btn = html.button(
            {
                "class": collapse_class,
                "onClick": handle_click,
            },
            html.span(heading),
            arrow_down,
        )
        return html.div({"class": "relative"}, btn)
    else:
        btn = html.button(
            {
                "class": collapse_class,
                "onClick": handle_click,
            },
            html.span(heading),
            arrow_up,
        )
        

        return html.div(
            {"class": "relative"},
            btn,
        )






