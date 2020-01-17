import sys
from threading import Thread
import os
import obd_listener
import uds_listener
import can_logger
import ecu_config_reader as ecu_config


VCAN_SETUP_FILE = "vcan_setup.sh"

CAN_SETUP_FILE = "can_setup.sh"


def main():
    set_up_can_interface()
    star_can_loger_thread()
    start_obd_listener_thread()
    start_uds_listener_thread()


def set_up_can_interface():
    interface_type = ecu_config.get_can_interface_type()
    can_interface = ecu_config.get_can_interface()
    isotp_ko_file_path = ecu_config.get_isotp_ko_file_path()
    if interface_type == "virtual":
        os.system("sh " + VCAN_SETUP_FILE + " " + can_interface + " " + isotp_ko_file_path)
    elif interface_type == "hardware":
        can_bitrate = ecu_config.get_can_bitrate()
        os.system("sh " + CAN_SETUP_FILE + " " + can_interface + " " + can_bitrate + " " + isotp_ko_file_path)


def star_can_loger_thread():
    Thread(target=can_logger.start).start()


def start_obd_listener_thread():
    Thread(target=obd_listener.start).start()


def start_uds_listener_thread():
    Thread(target=uds_listener.start).start()


if __name__ == '__main__':
    sys.exit(main())
