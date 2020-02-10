import unittest
from uds import services
import ecu_config as ecu_config
import dtc_utils


DIAGNOSTIC_SESSION_CONTROL_SID = 0x10

DIAGNOSTIC_SESSION_TYPES = [0x01, 0x02, 0x03, 0x04]

DIAGNOSTIC_SESSION_INVALID_TYPE = 0x05

DIAGNOSTIC_SESSION_PARAMETER_RECORD = [0x00, 0x1E, 0x0B, 0xB8]

ECU_RESET_SID = 0x11

ECU_RESET_HARD = 0x01

ECU_RESET_ENABLE_RAPID_POWER_DOWN = 0x04

ECU_RESET_POWER_DOWN_TIME = 0x0f

READ_DTC_INFO_SID = 0x19

READ_DTC_INFO_BY_STATUS_MASK = 0x02

READ_DTC_STATUS_AVAILABILITY_MASK = 0xFF

POSITIVE_RESPONSE_MASK = 0x40

NEGATIVE_RESPONSE_ID = 0x7F

NRC_SUB_FUNCTION_NOT_SUPPORTED = 0x12

NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT = 0x13


def get_response_sid(sid):
    return bytes([POSITIVE_RESPONSE_MASK + sid])


class TestUdsServices(unittest.TestCase):

    def test_process_service_0x10(self):
        request = bytes([DIAGNOSTIC_SESSION_CONTROL_SID]) + bytes([DIAGNOSTIC_SESSION_TYPES[0]])
        response = services.process_service_request(request)
        expected_response = get_response_sid(DIAGNOSTIC_SESSION_CONTROL_SID) + bytes(
            [DIAGNOSTIC_SESSION_TYPES[0]]) + bytes(DIAGNOSTIC_SESSION_PARAMETER_RECORD)
        self.assertIsNotNone(response)
        self.assertEqual(6, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x10_with_unsupported_session_type_returns_negative_response(self):
        request = bytes([DIAGNOSTIC_SESSION_CONTROL_SID]) + bytes([DIAGNOSTIC_SESSION_INVALID_TYPE])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([DIAGNOSTIC_SESSION_CONTROL_SID]) + bytes(
            [NRC_SUB_FUNCTION_NOT_SUPPORTED])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x10_with_invalid_message_length_returns_negative_response(self):
        request = bytes([DIAGNOSTIC_SESSION_CONTROL_SID])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([DIAGNOSTIC_SESSION_CONTROL_SID]) + bytes(
            [NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_hard_reset(self):
        request = bytes([ECU_RESET_SID]) + bytes([ECU_RESET_HARD])
        response = services.process_service_request(request)
        expected_response = get_response_sid(ECU_RESET_SID) + bytes([ECU_RESET_HARD])
        self.assertIsNotNone(response)
        self.assertEqual(2, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_enable_power_shut_down(self):
        request = bytes([ECU_RESET_SID]) + bytes([ECU_RESET_ENABLE_RAPID_POWER_DOWN])
        response = services.process_service_request(request)
        expected_response = get_response_sid(ECU_RESET_SID) + bytes([ECU_RESET_ENABLE_RAPID_POWER_DOWN]) + bytes(
            [ECU_RESET_POWER_DOWN_TIME])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_unsupported_reset_type_returns_negative_response(self):
        request = bytes([ECU_RESET_SID]) + bytes([0x06])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([ECU_RESET_SID]) + bytes(
            [NRC_SUB_FUNCTION_NOT_SUPPORTED])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_invalid_message_length_returns_negative_response(self):
        request = bytes([ECU_RESET_SID])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([ECU_RESET_SID]) + bytes(
            [NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x19(self):
        request = bytes([READ_DTC_INFO_SID]) + bytes([READ_DTC_INFO_BY_STATUS_MASK])
        response = services.process_service_request(request)
        dtcs = dtc_utils.encode_uds_dtcs(ecu_config.get_dtcs())
        expected_response = get_response_sid(READ_DTC_INFO_SID) + bytes([READ_DTC_INFO_BY_STATUS_MASK]) + bytes(
            [READ_DTC_STATUS_AVAILABILITY_MASK]) + dtcs
        self.assertIsNotNone(response)
        self.assertEqual(3 + len(dtcs), len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x19_with_unsupported_sub_function_returns_negative_response(self):
        request = bytes([READ_DTC_INFO_SID]) + bytes([0x03])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([READ_DTC_INFO_SID]) + bytes(
            [NRC_SUB_FUNCTION_NOT_SUPPORTED])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x19_with_invalid_message_length_returns_negative_response(self):
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([READ_DTC_INFO_SID]) + bytes(
            [NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT])

        request = bytes([READ_DTC_INFO_SID])
        response = services.process_service_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

        request = bytes([READ_DTC_INFO_SID]) + bytes([READ_DTC_INFO_BY_STATUS_MASK]) + bytes([0x01])
        response = services.process_service_request(request)
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())


if __name__ == '__main__':
    unittest.main()
