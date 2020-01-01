import unittest
import ecu_info

BIG_ENDIAN = "big"

ENGINE_TEMP_MIN = 130

ENGINE_TEMP_MAX = 150


class TestEcuInfo(unittest.TestCase):

    def test_get_vehicle_speed_is_one_byte(self):
        self.assertEqual(1, len(ecu_info.get_vehicle_speed()))

    def test_get_vehicle_speed_is_in_range_0_255(self):
        initial_vehicle_speed = 0
        self.assertEqual(initial_vehicle_speed.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        self.assertEqual((initial_vehicle_speed + 1).to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        for i in range(2, 256, 1):
            self.assertEqual(i.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())

        self.assertEqual(initial_vehicle_speed.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        self.assertEqual((initial_vehicle_speed + 1).to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        for i in range(2, 256, 1):
            self.assertEqual(i.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())

    def test_get_fuel_level_is_one_byte(self):
        self.assertEqual(1, len(ecu_info.get_fuel_level()))

    def test_get_engine_temperature_is_one_byte(self):
        self.assertEqual(1, len(ecu_info.get_engine_temperature()))

    def test_get_engine_temperature(self):
        self.assertAlmostEqual(ENGINE_TEMP_MIN, int(ecu_info.get_engine_temperature().hex(), 16), delta=(
                ENGINE_TEMP_MAX - ENGINE_TEMP_MIN))
        self.assertAlmostEqual(ENGINE_TEMP_MAX, int(ecu_info.get_engine_temperature().hex(), 16), delta=(
                ENGINE_TEMP_MAX - ENGINE_TEMP_MIN))


if __name__ == '__main__':
    unittest.main()
