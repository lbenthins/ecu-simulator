import unittest
from obd import services


class TestServices(unittest.TestCase):

    def test_process_service_0x01_pid_0x00(self):
        response = services.process_service_request(0x01, 0x00)
        self.assertIsNotNone(response)
        self.assertEqual("00080001", response.hex())

    def test_process_service_0x01_pid_0x20(self):
        response = services.process_service_request(0x01, 0x20)
        self.assertIsNotNone(response)
        self.assertEqual("00020001", response.hex())

        # response = services.process_service_request(0x01, 0x20)
        # self.assertEqual(response.hex(), "00080001")


if __name__ == '__main__':
    unittest.main()
