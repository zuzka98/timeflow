from idom.server import fastapi


base_url = "http://fastapi:8002"


def get_role():
    """
    Return role of logged in user.
    """
    role = None
    session = fastapi.use_scope()["session"]
    role = session["role"]
    return role
