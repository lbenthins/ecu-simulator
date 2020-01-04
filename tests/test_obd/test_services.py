import unittest
from obd import services

INVALID_SID = 0xB

INVALID_PID = 256

STRING_SID = "yy"

STRING_PID = "xx"

UNSUPPORTED_PID = 0xFF

UNSUPPORTED_SID = 0x08


class TestServices(unittest.TestCase):

    def test_process_service_0x01_pid_0x00(self):
        response = services.process_service_request(requested_sid=0x01, requested_pid=0x00)
        self.assertIsNotNone(response)
        self.assertEqual("410008080001", response.hex())

    def test_process_service_0x01_pid_0x20(self):
        response = services.process_service_request(requested_sid=0x01, requested_pid=0x20)
        self.assertIsNotNone(response)
        self.assertEqual("412000020001", response.hex())

    def test_process_service_0x01_pid_0x40(self):
        response = services.process_service_request(requested_sid=0x01, requested_pid=0x40)
        self.assertIsNotNone(response)
        self.assertEqual("414000008001", response.hex())

    def test_process_service_0x01_pid_0xE0_returns_no_pids(self):
        response = services.process_service_request(requested_sid=0x01, requested_pid=0xE0)
        self.assertIsNotNone(response)
        self.assertEqual("41e000000000", response.hex())

    def test_process_service_0x09_pid_0x00(self):
        response = services.process_service_request(requested_sid=0x09, requested_pid=0x00)
        self.assertIsNotNone(response)
        self.assertEqual("490040400001", response.hex())

    def test_process_service_0x03_returns_DTCs(self):
        response = services.process_service_request(requested_sid=0x03, requested_pid=None)
        self.assertIsNotNone(response)

    def test_process_unsupported_service_returns_none(self):
        self.assertIsNone(services.process_service_request(requested_sid=UNSUPPORTED_SID, requested_pid=0x00))
        self.assertIsNone(services.process_service_request(requested_sid=UNSUPPORTED_SID, requested_pid=None))

    def test_process_service_unknown_pid_returns_none(self):
        self.assertIsNone(services.process_service_request(requested_sid=0x01, requested_pid=UNSUPPORTED_PID))

    def test_process_invalid_service_request_returns_none(self):
        self.assertIsNone(services.process_service_request(requested_sid=INVALID_SID, requested_pid=0x00))
        self.assertIsNone(services.process_service_request(requested_sid=0x01, requested_pid=INVALID_PID))
        self.assertIsNone(services.process_service_request(requested_sid=INVALID_SID, requested_pid=INVALID_PID))
        self.assertIsNone(services.process_service_request(requested_sid=STRING_SID, requested_pid=0x00))
        self.assertIsNone(services.process_service_request(requested_sid=0x01, requested_pid=STRING_PID))
        self.assertIsNone(services.process_service_request(requested_sid=STRING_SID, requested_pid=STRING_PID))


if __name__ == '__main__':
    unittest.main()
