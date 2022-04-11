import requests
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from idom.server import fastapi
from idom.server.starlette import Options
from pathlib import Path
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from index import page as index_page

app = fastapi.create_development_app()
app.add_middleware(SessionMiddleware, secret_key="!secret")

HERE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(HERE)), name="static")
app.mount()
fastapi.configure(app, index_page, Options(redirect_root=False, url_prefix="/_idom"))

config = Config(".env")


# tokenUrl declares URL that frontend sends username and password to
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/login", response_class=HTMLResponse)
def test():

    return


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = requests
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/test", response_class=HTMLResponse)
def test():
    with open("index.html", "r") as f:
        html = f.read()
    return html


def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        workers=1,
        access_log=True,
    )


run()
