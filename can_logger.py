import can
import ecu_config
import os
import datetime
from addresses import ECU_ADDRESSES, TARGET_ADDRESSES

LOG_FILE_NAME_FORMAT = "can_%y%m%d%H%M%S.log"

MAX_LOG_FILE_SIZE = 1500000  # bytes

CAN_INTERFACE = ecu_config.get_can_interface()

BUS_TYPE = "socketcan_native"

CAN_MASK = 0x7FF


def start():
    bus = can.interface.Bus(channel=CAN_INTERFACE, bustype=BUS_TYPE, can_filters=get_filters())
    log_file = create_file_path()
    while True:
        log_file = create_new_file_path_if_size_exceeded(log_file)
        logger = can.Logger(log_file, append=True)
        logger.on_message_received(bus.recv())
        logger.stop()


def get_filters():
    filters = []
    for can_id in get_can_ids():
        filters.append({"can_id": can_id, "can_mask": CAN_MASK, "extended": False})
    return filters


def get_can_ids():
    can_ids = []
    can_ids.extend(ECU_ADDRESSES)
    can_ids.extend(TARGET_ADDRESSES)
    return can_ids


def create_new_file_path_if_size_exceeded(file_path):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > MAX_LOG_FILE_SIZE:
            file_path = create_file_path()
    return file_path


def create_file_path():
    return os.path.join(os.path.dirname(__file__), datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT))
