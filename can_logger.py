import can
import ecu_config_reader
import os
import datetime

LOG_FILE_NAME_FORMAT = 'can_%y%m%d%H%M%S.log'

MAX_LOG_FILE_SIZE = 1500000  # bytes

CAN_INTERFACE = ecu_config_reader.get_can_interface()

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
    ecu_can_ids = ecu_config_reader.get_ecu_addresses()
    tester_can_ids = []
    for ecu_can_id in ecu_can_ids:
        tester_can_ids.append(ecu_can_id+8)
    return ecu_can_ids + tester_can_ids


def create_file_path():
    return os.path.join(os.path.dirname(__file__), datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT))


def create_new_file_path_if_size_exceeded(log_file):
    if os.path.exists(log_file):
        if os.path.getsize(log_file) > MAX_LOG_FILE_SIZE:
            log_file = create_file_path()
    return log_file
