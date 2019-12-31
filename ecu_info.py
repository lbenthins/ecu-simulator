BIG_ENDIAN = "big"

PADDING = 0x00

vehicle_speed = 0


def get_vehicle_speed():
    global vehicle_speed
    result = vehicle_speed.to_bytes(1, BIG_ENDIAN)
    vehicle_speed = (vehicle_speed + 5) % 255
    return result


def get_fuel_level():
    return 0x10.to_bytes(1, BIG_ENDIAN)


def get_engine_temperature():
    return 0x20.to_bytes(1, BIG_ENDIAN)


def get_fuel_type():
    return 0x01.to_bytes(1, BIG_ENDIAN)


def get_vin():
    return bytes([PADDING]) + "TESTVIN0123456789".encode()


def get_ecu_name():
    return bytes([PADDING]) + "TEST_ECU".encode()


def get_dtcs():
    return 0x0504770001000200030004.to_bytes(11, BIG_ENDIAN)
