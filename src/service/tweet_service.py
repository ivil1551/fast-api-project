import time
from datetime import datetime

from src.config import config
from src.dao import dao
from src.utils import utils


def create_tweet(user_id: int, tweet: str):
    # initializing db connection
    db_obj = dao.AppDao()
    try:
        # validating tweet length constraints
        if not config.tweet_min_len <= len(tweet) <= config.tweet_max_len:
            return utils.get_response(
                content={'err_msg': f"Tweet should be {config.tweet_min_len} "
                                    f"to {config.tweet_max_len} character"},
                status_code=400)

        creation_time = time.time()
        insert_id = db_obj.insert_tweet(user_id=user_id, tweet=tweet, timestamp=creation_time)

        # validate db response
        if not isinstance(insert_id, int):
            # rollback if  failed to update any table or any exception raised
            db_obj.rollback_transaction()
            return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

        # commit transaction after successful db action
        db_obj.commit_transaction()
        utils.logger.info(f"method : Create Tweet - user id : {user_id} - status :200")
        return utils.get_response(
            content={'tweet_id': insert_id,
                     'created_timestamp': creation_time},
            status_code=200
        )
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)
    finally:
        # closes db connection
        db_obj.close_connection()
        del db_obj


def get_tweet(user_name: str, date: str):
    # initializing db connection
    db_obj = dao.AppDao()
    try:
        time_stamp = time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())
        tweets = db_obj.get_tweet(user_name=user_name, timestamp=time_stamp)

        # validate db response
        if not isinstance(tweets, list):
            return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

        tweets_lst = []
        if tweets:
            for tweet in tweets:
                tweets_lst.append({"tweet_id": tweet[0],
                                   "tweet": tweet[3],
                                   "created_timestamp": tweet[2]})

        utils.logger.info(f"method : Get Tweet - user name : {user_name} - status :200")
        return utils.get_response(
            content={"tweets_count": len(tweets_lst),
                     "tweets_list": tweets_lst},
            status_code=200
        )
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)
    finally:
        # closes db connection
        db_obj.close_connection()
        del db_obj


def delete_user_tweets(user_name: str):
    # initializing db connection
    db_obj = dao.AppDao()
    try:
        # gets all the tweets of a given user
        tweets = db_obj.get_tweet(user_name=user_name, timestamp=0)

        # validate db response
        if not isinstance(tweets, list):
            return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

        tweets_lst = []
        if tweets:
            deleted_tweets = db_obj.delete_tweet(user_name=user_name)
            if deleted_tweets != config.success_flag:
                # rollback if  failed to update any table or any exception raised
                db_obj.rollback_transaction()
                return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

            for tweet in tweets:
                tweets_lst.append({"tweet_id": tweet[0],
                                   "tweet": tweet[3]})

        # commit transaction on success
        db_obj.commit_transaction()
        utils.logger.info(f"method : Delete Tweet - user name : {user_name} - status :200")
        return utils.get_response(
            content={"deleted_tweets_count": len(tweets_lst),
                     "deleted_tweets_list": tweets_lst},
            status_code=200
        )

    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)
    finally:
        # closes db connection
        db_obj.close_connection()
        del db_obj
