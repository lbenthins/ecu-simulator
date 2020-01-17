import can
import ecu_config_reader

CAN_INTERFACE = ecu_config_reader.get_can_interface()

BUS_TYPE = "socketcan_native"

CAN_MASK = 0x7FF

LOGS_FILE_NAME = "can_logs.log"


def start():
    bus = can.interface.Bus(channel=CAN_INTERFACE, bustype=BUS_TYPE, can_filters=get_filters())
    while True:
        logger = can.Logger(LOGS_FILE_NAME, append=True)
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
