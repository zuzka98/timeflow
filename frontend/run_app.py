import uvicorn
from idom.server import fastapi
from index import page as index_page

app = fastapi.create_development_app()

fastapi.configure(app, index_page)


def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        workers=1,
        access_log=True,
    )


run()
