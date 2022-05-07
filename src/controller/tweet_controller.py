import datetime

from fastapi import APIRouter, Depends

from src.auth.jwt_token_validator import JWTBearer
from src.models import models
from src.service import tweet_service
from src.utils import utils

tweet_router = APIRouter()


@tweet_router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_tweet(body: models.CreateTweet):
    """
    To Create tweet

    HTTP method : POST
    Endpoint : /api/v1/tweet/create
    """
    try:
        return tweet_service.create_tweet(user_id=body.user_id, tweet=body.tweet)
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=500)


@tweet_router.get("", tags=["Enter date as yyyy-mm-dd"])
async def get_tweet(user_name: str, date: datetime.date):
    """
     To Get tweet

     HTTP method : GET
     Endpoint : /api/v1/tweet?user_name=""&date=""
    """
    try:
        return tweet_service.get_tweet(user_name=user_name, date=str(date))
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=500)


@tweet_router.delete("", dependencies=[Depends(JWTBearer())])
async def delete_user_tweets(body: models.DeleteTweet):
    """
     To delete tweet

     HTTP method : DELETE
     Endpoint : /api/v1/tweet
    """
    try:
        return tweet_service.delete_user_tweets(user_name=body.user_name)
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=500)
