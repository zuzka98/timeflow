from idom import html, use_state, component


@component
def site_index():

    index, set_index = use_state(0)

    def handle_click(event):
        set_index(index + 1)

    return html.div(
        html.p(f"The Count Is {index}"), html.button({"onClick": handle_click}, "Add 1")
    )
