import logging
from logging import handlers
import logger_utils
from logger_utils import MAX_LOG_FILE_SIZE

LOGGER_NAME = 'ecu_simulator'

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger = logging.getLogger(LOGGER_NAME)


def configure():
    formatter = logging.Formatter(LOGGER_FORMAT)
    __add_file_handler(formatter)
    __add_console_handler(formatter)
    logger.setLevel(logging.DEBUG)


def __add_file_handler(formatter):
    fh = handlers.RotatingFileHandler(logger_utils.create_file_path(LOGGER_NAME), maxBytes=MAX_LOG_FILE_SIZE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def __add_console_handler(formatter):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

