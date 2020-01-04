import isotp
from obd import services
import ecu_config_reader as ecu_config

CAN_INTERFACE = ecu_config.get_can_interface()
POSITIVE_ANSWER = 0x40

RX_ID_FUNCTIONAL = ecu_config.get_obd_broadcast_address()
RX_ID_PHYSICAL = ecu_config.get_obd_ecu_address()
TX_ID = RX_ID_PHYSICAL + 8

can_socket = isotp.socket()
can_socket2 = isotp.socket()
can_socket.bind(CAN_INTERFACE, isotp.Address(rxid=RX_ID_FUNCTIONAL, txid=TX_ID))
can_socket2.bind(CAN_INTERFACE, isotp.Address(rxid=RX_ID_PHYSICAL, txid=TX_ID))


def process_request(req):
    requested_service = req[0]
    requested_pid = None
    if len(req) == 2:
        requested_pid = req[1]
    service_response = services.process_service_request(requested_service, requested_pid)
    if service_response is not None:
        if requested_pid is None:
            return bytes([POSITIVE_ANSWER + requested_service]) + service_response
        return bytes([POSITIVE_ANSWER + requested_service]) + bytes([requested_pid]) + service_response
    return None


while True:
    request = can_socket.recv()
    if request is not None:
        if len(request) >= 1:
            print("Request: " + request.hex())
            response = process_request(request)
            if response is not None:
                print("Response: " + response.hex())
                can_socket2.send(response)

