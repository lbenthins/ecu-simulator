import isotp
import time

CAN_INTERFACE = "vcan0"
VEHICLE_SPEED = 0x1E
POSITIVE_ANSWER = 0x40

RX_ID = 0x7DF
TX_ID = 0x7E8

can_socket = isotp.socket()
can_socket.bind(CAN_INTERFACE, isotp.Address(rxid=RX_ID, txid=TX_ID))


def process_request(r):
    print("Received bytes " + str(r.hex()))
    if r[0] == int(0x01):
        print("Service: Current Data")
        if r[1] == int(0x0D):
            print("PID: Vehicle Speed")
            return bytes([POSITIVE_ANSWER + 0x01]) + bytes([0x0D]) + bytes([VEHICLE_SPEED])


while True:
    request = can_socket.recv()
    if request is not None:
        response = process_request(request)
        print("Response: " + response.hex())
    time.sleep(2)
