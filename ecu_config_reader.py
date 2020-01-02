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
