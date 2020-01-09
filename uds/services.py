READ_DTC_INFO_BY_STATUS_MASK = 0x2
READ_DTC_INFO_SID = 0x19
ECU_RESET_SID = 0x11

ECU_RESET_ENABLE_RAPID_POWER_SHUT_DOWN = 0x04

ECU_RESET_POWER_DOWN_TIME = 0x0F

DTC_STATUS_AVAILABILITY_MASK = 0xFF

NEGATIVE_RESPONSE_SID = 0x7F

NRC_SUB_FUNCTION_NOT_SUPPORTED = 0x12

NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT = 0x13

POSITIVE_RESPONSE_SID_MASK = 0x40


def get_0x19_response(request):
    return bytes([POSITIVE_RESPONSE_SID_MASK + READ_DTC_INFO_SID]) + bytes([READ_DTC_INFO_BY_STATUS_MASK]) + bytes([DTC_STATUS_AVAILABILITY_MASK])


def is_reset_type_supported(reset_type):
    return 0x05 >= reset_type >= 0x01


def get_0x11_response(request):
    negative_response = bytes([NEGATIVE_RESPONSE_SID]) + bytes([ECU_RESET_SID])
    if len(request) == 2:
        reset_type = request[1]
        if is_reset_type_supported(reset_type):
            positive_response = bytes([POSITIVE_RESPONSE_SID_MASK + ECU_RESET_SID]) + bytes([reset_type])
            if reset_type == ECU_RESET_ENABLE_RAPID_POWER_SHUT_DOWN:
                return positive_response + bytes([ECU_RESET_POWER_DOWN_TIME])
            return positive_response
        return negative_response + bytes([NRC_SUB_FUNCTION_NOT_SUPPORTED])
    return negative_response + bytes([NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT])


SERVICES = [
    {"id": ECU_RESET_SID, "description": "ECUReset", "response": lambda request: get_0x11_response(request)},
    {"id": 0x19, "description": "ReadDTCInformation", "response": lambda request: get_0x19_response(request)}
]


def process_service_request(request):
    if request is not None and len(request) >= 1:
        sid = request[0]
        for service in SERVICES:
            if service.get("id") == sid:
                return service.get("response")(request)
    return None
