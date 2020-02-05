import os
import datetime
import ecu_config

CAN_INTERFACE = ecu_config.get_can_interface()

MAX_LOG_FILE_SIZE = 1500000  # bytes

LOG_FILE_NAME_FORMAT = "_%y%m%d%H%M%S.log"


def create_file_path(log_type):
    return os.path.join(os.path.dirname("ecu_simulator"), datetime.datetime.now().strftime(log_type + LOG_FILE_NAME_FORMAT))


def create_new_file_path_if_size_exceeded(file_path, log_type):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > MAX_LOG_FILE_SIZE:
            file_path = create_file_path(log_type)
    return file_path


def write_to_file(file_path, timestamp, address, data):
    log_file = open(file_path, "a")
    formatted_log = format_log(get_timestamp(timestamp), address, data)
    log_file.write(formatted_log)
    log_file.close()


def get_timestamp(timestamp):
    if timestamp is None:
        return create_timestamp()
    return to_iso8601(timestamp)


def create_timestamp():
    return str(datetime.datetime.now().isoformat(timespec="milliseconds"))


def to_iso8601(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp).isoformat(timespec="milliseconds"))


def format_log(timestamp, address, data):
    return timestamp + " " + CAN_INTERFACE + " " + hex(address) + " " + "0x" + data.hex() + "\n"


