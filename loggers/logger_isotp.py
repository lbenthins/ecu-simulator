import isotp
import time
from loggers import logger_utils
from loggers.logger_utils import CAN_INTERFACE
from addresses import UDS_ECU_ADDRESS, UDS_TARGET_ADDRESS
from addresses import OBD_BROADCAST_ADDRESS, OBD_ECU_ADDRESS, OBD_TARGET_ADDRESS

LOG_TYPE = "isotp"


def start():
    uds_socket_req = create_socket(rxid=UDS_ECU_ADDRESS, txid=UDS_TARGET_ADDRESS)
    uds_socket_res = create_socket(rxid=UDS_TARGET_ADDRESS, txid=UDS_ECU_ADDRESS)

    obd_socket_req = create_socket(rxid=OBD_BROADCAST_ADDRESS, txid=OBD_TARGET_ADDRESS)
    obd_socket_res = create_socket(rxid=OBD_TARGET_ADDRESS, txid=OBD_ECU_ADDRESS)

    file_path = logger_utils.create_file_path(LOG_TYPE)
    while True:
        uds_request = uds_socket_req.recv()
        uds_response = uds_socket_res.recv()

        obd_request = obd_socket_req.recv()
        obd_response = obd_socket_res.recv()

        if uds_request is not None:
            write_to_log(file_path, uds_request, UDS_ECU_ADDRESS)
        if uds_response is not None:
            write_to_log(file_path, uds_response, UDS_TARGET_ADDRESS)
        if obd_request is not None:
            write_to_log(file_path, obd_request, OBD_BROADCAST_ADDRESS)
        if obd_response is not None:
            write_to_log(file_path, obd_response, OBD_TARGET_ADDRESS)


def create_socket(rxid, txid):
    socket = isotp.socket()
    socket.set_opts(socket.flags.LISTEN_MODE)
    socket.bind(CAN_INTERFACE, isotp.Address(rxid=rxid, txid=txid))
    return socket


def write_to_log(file_path, message, address):
    file_path = logger_utils.create_new_file_path_if_size_exceeded(file_path, LOG_TYPE)
    log_file = open(file_path, "a")
    log_file.write(create_log(address, message))
    log_file.close()


def create_log(address, message):
    return get_time() + " " + CAN_INTERFACE + " " + format_address(address) + "#" + format_msg(message) + "\n"


def get_time():
    return "(" + "{0:.6f}".format(time.time()) + ")"


def format_address(address):
    return hex(address).lstrip("0x").upper()


def format_msg(message):
    return message.hex().upper()
