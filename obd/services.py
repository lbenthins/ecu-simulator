import ecu_info

BIG_ENDIAN = "big"

SUPPORTED_PIDS_RESPONSE_MASK = 0x80000000

SUPPORTED_PIDS_RESPONSE_INIT_VALUE = 0x00000001

SUPPORTED_PIDS_RESPONSE_NUMBER_OF_PIDs = 32

FUEL_TYPE = ecu_info.get_fuel_type()

DTCs = ecu_info.get_dtcs()

VIN = ecu_info.get_vin()

ECU_NAME = ecu_info.get_ecu_name()

SERVICES = [
    {"id": 0x01, "description": "Show current data", "response": lambda: None,
     "pids": [
         {"id": 0x05, "description": "Engine coolant temperature", "response": lambda: ecu_info.get_engine_temperature()},
         {"id": 0x0D, "description": "Vehicle speed", "response": lambda: ecu_info.get_vehicle_speed()},
         {"id": 0x2F, "description": "Fuel tank level input", "response": lambda: ecu_info.get_fuel_level()},
         {"id": 0x51, "description": "Fuel type", "response": lambda: FUEL_TYPE}
     ]},
    {"id": 0x03, "description": "Show DTCs", "response": lambda: DTCs},
    {"id": 0x09, "description": "Request vehicle information", "response": lambda: None,
     "pids": [
         {"id": 0x02, "description": "Vehicle Identification Number(VIN)", "response": lambda: VIN},
         {"id": 0x0A, "description": "ECU name", "response": lambda: ECU_NAME}
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
