import dominate as dm
from dominate import tags as tg


def base_html():
    """
    Create home page of TimeFlow.
    """
    doc = dm.document(title="TimeFlow", doctype="<!DOCTYPE html>")
    doc.head += tg.meta(charset="UTF-8")
    doc.head += tg.link(
        rel="css/styles.css", type="text/css", href="static/css/styles.css"
    )
    doc += tg.div(id="idom-app")
    return doc
