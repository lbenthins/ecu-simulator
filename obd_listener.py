import isotp
import ecu_config
from obd import services

CAN_INTERFACE = ecu_config.get_can_interface()

BROADCAST_ADDRESS = ecu_config.get_obd_broadcast_address()

ECU_ADDRESS = ecu_config.get_obd_ecu_address()

TARGET_ADDRESS = ECU_ADDRESS + 8


def start():
    request_socket = create_isotp_socket(BROADCAST_ADDRESS, TARGET_ADDRESS)
    response_socket = create_isotp_socket(ECU_ADDRESS, TARGET_ADDRESS)
    while True:
        request = request_socket.recv()
        requested_pid, requested_sid = get_sid_and_pid(request)
        if requested_sid is not None:
            print("Request: " + request.hex())
            response = services.process_service_request(requested_sid, requested_pid)
            if response is not None:
                print("Response: " + response.hex())
                response_socket.send(response)


def create_isotp_socket(receiver_address, target_address):
    socket = isotp.socket()
    socket.bind(CAN_INTERFACE, isotp.Address(rxid=receiver_address, txid=target_address))
    return socket


def get_sid_and_pid(request):
    pid, sid = None, None
    if request is not None:
        request_bytes_length = len(request)
        if request_bytes_length >= 1:
            sid = request[0]
        if request_bytes_length >= 2:
            pid = request[1]
    return pid, sid
