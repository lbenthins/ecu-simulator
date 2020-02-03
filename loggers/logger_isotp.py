import isotp
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

        file_path = logger_utils.create_new_file_path_if_size_exceeded(file_path, LOG_TYPE)
        if uds_request is not None:
            logger_utils.write_to_file(file_path, None, UDS_ECU_ADDRESS, uds_request)
        if uds_response is not None:
            logger_utils.write_to_file(file_path, None, UDS_TARGET_ADDRESS, uds_response)
        if obd_request is not None:
            logger_utils.write_to_file(file_path, None, OBD_BROADCAST_ADDRESS, obd_request)
        if obd_response is not None:
            logger_utils.write_to_file(file_path, None, OBD_TARGET_ADDRESS, obd_response)


def create_socket(rxid, txid):
    socket = isotp.socket()
    socket.set_opts(socket.flags.LISTEN_MODE)
    socket.bind(CAN_INTERFACE, isotp.Address(rxid=rxid, txid=txid))
    return socket

