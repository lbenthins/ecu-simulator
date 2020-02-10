import dtc_utils
import ecu_config as ecu_config
from loggers.logger_app import logger

DIAGNOSTIC_SESSION_CONTROL_SID = 0x10

DIAGNOSTIC_SESSION_TYPES = [0x01, 0x02, 0x03, 0x04]

DIAGNOSTIC_SESSION_PARAMETER_RECORD = [0x00, 0x1E, 0x0B, 0xB8]

ECU_RESET_SID = 0x11

ECU_RESET_ENABLE_RAPID_POWER_SHUT_DOWN = 0x04

ECU_RESET_POWER_DOWN_TIME = 0x0F

READ_DTC_INFO_BY_STATUS_MASK = 0x2

READ_DTC_INFO_SID = 0x19

READ_DTC_STATUS_AVAILABILITY_MASK = 0xFF

DTCS = dtc_utils.encode_uds_dtcs(ecu_config.get_dtcs())

POSITIVE_RESPONSE_SID_MASK = 0x40

NEGATIVE_RESPONSE_SID = 0x7F

NRC_SUB_FUNCTION_NOT_SUPPORTED = 0x12

NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT = 0x13


SERVICES = [
    {"id": ECU_RESET_SID, "description": "ECUReset", "response": lambda request: get_0x11_response(request)},
    {"id": READ_DTC_INFO_SID, "description": "ReadDTCInformation", "response": lambda request: get_0x19_response(request)},
    {"id": DIAGNOSTIC_SESSION_CONTROL_SID, "description": "DiagnosticSessionControl", "response": lambda request: get_0x10_response(request)}
]


def process_service_request(request):
    if request is not None and len(request) >= 1:
        sid = request[0]
        for service in SERVICES:
            if service.get("id") == sid:
                logger.info("Requested UDS SID " + hex(sid) + ": " + service.get("description"))
                return service.get("response")(request)
        logger.warning("Requested SID " + hex(sid) + " not supported")
    else:
        logger.warning("Invalid request")
        return None


def get_0x10_response(request):
    if len(request) == 2:
        session_type = request[1]
        if session_type in DIAGNOSTIC_SESSION_TYPES:
            return get_positive_response_sid(DIAGNOSTIC_SESSION_CONTROL_SID) + bytes([session_type]) \
                   + bytes(DIAGNOSTIC_SESSION_PARAMETER_RECORD)
        return get_negative_response(DIAGNOSTIC_SESSION_CONTROL_SID,  NRC_SUB_FUNCTION_NOT_SUPPORTED)
    return get_negative_response(DIAGNOSTIC_SESSION_CONTROL_SID,  NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT)


def get_0x11_response(request):
    if len(request) == 2:
        reset_type = request[1]
        if is_reset_type_supported(reset_type):
            positive_response = get_positive_response_sid(ECU_RESET_SID) + bytes([reset_type])
            if reset_type == ECU_RESET_ENABLE_RAPID_POWER_SHUT_DOWN:
                return positive_response + bytes([ECU_RESET_POWER_DOWN_TIME])
            return positive_response
        return get_negative_response(ECU_RESET_SID,  NRC_SUB_FUNCTION_NOT_SUPPORTED)
    return get_negative_response(ECU_RESET_SID,  NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT)


def get_0x19_response(request):
    if len(request) == 2:
        report_type = request[1]
        if report_type == READ_DTC_INFO_BY_STATUS_MASK:
            positive_response = get_positive_response_sid(READ_DTC_INFO_SID) + bytes([report_type]) \
                                + bytes([READ_DTC_STATUS_AVAILABILITY_MASK])
            return add_dtcs_to_response(positive_response)
        return get_negative_response(READ_DTC_INFO_SID, NRC_SUB_FUNCTION_NOT_SUPPORTED)
    return get_negative_response(READ_DTC_INFO_SID, NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT)


def is_reset_type_supported(reset_type):
    return 0x05 >= reset_type >= 0x01


def add_dtcs_to_response(response):
    if len(DTCS) > 0:
        return response + DTCS
    return response


def get_positive_response_sid(requested_sid):
    return bytes([requested_sid + POSITIVE_RESPONSE_SID_MASK])


def get_negative_response(sid, nrc):
    logger.warning("Negative response for SID " + hex(sid) + " will be sent")
    return bytes([NEGATIVE_RESPONSE_SID]) + bytes([sid]) + bytes([nrc])


