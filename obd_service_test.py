import isotp
from my_obd import service

CAN_INTERFACE = "can0"
POSITIVE_ANSWER = 0x40

RX_ID = 0x7DF
TX_ID = 0x7E8

can_socket = isotp.socket()
can_socket2 = isotp.socket()
can_socket.bind(CAN_INTERFACE, isotp.Address(rxid=RX_ID, txid=TX_ID))
can_socket2.bind(CAN_INTERFACE, isotp.Address(rxid=0x7E0, txid=TX_ID))


def process_request(req):
    pids = service.get_service_pids(req[0])
    if pids is not None:
        pid_response = service.get_pid_response(pids, req[1])
        if pid_response is not None:
            return bytes([POSITIVE_ANSWER + req[0]]) + bytes([req[1]]) + pid_response
    return None


while True:
    request = can_socket.recv()
    if request is not None:
        print("Request: " + request.hex())
        response = process_request(request)
        if response is not None:
            print("Response: " + response.hex())
            can_socket2.send(response)

