import unittest
from obd import services


class TestServices(unittest.TestCase):

    def test_process_service_0x01_pid_0x00(self):
        response = services.process_service_request(0x01, 0x00)
        self.assertIsNotNone(response)
        self.assertEqual("08080001", response.hex())

    def test_process_service_0x01_pid_0x20(self):
        response = services.process_service_request(0x01, 0x20)
        self.assertIsNotNone(response)
        self.assertEqual("00020001", response.hex())

    def test_process_service_0x01_pid_0x40(self):
        response = services.process_service_request(0x01, 0x40)
        self.assertIsNotNone(response)
        self.assertEqual("00008001", response.hex())

    def test_process_service_0x01_pid_0xE0_returns_no_pids(self):
        response = services.process_service_request(0x01, 0xE0)
        self.assertIsNotNone(response)
        self.assertEqual("00000000", response.hex())


if __name__ == '__main__':
    unittest.main()
