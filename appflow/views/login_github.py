import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends, Request
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from dominate import tags as tg

router = APIRouter()

# Load in env variables
load_dotenv()

# to be removed and replaced with docker-compose-dev
TIMEFLOW_DEV = os.getenv("TIMEFLOW_DEV")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"


@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    request.session.pop("role")
    return "You Logged Out"


@router.get("/redirect", response_class=RedirectResponse)
async def login(request: Request):
    """
    Redirect user to GitHub for authentication.
    Future: Implement button that user clicks to cause the redirection.
    """

    github = OAuth2Session(GITHUB_CLIENT_ID, scope=["read:org", "read:user"])

    # Redirect user to GitHub for authorization
    authorization_url, state = github.authorization_url(authorization_base_url)
    request.session["oauth_state"] = state
    return authorization_url


@router.get("/callback", response_class=RedirectResponse)
async def callback(request: Request):
    """
    Fetch token of user and redirect to subdirectory /organizations.
    """
    github = OAuth2Session(GITHUB_CLIENT_ID, state=request.session["oauth_state"])
    authorization_response = str(request.url)

    # Convert authorization_reponse url to return with https
    if TIMEFLOW_DEV != "true":
        authorization_response = str(request.url)[:4] + "s" + str(request.url)[4:]
    token = github.fetch_token(
        token_url,
        client_secret=GITHUB_CLIENT_SECRET,
        authorization_response=authorization_response,
    )
    request.session["oauth_token"] = token
    organizations_url = f"{str(request.base_url)}organizations"
    return organizations_url


@router.get("/organizations", response_class=RedirectResponse)
async def organizations(request: Request):
    """
    Fetch organizations of user and determine role.
    """
    github = OAuth2Session(
        GITHUB_CLIENT_ID,
        token=request.session["oauth_token"],
        state=request.session["oauth_state"],
    )

    github_api = github.get("https://api.github.com/user").json()
    username = github_api["login"]
    request.session["username"] = username

    # Use dyvenia api with user's username to check if user is in team
    dyvenia_api = github.get(
        f"https://api.github.com/organizations/81221495/team/4777989/members/{username}"
    )

    # Give admin permissions to user if app is ran in dev mode
    if TIMEFLOW_DEV == "true":
        request.session["role"] = "admin"
        return f"{str(request.base_url)}timeflow"

    # User not dyvenia's core team
    if dyvenia_api.status_code == 404:
        return str(request.base_url)
    # User in dyvenia's core team
    elif dyvenia_api.status_code == 204:
        # Check if user is in the GitHub TimeFlow Admin Team
        admin_team = github.get(
            f"https://api.github.com/organizations/81221495/team/5925377/members/{username}"
        )

        if admin_team.status_code == 404:
            request.session["role"] = "user"
        elif admin_team.status_code == 204:
            request.session["role"] = "admin"

        return f"{str(request.base_url)}home"
