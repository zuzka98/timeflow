from idom import component, html, run



@component
def H3(label, font="black"):
    return html.h3(
        {"class": f"font-{font} text-xs text-heading my-2 uppercase tracking-wider"},
        label,
    )
