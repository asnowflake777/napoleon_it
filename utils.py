from typing import Tuple, List

import scrypt
from base64 import b64encode

from settings import SALT


def get_request_data(request_data, params: Tuple[str, ...]) -> List[str]:

    if isinstance(request_data, dict):
        result = [request_data.get(param) for param in params]
    else:
        result = [None for _ in params]

    return result


def encrypt_password(username: str, password: str) -> bytes:
    _password = password + SALT + username
    encrypted_password = scrypt.hash(_password, SALT)
    return b64encode(encrypted_password)
