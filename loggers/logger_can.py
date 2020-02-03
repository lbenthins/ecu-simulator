import can
from loggers import logger_utils
from addresses import ECU_ADDRESSES, TARGET_ADDRESSES

LOG_TYPE = "can"

BUS_TYPE = "socketcan_native"

CAN_MASK = 0x7FF


def start():
    bus = create_can_bus()
    file_path = logger_utils.create_file_path(LOG_TYPE)
    while True:
        file_path = logger_utils.create_new_file_path_if_size_exceeded(file_path, LOG_TYPE)
        message = bus.recv()
        logger_utils.write_to_file(file_path, message.timestamp, message.arbitration_id, message.data)


def create_can_bus():
    return can.interface.Bus(channel=logger_utils.CAN_INTERFACE, bustype=BUS_TYPE, can_filters=get_filters())


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
