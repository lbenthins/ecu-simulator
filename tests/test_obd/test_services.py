import unittest
from obd import services

INVALID_SERVICE_ID = "yy"

INVALID_PID = "xx"

UNKNOWN_PID = 0xFF

UNKNOWN_SERVICE = 0xFF


class TestServices(unittest.TestCase):

    def test_process_service_0x01_pid_0x00(self):
        response = services.process_service_request(requested_service=0x01, requested_pid=0x00)
        self.assertIsNotNone(response)
        self.assertEqual("08080001", response.hex())

    def test_process_service_0x01_pid_0x20(self):
        response = services.process_service_request(requested_service=0x01, requested_pid=0x20)
        self.assertIsNotNone(response)
        self.assertEqual("00020001", response.hex())

    def test_process_service_0x01_pid_0x40(self):
        response = services.process_service_request(requested_service=0x01, requested_pid=0x40)
        self.assertIsNotNone(response)
        self.assertEqual("00008001", response.hex())

    def test_process_service_0x01_pid_0xE0_returns_no_pids(self):
        response = services.process_service_request(requested_service=0x01, requested_pid=0xE0)
        self.assertIsNotNone(response)
        self.assertEqual("00000000", response.hex())

    def test_process_service_0x09_pid_0x00(self):
        response = services.process_service_request(requested_service=0x09, requested_pid=0x00)
        self.assertIsNotNone(response)
        self.assertEqual("40400001", response.hex())

    def test_process_service_0x03_returns_DTCs(self):
        response = services.process_service_request(requested_service=0x03, requested_pid=None)
        self.assertIsNotNone(response)

    def test_process_unknown_service_returns_none(self):
        response = services.process_service_request(requested_service=UNKNOWN_SERVICE, requested_pid=0x00)
        self.assertIsNone(response)

    def test_process_service_unknown_pid_returns_none(self):
        response = services.process_service_request(requested_service=0x01, requested_pid=UNKNOWN_PID)
        self.assertIsNone(response)

    def test_process_invalid_service_request_returns_none(self):
        self.assertIsNone(services.process_service_request(requested_service=INVALID_SERVICE_ID, requested_pid=0x00))
        self.assertIsNone(services.process_service_request(requested_service=0x01, requested_pid=INVALID_PID))
        self.assertIsNone(services.process_service_request(requested_service=INVALID_SERVICE_ID, requested_pid=INVALID_PID))


if __name__ == '__main__':
    unittest.main()
