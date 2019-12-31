import unittest
import ecu_info

BIG_ENDIAN = "big"


class TestEcuInfo(unittest.TestCase):

    def test_get_vehicle_speed_is_one_byte(self):
        self.assertEqual(1, len(ecu_info.get_vehicle_speed()))

    def test_get_vehicle_speed_is_in_range_0_255(self):
        initial_vehicle_speed = 0
        self.assertEqual(initial_vehicle_speed.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        self.assertEqual((initial_vehicle_speed + 5).to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        for i in range(10, 255, 5):
            self.assertEqual(i.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        self.assertEqual(initial_vehicle_speed.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        self.assertEqual((initial_vehicle_speed + 5).to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())
        for i in range(10, 255, 5):
            self.assertEqual(i.to_bytes(1, BIG_ENDIAN), ecu_info.get_vehicle_speed())

    def test_get_fuel_level_is_one_byte(self):
        self.assertEqual(1, len(ecu_info.get_fuel_level()))


if __name__ == '__main__':
    unittest.main()
