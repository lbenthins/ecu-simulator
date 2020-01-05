

ECU_RESET_ENABLE_RAPID_POWER_SHUT_DOWN = 0x04

ECU_RESET_POWER_DOWN_TIME = 0x0F

NEGATIVE_RESPONSE_SID = 0x7F

NRC_SUB_FUNCTION_NOT_SUPPORTED = 0x12

NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT = 0x13

POSITIVE_RESPONSE_SID_MASK = 0x40


def is_reset_type_supported(reset_type):
    return 0x05 >= reset_type >= 0x01


def get_0x11_response(request):
    request_sid = request[0]
    negative_response = bytes([NEGATIVE_RESPONSE_SID]) + bytes([request_sid])
    if len(request) == 2:
        reset_type = request[1]
        if is_reset_type_supported(reset_type):
            positive_response = bytes([POSITIVE_RESPONSE_SID_MASK + request_sid]) + bytes([reset_type])
            if reset_type == ECU_RESET_ENABLE_RAPID_POWER_SHUT_DOWN:
                return positive_response + bytes([ECU_RESET_POWER_DOWN_TIME])
            return positive_response
        return negative_response + bytes([NRC_SUB_FUNCTION_NOT_SUPPORTED])
    return negative_response + bytes([NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT])


SERVICES = [
    {"id": 0x11, "description": "ECUReset", "response": lambda request: get_0x11_response(request)}
]


def process_service_request(request):
    if request is not None and len(request) >= 1:
        sid = request[0]
        for service in SERVICES:
            if service.get("id") == sid:
                return service.get("response")(request)
    return None
