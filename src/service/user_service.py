import time

from src.auth import jwt_token_generator
from src.config import config
from src.dao import dao
from src.utils import utils


def create_user(user_name: str):
    # initializing db connection
    db_obj = dao.AppDao()
    try:
        # validating tweet length constraints
        if not config.user_name_min_len <= len(user_name) <= config.user_name_max_len:
            return utils.get_response(
                content={
                    'err_msg': f"Username should be {config.user_name_min_len} to"
                               f" {config.user_name_max_len} character"},
                status_code=400)

        # returns dict of user data if user exist else return empty dict
        is_user_exist = db_obj.get_user_info(user_name=user_name)

        # to handle db related error
        if not isinstance(is_user_exist, dict):
            return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

        # checks whether the user with same username exist or not
        if is_user_exist:
            utils.logger.info(
                f"method : Create User - user name : {user_name} - status : 400 - msg : User exist already")
            return utils.get_response(content={'err_msg': "User already exist"}, status_code=400)

        creation_time = time.time()
        # insert user into db
        insert_id = db_obj.insert_user(user_name=user_name, timestamp=creation_time)

        # validate db related error
        if not isinstance(insert_id, int):
            return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

        # commit transaction after successful db action
        db_obj.commit_transaction()
        utils.logger.info(f"method : Create User - user name : {user_name} - status : 200")
        return utils.get_response(
            content={'user_id': insert_id,
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


def get_user_jwt_token(user_name: str):
    # initializing db connection
    db_obj = dao.AppDao()
    try:
        # returns dict of user data if user exist else return empty dict
        is_user_exist = db_obj.get_user_info(user_name=user_name)

        # to handle db related error
        if not isinstance(is_user_exist, dict):
            return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)

        # checks whether the user with same username exist or not
        if not is_user_exist:
            utils.logger.info(f"method : Get user token - user name : {user_name} - status : 400 - msg : User is "
                              f"invalid or doesn't exist")
            return utils.get_response(content={'err_msg': "User is invalid/doesn't exist"}, status_code=400)

        # Generating jwt token
        jwt_token = jwt_token_generator.generate_jwt_token(user_name=user_name,
                                                           user_id=int(is_user_exist['user_id']))
        utils.logger.info(f"method : Get user token - user name : {user_name} - status : 200")
        return utils.get_response(content={"token": jwt_token}, status_code=200)
    except Exception as ex:
        utils.print_error(ex)
        return utils.get_response(content={'err_msg': 'Something went wrong'}, status_code=400)
    finally:
        # closes db connection
        db_obj.close_connection()
        del db_obj
