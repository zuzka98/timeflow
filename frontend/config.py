import base64
import re
from idom.server import fastapi


base_url = "http://fastapi:8002"


def role():
    """
    Return role of logged in user.
    """
    headers = fastapi.use_scope()["headers"]
    role = None
    for header in headers:
        if header[0].decode("utf-8") == "authorization":
            # Convert byte object to string
            header_auth_str = header[1].decode("utf-8")
            # Isolate the hash from the rest of the string
            hashed_auth = header_auth_str.split(" ")[1]
            # Decode the hashed authentication
            auth = base64.b64decode(hashed_auth).decode("utf-8")
            # Isolate role
            role = auth.split(":")[0]
            return role
    return role
