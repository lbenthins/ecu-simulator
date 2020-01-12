# ECU Simulator

This Python tool simulates some vehicle diagnostic services. It can be used to test OBD-II dongles or tester devices that support the UDS (ISO 14229) and ISO-TP (ISO 15765-2) protocols. 

This tool does NOT implement the ISO-TP protocol. It just simulates a couple of OBD and UDS services. The simulation consists in receiving a diagnostic request (e.g., get DTCs), and responding to it according to the protocol specifications. The data of some responses (e.g., VIN) must be defined in the `ecu_config.json` file.

I created this project to learn more about the OBD and UDS protocols. I did my best to understand the specifications, however, if you suspect that something is implemented wrongly, please let me know. Any feedback will be very appreciated. 

## Supported Services

### OBD-II

| Service | PID    |          Description                   |
|:-------:|:-----: |:---------------------------------------|
| 0x01    | 0x00   | List of supported PIDs in service 0x01 |
| 0x01    | 0x05   | Engine coolant temperature |
| 0x01    | 0x0D   | Vehicle speed |
| 0x01    | 0x2F   | Fuel tank level input |
| 0x01    | 0x51   | Fuel type |
| 0x03    | -      | Request DTCs |
| 0x09    | 0x00   | List of supported PIDs in service 0x09 |
| 0x09    | 0x02   | Vehicle Identification Number (VIN) |
| 0x09    | 0x0A   | ECU name |

### UDS (ISO 14229)

| Service |          Description                                   |
|:-------:|:-------------------------------------------------------|
| 0x10    | ECUReset <br> Supported sub-functions (reset types): 0x01, 0x02, 0x03, 0x04 and 0x05 |
| 0x19    | ReadDTCInformation <br> Supported sub-functions: 0x02 (reportDTCByStatusMask) <br> Default DTCStatusAvailabilityMask: 0XFF <br> Default statusOfDTC: 0x2F| 
 
## Addressing

**OBD:** Functional. See options `obd_broadcast_address` and `obd_ecu_address` in `ecu_config.json`.

**UDS:** Physical. See option `obd_ecu_address` in `ecu_config.json`.

In both cases, only ISO-TP **normal addressing** (only CAN arbitration ID is used) is supported.

## Requirements

* Python3
* [SocketCAN](https://www.kernel.org/doc/Documentation/networking/can.txt) Implementation of the CAN protocol. This kernel module is part of Linux. 
* [ISO-TP kernel module](https://github.com/hartkopp/can-isotp) It is NOT part of linux. It needs to be loaded before running the `ecu-simulator`.
* [isotp](https://can-isotp.readthedocs.io/en/latest/) The `ecu-simulator` only uses [isotp.socket](https://can-isotp.readthedocs.io/en/latest/isotp/socket.html), which is a wrapper for the ISO-TP kernel module.

## Usage 

The `ecu-simulator` try to set up the CAN interface and load the ISO-TP linux kernel module (you need to configure `can_interface`, `can_interface_type`, `can_bitrate`, and `isotp_ko_file_path` in `ecu_config.json`). To perform this task, the tool must be started with root privileges:   

```
sudo python3 ecu-simulator.py
```

If you do not want to start the tool with root privileges, you can do the following:

```
# set up CAN hardware interface
sudo sh can_setup.sh

# or set up CAN virtual interface 
sudo sh vcan_setup.sh

# and then start the tool without sudo
python3 ecu-simulator.py
``` 

## Test Environment  

The `ecu-simulator` was tested on a Raspberry Pi (Raspbian, Linux Kernel 4.19) and PiCAN as CAN-Bus board. 

### OBD-II

The OBD-II services were tested using a real OBD-II scanner.

<img src="https://github.com/lbenthins/ecu-simulator/blob/readme/img/obd.jpg" alt="OBD-II test env" width="555" height="606"/>

### UDS

To test the UDS services, the [Caring Caribou](https://github.com/CaringCaribou/caringcaribou) tool was used.

## Contact

lbenthins@gmail.com 



