import isotp
import ecu_config
from uds import services
from addresses import UDS_ECU_ADDRESS, UDS_TARGET_ADDRESS

CAN_INTERFACE = ecu_config.get_can_interface()


def start():
    isotp_socket = create_isotp_socket(UDS_ECU_ADDRESS, UDS_TARGET_ADDRESS)
    while True:
        request = isotp_socket.recv()
        if request is not None:
            if len(request) >= 1:
                response = services.process_service_request(request)
                if response is not None:
                    print("Response: " + response.hex())
                    isotp_socket.send(response)


def create_isotp_socket(receiver_address, target_address):
    socket = isotp.socket()
    socket.bind(CAN_INTERFACE, isotp.Address(rxid=receiver_address, txid=target_address))
    return socket

