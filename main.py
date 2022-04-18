from imp import reload
from pathlib import Path
from os import path, set_inheritable, environ
from socket import herror

import uvicorn
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from idom.backend import fastapi
from idom.backend.starlette import Options


# Appflow Views
from appflow.views.index import router as index_router
from appflow.views.site import router as site_router
from appflow.views.timeflow import router as timeflow_router
from appflow.views.login_github import router as gh_login_router

# Applications
from applications.site.index import site_index
from applications.timeflow.index import timeflow


# Env Variables
SESSION_SECRET_KEY = 123

# Create the fastapi app
app = fastapi.create_development_app()

# Specify location of static files and specify middleware
HERE = Path(__file__).parent
STATIC_PATH = path.join("appflow", "static")
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")
app.add_middleware(SessionMiddleware, secret_key=str(SESSION_SECRET_KEY))

# IDOM Applications


fastapi.configure(app, site_index, Options(url_prefix="/_site"))
fastapi.configure(app, timeflow, Options(url_prefix="/_timeflow"))

app.include_router(site_router)
app.include_router(timeflow_router)

# FastAPI Views

app.include_router(gh_login_router)
app.include_router(index_router)
