import unittest
from obd import service_responses

BIG_ENDIAN = "big"

ENGINE_TEMP_MIN = 130

ENGINE_TEMP_MAX = 150


class TestServiceResponses(unittest.TestCase):

    def test_get_vehicle_speed_is_one_byte(self):
        self.assertEqual(1, len(service_responses.get_vehicle_speed()))

    def test_get_vehicle_speed_is_in_range_0_255(self):
        initial_vehicle_speed = 0
        self.assertEqual(initial_vehicle_speed.to_bytes(1, BIG_ENDIAN), service_responses.get_vehicle_speed())
        self.assertEqual((initial_vehicle_speed + 1).to_bytes(1, BIG_ENDIAN), service_responses.get_vehicle_speed())
        for i in range(2, 256, 1):
            self.assertEqual(i.to_bytes(1, BIG_ENDIAN), service_responses.get_vehicle_speed())

        self.assertEqual(initial_vehicle_speed.to_bytes(1, BIG_ENDIAN), service_responses.get_vehicle_speed())
        self.assertEqual((initial_vehicle_speed + 1).to_bytes(1, BIG_ENDIAN), service_responses.get_vehicle_speed())
        for i in range(2, 256, 1):
            self.assertEqual(i.to_bytes(1, BIG_ENDIAN), service_responses.get_vehicle_speed())

    def test_get_fuel_level_is_one_byte(self):
        self.assertEqual(1, len(service_responses.get_fuel_level()))

    def test_get_engine_temperature_is_one_byte(self):
        self.assertEqual(1, len(service_responses.get_engine_temperature()))

    def test_get_engine_temperature(self):
        self.assertAlmostEqual(ENGINE_TEMP_MIN, int(service_responses.get_engine_temperature().hex(), 16), delta=(
                ENGINE_TEMP_MAX - ENGINE_TEMP_MIN))
        self.assertAlmostEqual(ENGINE_TEMP_MAX, int(service_responses.get_engine_temperature().hex(), 16), delta=(
                ENGINE_TEMP_MAX - ENGINE_TEMP_MIN))

    def test_get_vin_has_18_bytes(self):
        self.assertEqual(18, len(service_responses.get_vin()))

    def test_get_vin_first_byte_is_0(self):
        self.assertEqual(0, service_responses.get_vin()[0])

    def test_get_vin_has_20_bytes(self):
        self.assertEqual(20, len(service_responses.get_ecu_name()))

    def test_get_fuel_level_has_1_byte(self):
        self.assertEqual(1, len(service_responses.get_fuel_level()))

    def test_get_fuel_level_is_smaller_equal_than_100(self):
        fuel_level = int(service_responses.get_fuel_level().hex(), 16) * (100 / 255)
        self.assertTrue(100 >= fuel_level > 0)

    def test_get_fuel_type_has_1_byte(self):
        self.assertEqual(1, len(service_responses.get_fuel_type()))

    def test_get_fuel_type_is_smaller_equal_than_23(self):
        # see https://en.wikipedia.org/wiki/OBD-II_PIDs#Fuel_Type_Coding
        self.assertTrue(23 >= int(service_responses.get_fuel_type().hex(), 16) > 0)


if __name__ == '__main__':
    unittest.main()
