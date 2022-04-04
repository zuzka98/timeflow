from idom import component, html, run

h3Class = "font-black text-xs text-heading my-2 font-bold uppercase tracking-wider"


@component
def H3(label):
    return html.h3({'class': h3Class}, label)
