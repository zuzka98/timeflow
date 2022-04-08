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
        if header[0] == "b'authorization'":
            # Isolate the hash from the rest of the string
            hashed_auth = header[1].replace("'", "").split(" ")[1]
            # Decode the hashed authentication
            auth = base64.b64decode(hashed_auth)
            # Pattern to isolate role
            pattern = re.compile(r"[a-zA-Z]+")
            role = pattern.match(auth, re.IGNORECASE).group()
            print(role)
            return role
