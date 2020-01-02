import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ecu.json")

CONFIG = json.load(open(CONFIG_FILE, "r"))


def get_vin():
    return CONFIG["vin"]


def get_ecu_name():
    return CONFIG["ecu_name"]


def get_fuel_level():
    return CONFIG["fuel_level"]


def get_fuel_type():
    return CONFIG["fuel_type"]


def get_dtcs():
    return CONFIG["dtcs"]
