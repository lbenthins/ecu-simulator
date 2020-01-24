import sys
from threading import Thread
import os
import obd_listener
import uds_listener
import can_logger
import isotp_logger
import ecu_config
import ecu_simulator_logger as logging

VCAN_SETUP_FILE = "vcan_setup.sh"

CAN_SETUP_FILE = "can_setup.sh"


def main():
    logging.configure()
    logging.logger.info("Starting ECU-Simulator")
    set_up_can_interface()
    star_can_logger_thread()
    star_isotp_logger_thread()
    start_obd_listener_thread()
    start_uds_listener_thread()


def set_up_can_interface():
    interface_type = ecu_config.get_can_interface_type()
    can_interface = ecu_config.get_can_interface()
    isotp_ko_file_path = ecu_config.get_isotp_ko_file_path()
    if interface_type == "virtual":
        logging.logger.info("Setting up virtual CAN interface: " + can_interface)
        os.system("sh " + VCAN_SETUP_FILE + " " + can_interface + " " + isotp_ko_file_path)
    elif interface_type == "hardware":
        logging.logger.info("Setting up CAN interface: " + can_interface)
        logging.logger.info("Loading ISO-TP module from: " + isotp_ko_file_path)
        os.system("sh " + CAN_SETUP_FILE + " " + can_interface + " " + ecu_config.get_can_bitrate() + " " + isotp_ko_file_path)


def star_can_logger_thread():
    Thread(target=can_logger.start).start()


def star_isotp_logger_thread():
    Thread(target=isotp_logger.start).start()


def start_obd_listener_thread():
    Thread(target=obd_listener.start).start()


def start_uds_listener_thread():
    Thread(target=uds_listener.start).start()


if __name__ == '__main__':
    sys.exit(main())
