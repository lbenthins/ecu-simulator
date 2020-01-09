import unittest
from uds import services
import ecu_config_reader as ecu_config
import dtc_utils

ECU_RESET = 0x11

ECU_RESET_HARD = 0x01

ECU_RESET_ENABLE_RAPID_POWER_DOWN = 0x04

READ_DTC_INFO = 0x19

READ_DTC_INFO_BY_STATUS_MASK = 0x02

DTC_STATUS_AVAILABILITY_MASK = 0xFF

NEGATIVE_RESPONSE_ID = 0x7F

NRC_SUB_FUNCTION_NOT_SUPPORTED = 0x12

NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT = 0x13

POSITIVE_RESPONSE_MASK = 0x40


def get_positive_response_sid(sid):
    return bytes([POSITIVE_RESPONSE_MASK + sid])


class TestUdsServices(unittest.TestCase):

    def test_process_service_0x11_with_hard_reset(self):
        request = bytes([ECU_RESET]) + bytes([ECU_RESET_HARD])
        response = services.process_service_request(request)
        expected_response = get_positive_response_sid(ECU_RESET) + bytes([ECU_RESET_HARD])
        self.assertIsNotNone(response)
        self.assertEqual(2, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_enable_power_shut_down(self):
        request = bytes([ECU_RESET]) + bytes([ECU_RESET_ENABLE_RAPID_POWER_DOWN])
        response = services.process_service_request(request)
        expected_response = get_positive_response_sid(ECU_RESET) + bytes([ECU_RESET_ENABLE_RAPID_POWER_DOWN]) + bytes([services.ECU_RESET_POWER_DOWN_TIME])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_unsupported_reset_type_returns_negative_response(self):
        request = bytes([ECU_RESET]) + bytes([0x06])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([ECU_RESET]) + bytes(
            [NRC_SUB_FUNCTION_NOT_SUPPORTED])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x11_with_invalid_message_length_returns_negative_response(self):
        request = bytes([ECU_RESET])
        response = services.process_service_request(request)
        expected_response = bytes([NEGATIVE_RESPONSE_ID]) + bytes([ECU_RESET]) + bytes(
            [NRC_INCORRECT_MESSAGE_LENGTH_OR_INVALID_FORMAT])
        self.assertIsNotNone(response)
        self.assertEqual(3, len(response))
        self.assertEqual(expected_response.hex(), response.hex())

    def test_process_service_0x19(self):
        request = bytes([READ_DTC_INFO]) + bytes([READ_DTC_INFO_BY_STATUS_MASK])
        response = services.process_service_request(request)
        dtcs = ecu_config.get_dtcs()

        expected_response = get_positive_response_sid(READ_DTC_INFO) + bytes([READ_DTC_INFO_BY_STATUS_MASK]) + bytes([DTC_STATUS_AVAILABILITY_MASK]) + dtc_utils.encode_uds_dtcs(dtcs)
        self.assertIsNotNone(response)
        # self.assertEqual(2, len(response))
        self.assertEqual(expected_response.hex(), response.hex())


if __name__ == '__main__':
    unittest.main()
