import logging
from logging import handlers
from loggers.logger_utils import MAX_LOG_FILE_SIZE

LOGGER_NAME = "ecu_simulator"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

LOGGER_FORMAT = "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s"

LOG_FILE_NAME = LOGGER_NAME + ".log"

logger = logging.getLogger(LOGGER_NAME)


def configure():
    formatter = logging.Formatter(LOGGER_FORMAT, datefmt=DATE_FORMAT)
    __add_file_handler(formatter)
    __add_console_handler(formatter)
    logger.setLevel(logging.DEBUG)


def __add_file_handler(formatter):
    fh = handlers.RotatingFileHandler(LOG_FILE_NAME, maxBytes=MAX_LOG_FILE_SIZE, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def __add_console_handler(formatter):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

