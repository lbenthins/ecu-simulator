import os
import isotp
import time
import datetime
import obd_listener
import uds_listener
import ecu_config

LOG_FILE_NAME_FORMAT = 'isotp_%y%m%d%H%M%S.log'

MAX_LOG_FILE_SIZE = 1500000  # bytes

CAN_INTERFACE = ecu_config.get_can_interface()


def start():
    uds_socket_req = create_socket(rxid=uds_listener.ECU_ADDRESS, txid=uds_listener.TARGET_ADDRESS)
    uds_socket_res = create_socket(rxid=uds_listener.TARGET_ADDRESS, txid=uds_listener.ECU_ADDRESS)

    obd_broadcast_socket_req = create_socket(rxid=obd_listener.BROADCAST_ADDRESS, txid=obd_listener.TARGET_ADDRESS)
    obd_broadcast_socket_res = create_socket(rxid=obd_listener.TARGET_ADDRESS, txid=obd_listener.BROADCAST_ADDRESS)

    obd_socket_req = create_socket(rxid=obd_listener.ECU_ADDRESS, txid=obd_listener.TARGET_ADDRESS)
    obd_socket_res = create_socket(rxid=obd_listener.TARGET_ADDRESS, txid=obd_listener.ECU_ADDRESS)

    log_file_path = create_file_path()

    while True:
        uds_msg_req = uds_socket_req.recv()
        uds_msg_res = uds_socket_res.recv()

        obd_broadcast_msg_req = obd_broadcast_socket_req.recv()
        obd_broadcast_msg_res = obd_broadcast_socket_res.recv()

        obd_msg_req = obd_socket_req.recv()
        obd_msg_res = obd_socket_res.recv()

        if uds_msg_req is not None:
            write_to_log(log_file_path, uds_msg_req, uds_socket_req.address.rxid)
        if uds_msg_res is not None:
            write_to_log(log_file_path, uds_msg_res, uds_socket_res.address.rxid)
        if obd_broadcast_msg_req is not None:
            write_to_log(log_file_path, obd_broadcast_msg_req, obd_broadcast_socket_req.address.rxid)
        if obd_broadcast_msg_res is not None:
            write_to_log(log_file_path, obd_broadcast_msg_res, obd_broadcast_socket_res.address.rxid)
        if obd_msg_req is not None:
            write_to_log(log_file_path, obd_msg_req, obd_socket_req.address.rxid)
        if obd_msg_res is not None:
            write_to_log(log_file_path, obd_msg_res, obd_socket_res.address.rxid)


def write_to_log(log_file_path, msg, address):
    log_file_path = create_new_file_path_if_size_exceeded(log_file_path)
    log_file = open(log_file_path, "a")
    log_file.write(
        "(" + "{0:.6f}".format(time.time()) + ") " + CAN_INTERFACE + " " + hex(
            address).upper() + "#" + msg.hex().upper() + "\n")
    log_file.close()


def log(log_file_path, socket):
    while True:
        msg = socket.recv()
        if msg is not None:
            log_file_path = create_new_file_path_if_size_exceeded(log_file_path)
            log_file = open(log_file_path, "a")
            log_file.write(
                "(" + "{0:.6f}".format(time.time()) + ") " + CAN_INTERFACE + " " + hex(socket.address.rxid).upper() + "#" + msg.hex().upper() + "\n")
            log_file.close()


def create_socket(rxid, txid):
    socket = isotp.socket()
    socket.set_opts(socket.flags.LISTEN_MODE)
    socket.bind(CAN_INTERFACE, isotp.Address(rxid=rxid, txid=txid))
    return socket


def create_new_file_path_if_size_exceeded(file_path):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > MAX_LOG_FILE_SIZE:
            file_path = create_file_path()
    return file_path


def create_file_path():
    return os.path.join(os.path.dirname(__file__), datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT))
