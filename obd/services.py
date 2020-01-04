from obd import service_responses as responses

SUPPORTED_PIDS_RESPONSE_MASK = 0x80000000

SUPPORTED_PIDS_RESPONSE_INIT_VALUE = 0x00000001

SUPPORTED_PIDS_RESPONSE_NUMBER_OF_PIDs = 32

POSITIVE_RESPONSE_MASK = 0x40

BIG_ENDIAN = "big"

FUEL_TYPE = responses.get_fuel_type()

DTCs = responses.get_dtcs()

VIN = responses.get_vin()

ECU_NAME = responses.get_ecu_name()


SERVICES = [
    {"id": 0x01, "description": "Show current data", "response": lambda: None,
     "pids": [
         {"id": 0x05, "description": "Engine coolant temperature", "response": lambda: responses.get_engine_temperature()},
         {"id": 0x0D, "description": "Vehicle speed", "response": lambda: responses.get_vehicle_speed()},
         {"id": 0x2F, "description": "Fuel tank level input", "response": lambda: responses.get_fuel_level()},
         {"id": 0x51, "description": "Fuel type", "response": lambda: FUEL_TYPE}
     ]},
    {"id": 0x03, "description": "Show DTCs", "response": lambda: DTCs},
    {"id": 0x09, "description": "Request vehicle information", "response": lambda: None,
     "pids": [
         {"id": 0x02, "description": "Vehicle Identification Number(VIN)", "response": lambda: VIN},
         {"id": 0x0A, "description": "ECU name", "response": lambda: ECU_NAME}
     ]}
]


def process_service_request(requested_sid, requested_pid):
    if is_service_request_valid(requested_sid, requested_pid):
        service_response, service_pids = get_service(requested_sid)
        if service_pids is not None and requested_pid is not None:
            if is_supported_pids_request(requested_pid):
                response = get_supported_pids_response(service_pids, requested_pid)
                return add_response_prefix(requested_sid, requested_pid, response)
            return add_response_prefix(requested_sid, requested_pid, get_pid_response(requested_pid, service_pids))
        return add_response_prefix(requested_sid, requested_pid, service_response)
    return None


def add_response_prefix(requested_sid, requested_pid, response):
    if response is not None:
        response_sid = bytes([POSITIVE_RESPONSE_MASK + requested_sid])
        if requested_pid is None:
            return response_sid + response
        return response_sid + bytes([requested_pid]) + response
    return None


def is_service_request_valid(requested_sid, requested_pid):
    is_sid_valid_ = is_sid_valid(requested_sid)
    return is_sid_valid_ and is_pid_valid(requested_pid) or (is_sid_valid_ and requested_pid is None)


def is_sid_valid(sid):
    return isinstance(sid, int) and 10 >= sid >= 1


def is_pid_valid(pid):
    return isinstance(pid, int) and 255 >= pid >= 0


def get_service(requested_sid):
    for service in SERVICES:
        if service.get("id") == requested_sid:
            return service.get("response")(), service.get("pids")
    return None, None


def get_pid_response(requested_pid, pids):
    for pid in pids:
        if pid.get("id") == requested_pid:
            return pid.get("response")()
    return None


def is_supported_pids_request(requested_pid):
    return requested_pid % SUPPORTED_PIDS_RESPONSE_NUMBER_OF_PIDs == 0


def get_supported_pids_response(supported_pids, requested_pid):
    supported_pids_response = init_supported_pids_response(requested_pid)
    for pid in supported_pids:
        supported_pid = pid.get("id")
        if requested_pid < supported_pid < (requested_pid + SUPPORTED_PIDS_RESPONSE_NUMBER_OF_PIDs):
            supported_pids_response |= SUPPORTED_PIDS_RESPONSE_MASK >> (supported_pid - requested_pid - 1)
    return supported_pids_response.to_bytes(4, BIG_ENDIAN)


def init_supported_pids_response(requested_pid):
    if requested_pid / SUPPORTED_PIDS_RESPONSE_NUMBER_OF_PIDs > 6:
        return SUPPORTED_PIDS_RESPONSE_INIT_VALUE >> 1
    return SUPPORTED_PIDS_RESPONSE_INIT_VALUE
