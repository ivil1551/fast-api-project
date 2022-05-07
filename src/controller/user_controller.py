from fastapi import APIRouter

from src.models import models
from src.service import user_service
from src.utils import utils

user_router = APIRouter()


@user_router.post("/create")
async def create_user(body: models.CreateUser):
    """
    To Create user

    HTTP method : POST
    Endpoint : /api/v1/user/create
    """
    try:
        return user_service.create_user(user_name=body.user_name)
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=500)


@user_router.get("/token")
async def get_user_jwt_token(user_name: str):
    """
    To Get JWT token

    HTTP method : GET
    Endpoint : /api/v1/user/token?user_name=""
    """
    try:
        return user_service.get_user_jwt_token(
            user_name=user_name
        )
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=500)
