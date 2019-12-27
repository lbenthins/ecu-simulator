import isotp
from my_obd import services

CAN_INTERFACE = "vcan0"
POSITIVE_ANSWER = 0x40

RX_ID = 0x7DF
TX_ID = 0x7E8

can_socket = isotp.socket()
can_socket2 = isotp.socket()
can_socket.bind(CAN_INTERFACE, isotp.Address(rxid=RX_ID, txid=TX_ID))
can_socket2.bind(CAN_INTERFACE, isotp.Address(rxid=0x7E0, txid=TX_ID))


def process_request(req):
    requested_service = req[0]
    requested_pid = req[1]
    service_response = services.process_service_request(requested_service, requested_pid)
    if service_response is not None:
        return bytes([POSITIVE_ANSWER + requested_service]) + bytes([requested_pid]) + service_response
    return None


while True:
    request = can_socket.recv()
    if request is not None:
        print("Request: " + request.hex())
        response = process_request(request)
        if response is not None:
            print("Response: " + response.hex())
            can_socket2.send(response)

