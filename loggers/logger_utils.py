import os
import datetime
import ecu_config

CAN_INTERFACE = ecu_config.get_can_interface()

MAX_LOG_FILE_SIZE = 1500000  # bytes

LOG_FILE_NAME_FORMAT = "_%y%m%d%H%M%S.log"


def create_new_file_path_if_size_exceeded(file_path, log_type):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > MAX_LOG_FILE_SIZE:
            file_path = create_file_path(log_type)
    return file_path


def create_file_path(log_type):
    return os.path.join(os.path.dirname("ecu_simulator"), datetime.datetime.now().strftime(log_type + LOG_FILE_NAME_FORMAT))
