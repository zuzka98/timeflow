from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from dominate import tags as tg
from .base import base_html

router = APIRouter()


def get_user(request: Request):
    try:
        return request.session["role"]
    except KeyError:
        return "not authorized to see this page"


@router.get("/timeflow", response_class=HTMLResponse, dependencies=[Depends(get_user)])
async def site(request: Request):
    """
    Create home page of TimeFlow.
    """
    doc = base_html()
    doc.head += tg.script(type="module", src="static/js/timeflow.js", defer=True)
    return doc.render()
