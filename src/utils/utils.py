import logging
import os
from logging.handlers import RotatingFileHandler

from fastapi.responses import JSONResponse

from src.config import config

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
if not os.path.exists(config.logs_path):
    os.makedirs(config.logs_path)
handler = RotatingFileHandler(filename=os.path.join(config.logs_path, "main.log"),
                              maxBytes=5 * 1024 * 1024,
                              backupCount=5
                              )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_response(content, status_code):
    return JSONResponse(content=content, status_code=status_code)


def print_error(ex: Exception):
    filename = ex.__traceback__.tb_frame.f_code.co_filename
    line_number = ex.__traceback__.tb_lineno
    logger.error(f"Exception {ex} occurred in {filename} line no {line_number}")
