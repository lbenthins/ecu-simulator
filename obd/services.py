def get_vehicle_speed():
    return 0x1E.to_bytes(1, byteorder="big")


def get_fuel_level():
    return 0x10.to_bytes(1, byteorder="big")


SERVICES = [
    {0x01: "Show current data", "pids": [
        {"id": 0x0D, "description": "Vehicle speed", "response": get_vehicle_speed()},
        {"id": 0x2F, "description": "Fuel tank level input", "response": get_fuel_level()}
    ]}
]


def get_service_pids(service_id):
    for service in SERVICES:
        if service.get(service_id) is not None:
            return service.get("pids")
    return None


def get_supported_pids_response(pids):
    supported_pids_response = 0x00000001
    for pid in pids:
        pid_int = int(pid.get("id"))
        if pid_int < 32:
            supported_pids_response = supported_pids_response | 0x80000000 >> (pid_int - 1)
    return supported_pids_response.to_bytes(4, byteorder="big")


def process_service_request(requested_service, requested_pid):
    pids = get_service_pids(requested_service)
    if pids is not None:
        if requested_pid == 0x00:
            return get_supported_pids_response(pids)
        for pid in pids:
            if pid.get("id") == requested_pid:
                return pid.get("response")
    return None
