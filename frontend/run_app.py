import uvicorn
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from idom.server import fastapi
from idom.server.starlette import Options
from pathlib import Path
from requests_oauthlib import OAuth2Session
from starlette.middleware.sessions import SessionMiddleware

from index import page as index_page

app = fastapi.create_development_app()

HERE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(HERE)), name="static")
app.add_middleware(SessionMiddleware, secret_key="123")

fastapi.configure(app, index_page, Options(redirect_root=False, url_prefix="/_idom"))

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

client_id = "a3dd4c8a1bc07ca5d347"
client_secret = "d8ce2b6d5d788b816c9ddf5e1fd9801a29e60139"

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"


@app.get("/", response_class=RedirectResponse)
async def main(request: Request):
    """
    Redirect to login page.
    """
    login_url = f"{str(request.url)}login"
    return login_url


@app.get("/login", response_class=RedirectResponse)
async def login(request: Request):
    """
    Redirect user to GitHub for authentication.
    Future: Implement button that user clicks to cause the redirection.
    """

    github = OAuth2Session(client_id, scope=["read:org", "read:user"])

    # Redirect user to GitHub for authorization
    authorization_url, state = github.authorization_url(authorization_base_url)
    request.session["oauth_state"] = state
    return authorization_url


@app.get("/callback", response_class=RedirectResponse)
async def callback(request: Request):
    """
    Fetch token of user and redirect to subdirectory /organizations.
    """
    github = OAuth2Session(client_id, state=request.session["oauth_state"])
    token = github.fetch_token(
        token_url, client_secret=client_secret, authorization_response=str(request.url)
    )
    request.session["oauth_token"] = token
    organizations_url = f"{str(request.base_url)}organizations"
    return organizations_url


@app.get("/organizations", response_class=RedirectResponse)
async def organizations(request: Request):
    """
    Fetch organizations of user and determine role.
    """
    github = OAuth2Session(
        client_id,
        token=request.session["oauth_token"],
        state=request.session["oauth_state"],
    )

    github_api = github.get("https://api.github.com/user").json()
    username = github_api["login"]

    # Use dyvenia api with user's username to check if user is in team
    dyvenia_api = github.get(
        f"https://api.github.com/organizations/81221495/team/4777989/members/{username}"
    )

    # User not dyvenia's core team
    if dyvenia_api.status_code == 404:
        return request.base_url
    # User in dyvenia's core team
    elif dyvenia_api.status_code == 204:
        # Check if user is in the GitHub TimeFlow Admin Team
        admin_team = github.get(
            f"https://api.github.com/organizations/81221495/team/5925377/members/{username}"
        )
        print("admin_team", admin_team)
        if admin_team == 404:
            request.session["role"] = "user"
            return f"{str(request.url)}home"
        elif admin_team == 204:
            request.session["role"] = "admin"
            return f"{str(request.url)}home"


@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    role = request.session["role"]
    with open("index.html", "r") as f:
        html = f.read()
    return html
    # dominate html


def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        workers=1,
        access_log=True,
    )


run()
