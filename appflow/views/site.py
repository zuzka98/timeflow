from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from dominate import tags as tg


from .base import base_html

router = APIRouter()


@router.get("/site", response_class=HTMLResponse)
async def site():
    """
    Create home page of TimeFlow.
    """
    doc = base_html()
    doc.head += tg.script(type="module", src="static/js/site.js", defer=True)
    return doc.render()
