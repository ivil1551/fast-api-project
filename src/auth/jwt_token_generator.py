import time

import jwt

from src.config import config
from src.utils import utils


# function used for signing the JWT string
def generate_jwt_token(user_name: str, user_id: int):
    payload = {
        "user_name": user_name,
        "user_id": user_id,
        "expiration_time": time.time() + config.jwt_token_validity
    }
    return jwt.encode(payload, key=config.jwt_secret_key, algorithm=config.jwt_hashing_algorithm)


def is_valid_token(token: str):
    try:
        decoded_token = jwt.decode(token, key=config.jwt_secret_key, algorithms=[config.jwt_hashing_algorithm])
        return decoded_token if decoded_token["expiration_time"] >= time.time() else None
    except Exception as ex:
        utils.print_error(ex)
        return None
