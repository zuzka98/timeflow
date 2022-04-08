import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from idom.server import fastapi
from idom.server.starlette import Options
from pathlib import Path
from index import page as index_page

app = fastapi.create_development_app()
HERE = Path(__file__).parent
print(HERE)
input()
app.mount("/static", StaticFiles(directory=str(HERE)), name="static")
app.mount()
fastapi.configure(app, index_page, Options(redirect_root=False, url_prefix="/_idom"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/login", response_class=HTMLResponse)
def test():
    return


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = ""
    pass


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
