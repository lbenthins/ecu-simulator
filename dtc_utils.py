DTC_GROUP = {"P": "00", "C": "01", "B": "10", "U": "11"}

DTC_TYPE = {"0": "00", "1": "01", "2": "10", "3": "11"}

DTC_LENGTH = 5

BIG_ENDIAN = "big"

UDS_DTC_HIGH_BYTE = 0x01

UDS_DTC_DEFAULT_STATUS = 0x2F


def encode_obd_dtcs(dtcs):
    dtcs_bytes = bytearray()
    for dtc in dtcs:
        if is_dtc_valid(dtc):
            dtcs_bytes += get_dtc_first_byte(dtc) + get_dtc_second_byte(dtc)
    return dtcs_bytes


def encode_uds_dtcs(dtcs):
    dtcs_bytes = bytearray()
    for dtc in dtcs:
        if is_dtc_valid(dtc):
            dtcs_bytes += get_dtc_first_byte(dtc) + get_dtc_second_byte(dtc) + bytes([UDS_DTC_HIGH_BYTE]) + \
                          bytes([UDS_DTC_DEFAULT_STATUS])
    return dtcs_bytes


def is_dtc_valid(dtc):
    return len(dtc) == DTC_LENGTH and DTC_GROUP.get(dtc[0]) is not None and DTC_TYPE.get(dtc[1]) is not None \
           and is_hex_value(dtc[2]) and is_hex_value(dtc[3]) and is_hex_value(dtc[4])


def get_dtc_first_byte(dtc):
    bits_0_3 = int(DTC_GROUP.get(dtc[0]) + DTC_TYPE.get(dtc[1]) + "0000", 2)
    bits_4_7 = int("0000" + dtc[2], 16)
    return (bits_0_3 | bits_4_7).to_bytes(1, BIG_ENDIAN)


def get_dtc_second_byte(dtc):
    return int((dtc[3] + dtc[4]), 16).to_bytes(1, BIG_ENDIAN)


def is_hex_value(value):
    try:
        int(value, 16)
        return True
    except ValueError:
        return False
