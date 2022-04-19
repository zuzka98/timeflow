from email.mime import base
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from dominate import tags as tg

from .base import base_html

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def main():
    doc = base_html()
    ul = tg.ul()
    ul += tg.li(tg.a("Login into Timeflow", href="/redirect"))
    ul += tg.li(tg.a("Check out our very useful counter", href="/site"))
    doc += ul

    return doc.render()
