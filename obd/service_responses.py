import random
import ecu_config_reader
import dtc_utils


DEFAULT_ECU_NAME = "ECU_SIMULATOR"

DEFAULT_VIN = "TESTVIN0123456789"

DEFAULT_FUEL_LEVEL = 60

DEFAULT_FUEL_TYPE = 1  # Gasoline

MAX_NUMBER_OF_CHARS_ECU_NAME = 20

MAX_NUMBER_OF_CHARS_VIN = 17

MAX_NUMBER_OF_FUEL_TYPES = 23

FUEL_LEVEL_MAX = 100

VEHICLE_SPEED_MAX = 255

VEHICLE_SPEED_ACCELERATION = 1

ENGINE_TEMP_MIN = 130  # 90 C - 40

ENGINE_TEMP_MAX = 150  # 110 C - 40

MAX_NUMBER_OF_DTCS_IN_RESPONSE = 255

BIG_ENDIAN = "big"

vehicle_speed = 0


def get_vehicle_speed():
    global vehicle_speed
    current_speed = vehicle_speed.to_bytes(1, BIG_ENDIAN)
    increment_vehicle_speed()
    return current_speed


def increment_vehicle_speed():
    global vehicle_speed
    vehicle_speed = (vehicle_speed + VEHICLE_SPEED_ACCELERATION) % (VEHICLE_SPEED_MAX + 1)


def get_engine_temperature():
    return random.randrange(ENGINE_TEMP_MIN, ENGINE_TEMP_MAX).to_bytes(1, BIG_ENDIAN)


def get_fuel_level():
    # the OBD device calculates the fuel level: (100/255) * fuel level
    # therefore, fuel level is multiplied by (255/100)
    fuel_level = validate_fuel_level(ecu_config_reader.get_fuel_level())
    return int(fuel_level * (255 / 100)).to_bytes(1, BIG_ENDIAN)


def validate_fuel_level(fuel_level):
    if isinstance(fuel_level, int) and fuel_level <= FUEL_LEVEL_MAX:
        return fuel_level
    return DEFAULT_FUEL_LEVEL


def get_fuel_type():
    fuel_type = validate_fuel_type(ecu_config_reader.get_fuel_type())
    return fuel_type.to_bytes(1, BIG_ENDIAN)


def validate_fuel_type(fuel_type):
    if MAX_NUMBER_OF_FUEL_TYPES >= fuel_type > 0:
        return fuel_type
    return DEFAULT_FUEL_TYPE


def get_vin():
    vin = ecu_config_reader.get_vin()
    if len(vin) > MAX_NUMBER_OF_CHARS_VIN:
        return add_vin_padding(DEFAULT_VIN)
    return add_vin_padding(vin)


def add_vin_padding(vin):
    vin_bytes = vin.encode()
    if len(vin_bytes) < MAX_NUMBER_OF_CHARS_VIN:
        vin_bytes = bytes(MAX_NUMBER_OF_CHARS_VIN - len(vin_bytes)) + vin_bytes
    return bytes(1) + vin_bytes


def get_ecu_name():
    ecu_name = ecu_config_reader.get_ecu_name()
    if len(ecu_name) > MAX_NUMBER_OF_CHARS_ECU_NAME:
        return add_ecu_name_padding(DEFAULT_ECU_NAME)
    return add_ecu_name_padding(ecu_name)


def add_ecu_name_padding(ecu_name):
    ecu_name_bytes = ecu_name.encode()
    if len(ecu_name_bytes) < MAX_NUMBER_OF_CHARS_ECU_NAME:
        ecu_name_bytes = bytes(MAX_NUMBER_OF_CHARS_ECU_NAME - len(ecu_name_bytes)) + ecu_name_bytes
    return ecu_name_bytes


def get_dtcs():
    dtcs = ecu_config_reader.get_dtcs()
    dtcs_bytes = dtc_utils.encode_obd_dtcs(dtcs)
    return add_number_of_dtcs_to_response(dtcs_bytes)


def add_number_of_dtcs_to_response(dtcs_bytes):
    number_of_dtcs = len(dtcs_bytes) / 2
    if MAX_NUMBER_OF_DTCS_IN_RESPONSE >= number_of_dtcs > 0:
        return int(number_of_dtcs).to_bytes(1, BIG_ENDIAN) + dtcs_bytes
    return bytes(1)