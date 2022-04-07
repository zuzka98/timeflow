import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from idom.server import fastapi
from idom.server.starlette import Options
from pathlib import Path
from index import page as index_page

app = fastapi.create_development_app()
HERE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(HERE)), name="static")
fastapi.configure(app, index_page, Options(redirect_root=False))


def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        workers=1,
        access_log=True,
    )


run()
