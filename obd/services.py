BIG_ENDIAN = "big"

SUPPORTED_PIDS_RESPONSE_MASK = 0x80000000

SUPPORTED_PIDS_RESPONSE_INIT_VALUE = 0x00000001

SUPPORTED_PIDS_RESPONSE_NUMBER_OF_PIDs = 32


def get_vehicle_speed():
    return 0x1E.to_bytes(1, BIG_ENDIAN)


def get_fuel_level():
    return 0x10.to_bytes(1, BIG_ENDIAN)


def get_engine_temperature():
    return 0x20.to_bytes(1, BIG_ENDIAN)


def get_fuel_type():
    return 0x01.to_bytes(1, BIG_ENDIAN)


def get_vin():
    return bytes([0x00]) + "TESTVIN0123456789".encode()


def get_ecu_name():
    return bytes([0x00]) + "TEST_ECU".encode()


def get_dtcs():
    return 0x0504770001000200030004.to_bytes(11, BIG_ENDIAN)


SERVICES = [
    {"id": 0x01, "description": "Show current data",
     "pids": [
         {"id": 0x05, "description": "Engine coolant temperature", "response": get_engine_temperature()},
         {"id": 0x0D, "description": "Vehicle speed", "response": get_vehicle_speed()},
         {"id": 0x2F, "description": "Fuel tank level input", "response": get_fuel_level()},
         {"id": 0x51, "description": "Fuel type", "response": get_fuel_type()}
     ]},
    {"id": 0x03, "description": "Show DTCs", "response": get_dtcs()},
    {"id": 0x09, "description": "Request vehicle information",
     "pids": [
         {"id": 0x02, "description": "Vehicle Identification Number(VIN)", "response": get_vin()},
         {"id": 0x0A, "description": "ECU name", "response": get_ecu_name()}
     ]}
]


def process_service_request(requested_service, requested_pid):
    if is_service_request_valid(requested_service, requested_pid):
        service_response, service_pids = get_service(requested_service)
        if service_pids is not None and requested_pid is not None:
            if is_supported_pids_request(requested_pid):
                return get_supported_pids_response(service_pids, requested_pid)
            return get_pid_response(requested_pid, service_pids)
        return service_response
    return None


def is_service_request_valid(requested_service, requested_pid):
    return (isinstance(requested_service, int) and isinstance(requested_pid, int)) \
            or (isinstance(requested_service, int) and requested_pid is None)


def get_service(requested_service):
    for service in SERVICES:
        if service.get("id") == requested_service:
            return service.get("response"), service.get("pids")
    return None, None


def get_service_response(requested_service):
    for service in SERVICES:
        if service.get("id") == requested_service:
            return service.get("response")
    return None


def get_pid_response(requested_pid, pids):
    for pid in pids:
        if pid.get("id") == requested_pid:
            return pid.get("response")
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
