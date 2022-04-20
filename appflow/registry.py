from idom.backend import fastapi
from idom.backend.starlette import Options
from index import page as index_page

fastapi.configure(app, index_page, Options(redirect_root=False, url_prefix="/_idom"))
