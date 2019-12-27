def get_vehicle_speed():
    return 0x1E.to_bytes(1, byteorder="big")


supported_services = [
    {0x01: "show current data",
     "PIDs": [
         {"id": 0x0D, "description": "vehicle speed", "response": get_vehicle_speed()}
     ]}
]


def get_service_pids(requested_service):
    for supported_service in supported_services:
        if supported_service.get(requested_service) is not None:
            return supported_service.get("PIDs")
    return None


def get_pid_response(supported_pids, requested_pid):
    if requested_pid == 0x00:
        return get_supported_pids_response(supported_pids)
    for supported_pid in supported_pids:
        if supported_pid.get("id") == requested_pid:
            return supported_pid.get("response")
    return None


def get_supported_pids_response(supported_pids):
    supported_pids_response = 0x00000000
    for pid in supported_pids:
        supported_pids_response = supported_pids_response | 0x80000000 >> (int(pid.get("id") - 1))
    return supported_pids_response.to_bytes(4, byteorder="big")
