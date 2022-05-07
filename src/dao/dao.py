import mysql.connector

from src.config import config
from src.utils import utils


class AppDao:
    def __init__(self):
        # for application credentials will be passed from env or through secrets manager
        self.db_conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            port=config.port,
            database=config.database
        )
        self.db_conn.autocommit = False
        self.cursor = self.db_conn.cursor()

    def insert_tweet(self, user_id, tweet, timestamp):
        try:
            for table in config.tweets_tables:
                self.cursor.execute(f'insert into {table} (user_id, tweet, created_time) values (%s, %s, %s)',
                                    (user_id, tweet, timestamp))
            return self.cursor.lastrowid
        except Exception as ex:
            utils.print_error(ex)
            return ex

    # def async_insert_tweet(self, user_id, tweet, timestamp)):

    def get_tweet(self, user_name, timestamp):
        try:
            self.cursor.execute('select tweets_table.* from tweets_table left join user_table '
                                'on tweets_table.user_id = user_table.user_id where user_table.user_name '
                                'like %s and tweets_table.created_time>=%s',
                                (user_name, timestamp))
            data = self.cursor.fetchall()
            return data
        except Exception as ex:
            utils.print_error(ex)
            return ex

    def delete_tweet(self, user_name):
        try:
            for table in config.tweets_tables:
                self.cursor.execute(f'delete {table}.* from {table} left join user_table '
                                    f'on {table}.user_id = user_table.user_id where user_table.user_name '
                                    'like %s', (user_name,))
            return config.success_flag
        except Exception as ex:
            utils.print_error(ex)
            return ex

    def get_user_info(self, user_name):
        try:
            self.cursor.execute('select * from user_table where user_name=%s', (user_name,))
            data = self.cursor.fetchone()
            if data:
                return {"user_id": data[0],
                        "user_name": data[1],
                        "created_time": data[2]
                        }
            return {}
        except Exception as ex:
            utils.print_error(ex)
            return ex

    def insert_user(self, user_name, timestamp):
        try:
            self.cursor.execute('insert into user_table (user_name, created_time) values (%s, %s)',
                                (user_name, timestamp))
            return self.cursor.lastrowid
        except Exception as ex:
            utils.print_error(ex)
            return ex

    def close_connection(self):
        self.cursor.close()
        self.db_conn.close()

    def commit_transaction(self):
        self.db_conn.commit()

    def rollback_transaction(self):
        self.db_conn.rollback()
