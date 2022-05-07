from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth import jwt_token_generator
from src.utils import utils


def is_valid_token(token: str, request_body: dict)->bool:
    """
    Checks whether the given token match with the requester of the API
    """
    try:
        decoded_token = jwt_token_generator.is_valid_token(token)

        # checks whether the jwt token belongs to the user making the api call
        if decoded_token:
            # create tweet has input as user_id
            if "user_id" in request_body:
                return True if int(request_body["user_id"]) == decoded_token["user_id"] else False

            # delete tweet method has input as user_name
            if "user_name" in request_body:
                return True if request_body["user_name"] == decoded_token["user_name"] else False
        return False
    except Exception as ex:
        utils.print_error(ex)
        return False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        request_body = await request.json()
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not is_valid_token(credentials.credentials, request_body):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
