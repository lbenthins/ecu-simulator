def get_vehicle_speed():
    return 0x1E.to_bytes(1, byteorder="big")


def get_fuel_level():
    return 0x10.to_bytes(1, byteorder="big")


def get_engine_temperature():
    return 0x20.to_bytes(1, byteorder="big")


def get_fuel_type():
    return 0x01.to_bytes(1, byteorder="big")


SERVICES = [
    {0x01: "Show current data",
     "pids": [
         {"id": 0x05, "description": "Engine coolant temperature", "response": get_engine_temperature()},
         {"id": 0x0D, "description": "Vehicle speed", "response": get_vehicle_speed()},
         {"id": 0x2F, "description": "Fuel tank level input", "response": get_fuel_level()},
         {"id": 0x51, "description": "Fuel type", "response": get_fuel_type()}
     ]}
]


def get_service_pids(service_id):
    for service in SERVICES:
        if service.get(service_id) is not None:
            return service.get("pids")
    return None


def get_supported_pids_response(supported_pids, requested_pid):
    supported_pids_response = 0x00000001
    if requested_pid / 32 > 6:
        supported_pids_response = 0x00000000
    for p in supported_pids:
        supported_pid = p.get("id")
        if requested_pid < supported_pid < (requested_pid + 32):
            supported_pids_response = supported_pids_response | 0x80000000 >> (supported_pid - requested_pid - 1)
    return supported_pids_response.to_bytes(4, byteorder="big")


def is_supported_pids_request(pid):
    if pid == 0x00:
        return True
    return pid % 32 == 0


def process_service_request(requested_service, requested_pid):
    pids = get_service_pids(requested_service)
    if pids is not None:
        if is_supported_pids_request(requested_pid):
            return get_supported_pids_response(pids, requested_pid)
        for pid in pids:
            if pid.get("id") == requested_pid:
                return pid.get("response")
    return None
