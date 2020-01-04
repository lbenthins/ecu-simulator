import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ecu_config.json")

CONFIG = json.load(open(CONFIG_FILE, "r"))


def get_vin():
    return CONFIG["vin"].get("value")


def get_ecu_name():
    return CONFIG["ecu_name"].get("value")


def get_fuel_level():
    return CONFIG["fuel_level"].get("value")


def get_fuel_type():
    return CONFIG["fuel_type"].get("value")


def get_dtcs():
    return CONFIG["dtcs"].get("value")


def get_obd_broadcast_address():
    try:
        return int(CONFIG["obd_broadcast_address"].get("value"), 16)
    except ValueError as error:
        print(error)
        exit(1)


def get_obd_ecu_address():
    try:
        return int(CONFIG["obd_ecu_address"].get("value"), 16)
    except ValueError as error:
        print(error)
        exit(1)


def get_can_interface():
    return CONFIG["can_interface"].get("value")


def get_can_interface_type():
    return CONFIG["can_interface_type"].get("value")


def get_can_bitrate():
    return CONFIG["can_bitrate"].get("value")


def get_isotp_ko_file_path():
    return CONFIG["isotp_ko_file_path"].get("value")
